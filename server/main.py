from fastapi import FastAPI
from server.api.command import router

app = FastAPI(title="AI Voice Assistant")
app.include_router(router)
