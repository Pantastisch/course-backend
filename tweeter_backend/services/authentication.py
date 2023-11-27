from datetime import datetime, timedelta

from dotenv import dotenv_values
from jose import jwt

config = dotenv_values(".env")


class AuthenticationService:
    secret_key: str
    algorithm: str

    def __init__(self):
        self.secret_key = self._get_env_var("SECRET_KEY")
        self.algorithm = self._get_env_var("ALGORITHM")

    def _get_env_var(self, key: str, default: str = "") -> str:
        value = config.get(key)

        if not value:
            if not default:
                raise ValueError(f"{key} is not set")

            value = default

        return value

    def encode(self, claims: dict):
        claims_to_encode = claims.copy()

        exp = datetime.utcnow() + timedelta(minutes=30)

        claims_to_encode.update({"exp": exp})

        encoded_jwt = jwt.encode(
            claims=claims_to_encode,
            key=self.secret_key,
            algorithm=self.algorithm,
        )

        return encoded_jwt

    def decode(self, token: str):
        payload = jwt.decode(
            token=token,
            key=self.secret_key,
            algorithms=[self.algorithm],
        )

        return payload

    def username(self, token: str):
        payload = self.decode(token)

        return payload.get("sub")
