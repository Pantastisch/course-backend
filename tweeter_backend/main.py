from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tweeter_backend.routers import profiles, token, tweets

config = dotenv_values(".env")

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profiles.router)
app.include_router(tweets.router)
app.include_router(token.router)


@app.get("/")
async def get_root():
    return {"message": "Hello World from the tweeter_backend!"}
