from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Tweet(BaseModel):
    pass


class TweetCreate(Tweet):
    content: str


class TweetCreateInternal(TweetCreate):
    profile_id: int
    created_at: datetime = datetime.utcnow()


class TweetRead(Tweet):
    id: int
    profile_id: int
    content: str
    created_at: datetime
    updated_at: Optional[datetime] | None = None
