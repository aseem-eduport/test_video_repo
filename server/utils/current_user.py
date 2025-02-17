"""Utils function for current logged in users"""
from fastapi import Header, HTTPException

from server.models.user import UserMessageHistory, Messages

async def current_user(x_user_id: str | None = Header(None)) -> UserMessageHistory:
    if x_user_id:
        user_message_history = await UserMessageHistory.find({"user_id": x_user_id}, fetch_links=True).first_or_none()
        if user_message_history and not user_message_history.is_allowed:
            raise HTTPException(status_code=400, detail="Your not allowed to access it.")
        elif user_message_history:
            return user_message_history
        else:
            starting_history = UserMessageHistory(user_id=x_user_id)
            return await UserMessageHistory.insert_one(starting_history)
    else:
        raise HTTPException(status_code=400, detail="The x-user-id and Authorization is required.")