from typing import Annotated, NoReturn

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from tweeter_backend.models import Profile, ProfileModel
from tweeter_backend.services import AuthenticationService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticated_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> ProfileModel | NoReturn:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = AuthenticationService().username(token)

    if username is None:
        raise credentials_exception

    user = Profile().read_by_username(username)

    if user is None:
        raise credentials_exception

    return user
