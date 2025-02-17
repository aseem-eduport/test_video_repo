"""Doubt Clearance Route"""

from fastapi import APIRouter, Depends, HTTPException, Response, Security

# The / prefix is a temporary solution to support existing api and currently we have few apis
router = APIRouter(tags=["Doubt Clearance"])

from typing import Annotated
from fastapi import FastAPI, File
from server.utils.util import generate_response
from server.brain.transcription import generate_transcription_data
from server.utils.current_user import current_user
from server.models.user import Messages, UserMessageHistory
from server.utils.memory_utils import add_generated_response_to_memory

@router.get("/ping")
def ping():
    return "PONG"

@router.post("/question")
async def video_search_api(question: str, user_history: UserMessageHistory = Depends(current_user)):
    generated_content, link = generate_response(question, user_history=user_history)
    if generated_content:
        await add_generated_response_to_memory(generated_content, link, question, user_history)
    return {"content": generated_content, "link": link}

@router.post("/audio")
def audio_transcription(audio_data: Annotated[bytes, File()]):
    transcription = generate_transcription_data(audio_data)
    return transcription
