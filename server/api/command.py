from fastapi import APIRouter
from pydantic import BaseModel
from server.core.deepseek_client import DeepSeekClient

router = APIRouter()
deepseek = DeepSeekClient()

class Command(BaseModel):
    text: str

@router.post("/command")
def process_command(cmd: Command):
    answer = deepseek.ask(cmd.text)
    return {"answer": answer}
