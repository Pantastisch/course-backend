from fastapi import APIRouter, HTTPException, status

from tweeter_backend.models import Profile
from tweeter_backend.schemas import ProfileRead

router = APIRouter(
    prefix="/{username}",
    tags=["profiles"],
)

model = Profile()


@router.get("/", response_model=ProfileRead)
async def read_profile_by_username(username: str):
    profile = model.read_by_username(username)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return profile
