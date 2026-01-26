from fastapi import APIRouter
from pydantic import BaseModel
from server.core.deepseek_client import parse_command
from server.core.executor import execute_command

router = APIRouter()


class CommandRequest(BaseModel):
    text: str


class CommandResponse(BaseModel):
    answer: str


@router.post("/command", response_model=CommandResponse)
def command_endpoint(cmd: CommandRequest):
    parsed = parse_command(cmd.text)
    answer = execute_command(parsed)
    return {"answer": answer}
