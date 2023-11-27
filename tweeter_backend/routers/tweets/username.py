from fastapi import APIRouter

from tweeter_backend.models import Tweet
from tweeter_backend.schemas import TweetRead

router = APIRouter(
    prefix="/{username}",
    tags=["tweets"],
)

model = Tweet()


@router.get("/", response_model=list[TweetRead])
async def read_tweets_by_username(username: str):
    raise NotImplementedError
