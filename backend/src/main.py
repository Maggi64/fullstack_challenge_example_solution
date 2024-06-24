from datetime import datetime
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from pydantic import BaseModel
from starlette import status


class TimeGetResponse(BaseModel):
    current_time: datetime


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://localhost:{os.getenv('FRONTEND_PORT')}",
        f"http://127.0.0.1:{os.getenv('FRONTEND_PORT')}",
        f"https://{os.getenv('CODESPACE_NAME')}-{os.getenv('FRONTEND_PORT')}.app.github.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_current_time() -> TimeGetResponse:
    """
    This endpoint serves as a very basic example and returns the current time from the
    database.

    It is intentionally kept very simple and doesn't follow best practices regarding
    code structure and separation of concerns yet. Therefore, it doesn't serve as a
    blueprint for your implementation. Please follow known best practices and patterns
    when implementing the task and change the existing code as you see fit.
    """
    connection = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    cursor = connection.cursor()

    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch database time.",
        )
    
    return TimeGetResponse(current_time=result[0])