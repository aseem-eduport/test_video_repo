from typing import Annotated, Any, Optional, List
from datetime import datetime

from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field

class Messages(Document):
    question: str
    answer: str
    video_url: str | None = None
    token_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)


class UserMessageHistory(Document):
    """User Data and Message History"""
    user_id: Annotated[str, Indexed(str, unique=True)]
    total_token: int = 0
    is_allowed: bool = True
    messages: Optional[List[Link[Messages]]] = []

    @property
    def created(self) -> datetime | None:
        """Datetime user was created from ID."""
        return self.id.generation_time if self.id else None