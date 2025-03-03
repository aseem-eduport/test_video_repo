# from vector_db import client, vector_store, embeddings
from chains import (main_chat_chain,
                    question_validition_chain,
                    eduport_context,
                    select_context_chain,
                    hint_mode_chain)
from vector_db import cloude_embd_col
# from langchain.retrievers import BM25Retriever

def select_best_context_via_gemini(results, question):
    """
    Given a list of context results (each a dict with at least 'content', 'url', and 'chapter_name'),
    use a LangChain prompt chain (powered by Gemini) to select the most relevant transcription.
    Returns the chosen result (a dict).
    """
    # Format the results into a string.
    formatted_results = ""
    for idx, res in enumerate(results):
        excerpt = res.get('content', '')[:200]  # Use first 200 characters for brevity.
        chapter_name = res.get('chapter_name', 'Unknown Chapter')
        formatted_results += f"\nResult {idx+1} (Chapter: {chapter_name}): {excerpt}\n"
    
    chain_input = {
        "question": question,
        "results": formatted_results,
        "num_results": len(results)
    }
    
    # Call the Gemini-powered chain for transcription comparison.
    output = select_context_chain.invoke(chain_input)
    
    try:
        chosen_num = int(output.strip())
        if 1 <= chosen_num <= len(results):
            return results[chosen_num - 1]
        else:
            return results[0]  # Default to the first result if out of range.
    except Exception:
        return results[0]  # Default to the first result if parsing fails.

def generate_youtube_link(context_data):
    start_time = int(context_data.get('timestamp_start', 0))
    end_time = int(context_data.get('timestamp_end', 0)) if context_data.get('timestamp_end') else None
    url = context_data.get('url', '')
    video_url = f"https://youtu.be/{url}?start={start_time}"
    if end_time:
        video_url += f"&end={end_time}"
    return video_url

def generate_vide_data(context_data):
    return context_data.get('content', '')

def generate_context_response(contexts_data, question):
    # Use Gemini (via the select_context_chain) to pick the best transcription context.
    correct_context = select_best_context_via_gemini(contexts_data, question)
    if correct_context:
        link = generate_youtube_link(correct_context)
        video_data = generate_vide_data(correct_context)
    else:
        link = None
        video_data = "Can't find the video for your question."
    return video_data, link

def search_for_timestamp(full_timestamp_data):
    matched_data = []
    full_documents_data = full_timestamp_data['documents'][0]
    for ind, ques in enumerate(full_documents_data):
        processed_data = {
            "url": full_timestamp_data['metadatas'][0][ind]['youtube_id'],
            "video_name": full_timestamp_data['metadatas'][0][ind]['video_title'],
            "content": ques,
            "chapter_name": full_timestamp_data['metadatas'][0][ind]['chapter_name'],
            "timestamp_start": full_timestamp_data['metadatas'][0][ind]['timestamp_start'],
            "timestamp_end": full_timestamp_data['metadatas'][0][ind]['timestamp_end'],
        }
        matched_data.append(processed_data)
    return matched_data

def hint_mode_conversation(question, context, user_input=None):
    """
    A function to simulate the conversation flow in hint mode.
    It will provide ongoing hints and nudges until the user reaches the answer.
    """
    # Keep a history of user responses and AI hints (to make the conversation dynamic)
    conversation_history = []

    # Check the initial context and question to start the hint mode conversation
    prompt = f"Question: {question}\nContext: {context}\n\nStart asking questions or providing hints based on the context. \n" \
             f"The hints should guide the user towards the correct answer without directly giving it."

    # Append the current prompt to the conversation history
    conversation_history.append({"role": "system", "content": prompt})

    # Simulate conversation with the user
    while True:
        # If the user provided an input, use it to create new hints/questions
        if user_input:
            conversation_history.append({"role": "user", "content": user_input})

        # Get the hint or question from the AI (using the hint mode chain)
        hint_response = hint_mode_chain.invoke({
            "context": context,
            "question": question,
            "conversation_history": conversation_history
        })

        # Append the AI's response to the conversation history
        conversation_history.append({"role": "assistant", "content": hint_response})

        # Check if the user has converged on the correct answer
        if "correct answer" in hint_response.lower():  # Assuming you detect when the correct answer is given
            break
        
        # Update user input based on AI's hint
        user_input = hint_response

    return hint_response

def generate_response(question, use_hint_mode=False):
    generated_content, link = None, None

    # Use Llama for question validation.
    validition_response = question_validition_chain.invoke({"question": question})
    if validition_response != 'YES':
        generated_content = main_chat_chain.invoke({'context': eduport_context, 'question': question})
        return generated_content, None

    # Query the top 50 context results from your cloud embeddings.
    context_results = cloude_embd_col.query(query_texts=question, n_results=25)
    processed_data = search_for_timestamp(context_results)
    
    if processed_data:
        # Use Gemini only for transcription comparison to select the best context.
        context, link = generate_context_response(processed_data, question)
    else:
        context = "Can't find the video for the question"
        link = None

    # If hint mode is enabled, use the hint mode conversation flow
    if use_hint_mode:
        generated_content = hint_mode_conversation(question, context)
    else:
        # Use Llama to generate the final answer
        generated_content = main_chat_chain.invoke({"context": context, "question": question})
    
    return generated_content, link