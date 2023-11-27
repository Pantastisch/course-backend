from typing import Annotated

from fastapi import APIRouter, Depends

from tweeter_backend import dependencies
from tweeter_backend.models import Profile
from tweeter_backend.schemas import ProfileRead

router = APIRouter(
    prefix="/me",
    tags=["profiles"],
)

model = Profile()


@router.get(
    "/",
    response_model=ProfileRead,
)
async def read_my_profile(
    current_user: Annotated[ProfileRead, Depends(dependencies.authenticated_user)]
):
    return current_user
