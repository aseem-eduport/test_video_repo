from typing import Annotated
from fastapi import FastAPI, File, Query
from fastapi.middleware.cors import CORSMiddleware
from util import generate_response
from trasncription import generate_transcription_data

app = FastAPI()

# CORS setup
allowed_orgins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return "PONG"

# Add use_hint_mode query parameter to toggle hint mode
@app.post("/question")
def video_search_api(
    question: str, 
    use_hint_mode: bool = Query(False, description="Set to true to use hint mode")
):
    # Pass the use_hint_mode flag to the generate_response function
    generated_content, link = generate_response(question, use_hint_mode)
    return {"content": generated_content, "link": link}

@app.post("/audio")
def audio_transcription(audio_data: Annotated[bytes, File()]):
    transcription = generate_transcription_data(audio_data)
    return transcription