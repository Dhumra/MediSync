# Starts Front-End service logic (e.g., runs FastAPI server or CLI interface).

# frontend-service/main.py

from fastapi import FastAPI
from routers import appointment

app = FastAPI()
app.include_router(appointment.router)
