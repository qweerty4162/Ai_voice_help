from fastapi import FastAPI
from server.api.command import router

app = FastAPI(title="Voice Assistant Server")
app.include_router(router)
