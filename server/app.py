from contextlib import asynccontextmanager

from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk

from server.config import CONFIG
from server.models.user import UserMessageHistory, Messages

sentry_sdk.init(
    dsn="https://d1fbd9baf245ed2fd702715b64b3eccd@sentry.eduport.in/14",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    send_default_pii=True,
    profiles_sample_rate=1.0,
)

DESCRIPTION = """
This API powers the doubts cleare module

It supports:
- Video searching
- Doubt clearance
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application service"""
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri).doubt_clearance
    await init_beanie(app.db, document_models=[UserMessageHistory, Messages])
    print("Startup Complete")
    yield
    print("Shutdown complete")

app = FastAPI(
    title="Doubt Clearance",
    description=DESCRIPTION,
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)