from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from tweeter_backend import dependencies
from tweeter_backend.models import Tweet
from tweeter_backend.schemas import (
    ProfileRead,
    TweetCreate,
    TweetCreateInternal,
    TweetRead,
)

from . import id as id_routes
from . import username

router = APIRouter(
    prefix="/tweets",
    tags=["tweets"],
)

model = Tweet()


@router.post(
    "/",
    dependencies=[Depends(dependencies.authenticated_user)],
    response_model=TweetRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_tweet(
    current_user: Annotated[ProfileRead, Depends(dependencies.authenticated_user)],
    tweet: TweetCreate,
):
    tweet_model = TweetCreateInternal(**tweet.model_dump(), profile_id=current_user.id)

    new_tweet = model.create(tweet_model)

    return new_tweet


@router.get("/", response_model=list[TweetRead])
async def read_tweets():
    tweets = model.read_all()

    # Return 204 No Content if there are no tweets.
    if not tweets:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No tweets found.",
        )

    return tweets


router.include_router(id_routes.router)
router.include_router(username.router)
