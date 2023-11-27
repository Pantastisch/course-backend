from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from tweeter_backend import dependencies
from tweeter_backend.models import Profile
from tweeter_backend.schemas import ProfileCreate, ProfileCreateInternal, ProfileRead
from tweeter_backend.services import PasswordService

from . import me, username

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)

model = Profile()


@router.post("/", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(profile: ProfileCreate):
    new_profile = ProfileCreateInternal(**profile.model_dump())

    if not PasswordService().is_bcrypt(new_profile.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid hashed password.",
        )

    return model.create(new_profile)


@router.get("/", response_model=list[ProfileRead])
async def read_profiles():
    profiles = model.read_all()

    # Return 204 No Content if there are no profiles.
    if not profiles:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No profiles found.",
        )

    return profiles


router.include_router(me.router)
router.include_router(username.router)
