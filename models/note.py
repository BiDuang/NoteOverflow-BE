from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel


class NoteInfo(BaseModel):
    id: int
    author: str | None
    content: str
    update_at: datetime


class CommentInfo(BaseModel):
    id: int
    note_id: int
    author: str | None
    content: str
    update_at: datetime


class PostContent(BaseModel):
    is_anonymous: bool
    content: str


class UpdateContent(BaseModel):
    content: str
