from pydantic import BaseModel


class Command(BaseModel):
    intent: str
    response: str


class Task(BaseModel):
    text: str
    time: str
