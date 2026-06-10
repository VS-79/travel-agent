from fastapi import FastAPI
from app.api.routes import chat, health, trips

app = FastAPI(title="Travel Agent API", version="1.0.0")

app.include_router(health.router)
app.include_router(chat.router, prefix="/api")
app.include_router(trips.router, prefix="/api")