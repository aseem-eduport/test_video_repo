import os
from langchain_groq.chat_models import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GROQ_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBLOv_Q-Ejfrs7b6g3Eg5h3Lr8J55_BsGA"
llama_3 = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

gemini_2 = ChatGoogleGenerativeAI(
    model="gemini-2.0-pro-exp-02-05",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

llm = gemini_2