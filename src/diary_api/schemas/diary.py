from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DiaryEntryBase(BaseModel):
    title: str
    content: str


class DiaryEntryCreate(DiaryEntryBase):
    pass


class DiaryEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_done: Optional[bool] = None


class DiaryEntryInDBBase(DiaryEntryBase):
    id: int
    is_done: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DiaryEntry(DiaryEntryInDBBase):
    pass


class DiaryEntryInDB(DiaryEntryInDBBase):
    pass


                     