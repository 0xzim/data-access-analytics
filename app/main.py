from fastapi import FastAPI
from .auth import router as auth_router
from .database import Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Data Access Monitoring System")
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Welcome to the Cloud Data Access Monitoring Project"}