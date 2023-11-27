from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from tweeter_backend.models import Profile
from tweeter_backend.schemas import AccessToken
from tweeter_backend.services import AuthenticationService, PasswordService

router = APIRouter(
    prefix="/token",
    tags=["token"],
)


@router.post("/", response_model=AccessToken)
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = Profile().read_by_username(form_data.username)

    if not user:
        raise credentials_exception

    if not PasswordService().verify(form_data.password, user.hashed_password):
        raise credentials_exception

    access_token = AuthenticationService().encode(claims={"sub": user.username.lower()})

    return {"access_token": access_token, "token_type": "bearer"}
