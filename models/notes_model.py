from pydantic import BaseModel
from datetime import datetime


class Data(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    category: str
    user_id: str


class NoteModel(BaseModel):
    success: bool
    status: int
    message: str
    data: Data


class NoteListModel(BaseModel):
    success: bool
    status: int
    message: str
    data: list[Data]
