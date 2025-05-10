import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.models import EmailTracking
from app.models import Event
from app.models import User
from app.models import UserEvent
from app.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    for model in [User, Event, UserEvent, EmailTracking]:
        if not model.exists():
            model.create_table(read_capacity_units=1000, write_capacity_units=1000, wait=True)
    yield


app = FastAPI(title=os.getenv("PROJECT_NAME", "supermomos"), debug=False, version="1.0", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
