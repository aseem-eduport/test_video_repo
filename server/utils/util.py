from server.brain.chains import (validation_chain,
                    main_chat_chain,
                    validation_category_chain,
                    general_category_chain,
                    eduport_category_chain,
                    message_summery_chain,
                    select_context_chain,
                    search_query_chain,
                    hint_mode_chain)
from server.brain.vector_db import cloud_embed_col
from server.utils.current_user import CurrentUserResponse
from langchain_community.callbacks.manager import get_openai_callback


def select_best_context(results, question):
    """
    Given a list of context results (each a dict with at least 'content',
    'url', and 'chapter_name'),
    Returns the chosen result (a dict).
    """
    formatted_results = ""
    for idx, res in enumerate(results):
        excerpt = res.get('content', '')
        chapter_name = res.get('chapter_name', 'Unknown Chapter')
        sub_topic = res.get('sub_topic', 'Unknown Sub Topic')
        topic = res.get('topic', 'Unknown Topic')
        subject = res.get('subject', 'Unknown Subject')
        course_name = res.get('course_name', 'Unknown Course Name')
        formatted_results += f"\nResult {idx+1} (Chapter: {chapter_name}, Sub Topic: {sub_topic}, Topic: {topic}, Subject: {subject}, Course Name: {course_name}): {excerpt}\n"
    
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

def get_the_correct_context(context_datas, question):
  for context_data in context_datas:
    page_content = context_data['content']
    valid = validation_chain.invoke({"context": page_content, "question": question})
    if valid == 'TRUE':
      return context_data
  return 'FALSE'

def generate_youtube_link(context_data):
  # metadata = context_data[0].metadata
  start_time = int(context_data['timestamp_start']) if context_data.get('timestamp_start') else 0
  end_time = int(context_data['timestamp_end']) if context_data.get('timestamp_end') else None
  url = context_data['url']
  video_url = f"https://youtu.be/{url}&start={start_time}&end={end_time}"
  return video_url

def generate_vide_data(context_data):
  data = context_data['content']
  # confidence = context_data[1]
  return data

def generate_context_response(contexts_data, question):
  correct_context = get_the_correct_context(contexts_data, question)
  if correct_context != 'FALSE':
    link = generate_youtube_link(correct_context)
    video_data = generate_vide_data(correct_context)
  else:
    link = None
    video_data = "Can't find the video for your question."
  return video_data, link

def get_main_video_data(context):
  url_tag = context['metadatas'][0][0]['youtube_id']
  video_name = context['metadatas'][0][0]['video_title']
  content = context['documents'][0][0]
  return url_tag, video_name, content

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
  
# def generate_response(question, user_history: CurrentUserResponse=None):
#   generated_content, link, context = None, None, None
#   history = []
#   for message in user_history.messages:
#       history.append({"role": "user", "content": message.question})
#       history.append({"role": "assistant", "content": message.answer})
#   print(history)
#   with get_openai_callback() as cb:
#     validation_response = question_validation_chain.invoke({"question": question, "history": history}).strip()
#     print(validation_response)
#     if validation_response !=  'YES':
#       generated_content = main_chat_chain.invoke({'context': eduport_context, 'question': question, 'history': history})
#       return generated_content, None, cb.total_tokens
#     context = cloud_embed_col.query(query_texts=question, n_results=1)
#     processed_data = search_for_timestamp(context) if context else None
#     if processed_data:
#       context = generate_vide_data(processed_data[0])
#       link = generate_youtube_link(processed_data[0])
#     else:
#       context = "Can't find the video for the question"
#       link = None
#     # context, link = generate_context_response(processed_data, question)
#     print(new_main_template.format(context=context, question=question, history=history))
#     generated_content = main_chat_chain.invoke({"context": context, "question": question, 'history': history})
#     print(cb.total_tokens)
#     return generated_content, link, cb.total_tokens

def generate_general_response(question):
  response = general_category_chain.invoke({"user_input": question})
  return response, None

def generate_eduport_response(question):
  response = eduport_category_chain.invoke({"user_input": question})
  return response, None

def generate_history_summary(user_history: CurrentUserResponse=None):
  # history = []
  summary = ""

  # for message in user_history.messages[:10]:
  #   history.append({"role": "user", "content": message.question, "timestamp": message.created_at})
  #   history.append({"role": "assistant", "content": message.answer, "timestamp": message.created_at})

  if user_history.messages:
    summary = message_summery_chain.invoke({"history": user_history.messages[:20]})
  return summary

def generate_context_response(contexts_data, question):
    # Use Gemini (via the select_context_chain) to pick the best transcription context.
    correct_context = select_best_context(contexts_data, question)
    if correct_context:
        link = generate_youtube_link(correct_context)
        video_data = generate_vide_data(correct_context)
    else:
        link = None
        video_data = "Can't find the video for your question."
    return video_data, link

def generate_study_response(question, user_history: CurrentUserResponse=None):
  context = ""
  link = None
  history_summary = generate_history_summary(user_history)
  is_video_search = search_query_chain.invoke({"question": question}).rstrip()
  if is_video_search == 'YES':
    context = cloud_embed_col.query(query_texts=question, n_results=25)
    processed_data = search_for_timestamp(context) if context else None
    if processed_data:
      context, link = generate_context_response(processed_data, question)
  
  generated_content = main_chat_chain.invoke({"context": context,
                                              "question": question,
                                              "history": history_summary,})
  return generated_content, link

def hint_mode(question: str, user_history: CurrentUserResponse, context: str = ""):
    """
    This function is triggered when Hint Mode is enabled. It gathers the user's chat history
    and passes it along with the current question and context to the `hint_mode_chain`.
    """
    # Step 1: Gather the conversation history
    conversation_history = []
    for message in user_history.messages:
        conversation_history.append(f"User: {message.question}")
        conversation_history.append(f"Assistant: {message.answer}")
    
    # Step 2: Format the conversation history as a string
    conversation_history_str = "\n".join(conversation_history)
    
    # Step 3: Prepare the input for the hint_mode_chain.
    # We have the `question`, `context`, and the formatted `conversation_history`.
    chain_input = {
        "question": question,
        "context": context,
        "conversation_history": conversation_history_str
    }
    
    # Step 4: Generate the hint by invoking the `hint_mode_chain`.
    generated_hint = hint_mode_chain.invoke(chain_input)
    
    return generated_hint, None  # No video link needed for hint mode (assuming no link is returned)

def generate_response(question, user_history: CurrentUserResponse=None):
  with get_openai_callback() as cb:
    generated_content, link = None, None
    validated_category = validation_category_chain.invoke({"user_input": question}).rstrip()
    match validated_category:
      case "GENERAL":
        generated_content, link= generate_general_response(question)
      case "EDUPORT":
        generated_content, link = generate_eduport_response(question)
      case "STUDY":
        generated_content, link = generate_study_response(question, user_history)
      case _:
        generated_content, link = None, None
    return generated_content, link, cb.total_tokens