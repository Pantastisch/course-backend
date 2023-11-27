from passlib.context import CryptContext


class PasswordService:
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str):
        return self.context.hash(password)

    def verify(self, plain_password: str, hashed_password: str):
        return self.context.verify(plain_password, hashed_password)

    def is_bcrypt(self, hashed_password: str):
        return self.context.identify(hashed_password) == "bcrypt"
