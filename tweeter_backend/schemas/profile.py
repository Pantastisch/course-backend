from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    pass


class ProfileCreate(Profile):
    username: str
    email: EmailStr
    hashed_password: str


class ProfileCreateInternal(ProfileCreate):
    created_at: datetime = datetime.utcnow()


class ProfileRead(Profile):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] | None = None
