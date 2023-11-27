from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from tweeter_backend import dependencies
from tweeter_backend.models import Tweet
from tweeter_backend.schemas import ProfileRead, TweetRead

router = APIRouter(
    prefix="/{id}",
    tags=["tweets"],
)

model = Tweet()


@router.get("/", response_model=TweetRead)
async def read_tweet_by_id(tweet_id: Annotated[int, Path(ge=0, alias="id")]):
    tweet = model.read_by_id(tweet_id)

    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return tweet


@router.put(
    "/",
    dependencies=[Depends(dependencies.authenticated_user)],
    response_model=TweetRead,
)
async def update_tweet_by_id(
    current_user: Annotated[ProfileRead, Depends(dependencies.authenticated_user)],
    tweet_id: Annotated[int, Path(ge=0, alias="id")],
    # tweet: TweetCreate,
):
    raise NotImplementedError


@router.delete(
    "/",
    dependencies=[Depends(dependencies.authenticated_user)],
    response_model=TweetRead,
)
async def delete_tweet_by_id(
    current_user: Annotated[ProfileRead, Depends(dependencies.authenticated_user)],
    tweet_id: Annotated[int, Path(ge=0, alias="id")],
):
    raise NotImplementedError
