from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Column, DateTime, Integer, String

from tweeter_backend.schemas import ProfileCreateInternal
from tweeter_backend.services import DatabaseService

from .base import Base


class ProfileOrm(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(72), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


class ProfileModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)
    hashed_password: str = Field(max_length=72)
    created_at: datetime
    updated_at: datetime | None


class Profile:
    def create(self, profile: ProfileCreateInternal) -> ProfileModel:
        session = DatabaseService().session()

        orm_profile = ProfileOrm(**profile.model_dump())

        with session.begin():
            session.add(orm_profile)
            session.flush()

        return ProfileModel.model_validate(orm_profile)

    def read_all(self) -> list[ProfileModel]:
        session = DatabaseService().session()

        with DatabaseService().session().begin():
            orm_profiles = session.query(ProfileOrm).all()

        return [ProfileModel.model_validate(profile) for profile in orm_profiles]

    def read_by_id(self, profile_id: int) -> ProfileModel | None:
        session = DatabaseService().session()

        with session.begin():
            orm_profile = session.query(ProfileOrm).filter_by(id=profile_id).first()

        if orm_profile is None:
            return None

        return ProfileModel.model_validate(orm_profile)

    def read_by_username(self, username: str) -> ProfileModel | None:
        session = DatabaseService().session()

        with session.begin():
            orm_profile = session.query(ProfileOrm).filter_by(username=username).first()

        if orm_profile is None:
            return None

        return ProfileModel.model_validate(orm_profile)
