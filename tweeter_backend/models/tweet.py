from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from tweeter_backend.schemas import TweetCreateInternal
from tweeter_backend.services import DatabaseService

from .base import Base


class TweetOrm(Base):
    __tablename__ = "tweets"

    id = Column(Integer, autoincrement=True, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class TweetModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile_id: int
    content: str = Field(max_length=1000)
    created_at: datetime
    updated_at: datetime | None


class Tweet:
    def create(self, tweet: TweetCreateInternal) -> TweetModel:
        session = DatabaseService().session()

        orm_tweet = TweetOrm(**tweet.model_dump())

        with session.begin():
            session.add(orm_tweet)
            session.flush()

        return TweetModel.model_validate(orm_tweet)

    def read_all(self) -> list[TweetModel]:
        session = DatabaseService().session()

        with session.begin():
            orm_tweets = session.query(TweetOrm).all()

        return [TweetModel.model_validate(tweet) for tweet in orm_tweets]

    def read_by_id(self, tweet_id: int) -> TweetModel | None:
        session = DatabaseService().session()

        with session.begin():
            orm_tweet = session.query(TweetOrm).filter_by(id=tweet_id).first()

        return TweetModel.model_validate(orm_tweet) if orm_tweet else None
