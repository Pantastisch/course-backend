from dotenv import dotenv_values
from fastapi import FastAPI

from tweeter_backend.routers import profiles, token, tweets

config = dotenv_values(".env")

app = FastAPI()

app.include_router(profiles.router)
app.include_router(tweets.router)
app.include_router(token.router)


@app.get("/")
async def get_root():
    return {"message": "Hello World from the tweeter_backend!"}
