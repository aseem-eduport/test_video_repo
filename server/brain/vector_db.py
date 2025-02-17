# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# class LocalHuggingFaceEmbeddingFunction(chromadb.EmbeddingFunction[chromadb.Documents]):
#     def __init__(self, model_name: str):
#         self.model = SentenceTransformer(model_name)

#     def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
#         #Convert the numpy array to a Python list
#         return self.model.encode(input).tolist()

# setup chromadb client
# client = chromadb.PersistentClient(path="./chroma_db")

# vector_store = Chroma(client=client,
#                       collection_name="video_embeddings3",
#                       embedding_function=embeddings,)

# # collection
# timestamp_collection = client.get_or_create_collection(name="video_embeddings3", metadata={"hnsw:space": "cosine"})
# full_text_collection = client.get_or_create_collection(name="video_embeddings5", metadata={"hnsw:space": "cosine"})

# embedding_ef = LocalHuggingFaceEmbeddingFunction('all-MiniLM-L6-v2')
# new_vector_store = chromadb.PersistentClient(path="./chroma_new_db")
# new_vector_col = new_vector_store.get_collection("timestamp_vdb", embedding_function=embedding_ef)

cloud_emb_store = chromadb.HttpClient(host='95.217.21.180', port=8005)
# cloude_embd_col = cloude_emb_store.get_collection("timestamp_vdb")
cloud_embed_col = cloud_emb_store.get_collection("Timestamped_Transcription_NEET_3")