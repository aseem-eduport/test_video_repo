import os
from langchain_groq.chat_models import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GROQ_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCkNqf6Bpmwi_fax72ukDXiJIZ-dI2kJPA"
llama_3 = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

gemini_2_flash = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

gemini_2_flash_exp = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

llm = llama_3