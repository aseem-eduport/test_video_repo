# from vector_db import client, vector_store, embeddings
from server.brain.chains import (validation_chain,
                    main_chat_chain,
                    question_validation_chain,
                    eduport_context,)
from server.brain.vector_db import cloud_embed_col
from server.models.user import UserMessageHistory
# from langchain.retrievers import BM25Retriever

#print(vector_store.similarity_search("gravitaional field", filter={"timestamp_end": {"$gte": 90}}))

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

# def generate_topics(question):
#   rewrited_question = generate_topic_chain.invoke({"question": question})
#   return rewrited_question

# def fetch_from_full_text_db(question):
#   query_result = full_text_collection.query(query_texts=[question], n_results=1)
#   if query_result:
#     return query_result

# def fetch_from_timestamp_db(url):
#   query_result = timestamp_collection.get(where={"url": url})
#   if query_result:
#     return query_result

# def generate_response(question):
#   topic_list = generate_topics(question)
#   # context_data = vector_store.similarity_search_by_vector(embeddings.embed_query(question), k=5)
#   # context_data = fetch_from_full_text_db(question)
#   context_data = fetch_from_full_text_db(question)
#   context, link = generate_context_response(context_data, question)
#   if link and topic_list:
#     context, link = 
#   generated_content = main_chat_chain.invoke({"context": context, "question": question})
#   print(generated_content, link, context, "--------generated content--------")
#   return generated_content, link

def get_main_video_data(context):
  url_tag = context['metadatas'][0][0]['youtube_id']
  video_name = context['metadatas'][0][0]['video_title']
  content = context['documents'][0][0]
  return url_tag, video_name, content

def search_for_timestamp(full_timestamp_data):
  similarity_distance = full_timestamp_data['distances'][0][0]
  matched_data = []
  if similarity_distance <= 0.7:
    full_documents_data = full_timestamp_data['documents'][0]
    for ind, ques in enumerate(full_documents_data):
      processed_data = {
        "url": full_timestamp_data['metadatas'][0][ind]['youtube_id'],
        "video_name": full_timestamp_data['metadatas'][0][ind]['video_title'],
        "content": ques,
        "timestamp_start": full_timestamp_data['metadatas'][0][ind]['timestamp_start'],
        "timestamp_end": full_timestamp_data['metadatas'][0][ind]['timestamp_end'],
      }
      matched_data.append(processed_data)
  return matched_data

# def generate_response(question):
#   generated_content, link, context = None, None, None
#   topic_list = generate_topics(question)
#   main_video_context = fetch_from_full_text_db(question)
#   if main_video_context.get('documents'):
#     link, video_name, context = get_main_video_data(main_video_context)
#     if topic_list:
#       timestamp_context = search_for_timestamp(topic_list, link)
#       print(timestamp_context)
#       if timestamp_context:
#         context, link = generate_context_response(timestamp_context, question)
#         # print("timestampt data--------", context)
#     generated_content = main_chat_chain.invoke({"context": context, "question": question})
#     print(generated_content, link, context, "--------generated content--------")
#   return generated_content, link

# def get_bm25search(question):
#   all_text_chunk = vector_store.get()['documents']
#   keyword_retriever = BM25Retriever.from_texts(all_text_chunk)
#   keyword_retriever.k =  1
#   response = keyword_retriever.invoke(question)
#   return response[0] if response else None

# def generate_response(question):
#   generated_content, link, context = None, None, None
#   context = get_bm25search(question)
#   if not context:
#     return "Cant find the video", None
#   context_data = timestamp_collection.get(where_document={"$contains": context.page_content}, limit=1)
#   # valid = validation_chain.invoke({"context": context_data, "question": question})
#   # if valid == "FALSE":
#   #   context, link = "Cant find the video", None
#   # else:
#   link = generate_youtube_link(context_data['metadatas'][0])
#   generated_content = main_chat_chain.invoke({"context": context, "question": question})
#   print(generated_content, link, context, "--------generated content--------")
#   return generated_content, link
  
def generate_response(question, user_history: UserMessageHistory=None):
  generated_content, link, context = None, None, None
  messages = sorted(user_history.messages, key=lambda message: message.created_at)[:10]
  user_history = ""
  for indx, message in enumerate(messages):
      user_history += f"\nQuestion{indx}: {message.question}\nAnswer{indx}: {message.answer}"
  validation_response = question_validation_chain.invoke({"question": question})
  if validation_response !=  'YES':
    generated_content = main_chat_chain.invoke({'context': eduport_context, 'question': question, 'history': user_history})
    return generated_content, None
  context = cloud_embed_col.query(query_texts=question, n_results=1)
  processed_data = search_for_timestamp(context) if context else None
  if processed_data:
    context = generate_vide_data(processed_data[0])
    link = generate_youtube_link(processed_data[0])
  else:
    context = "Can't find the video for the question"
    link = None
  # context, link = generate_context_response(processed_data, question)
  generated_content = main_chat_chain.invoke({"context": context, "question": question, 'history': user_history})
  return generated_content, link