from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from scalar_fastapi import get_scalar_api_reference

from app.db.session import init_db
from app.controller import v1_router
from app.services.model_garden.model_registry import register_default_models

from dotenv import load_dotenv
load_dotenv()


# =========================
# LIFESPAN EVENTS
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    register_default_models()
    print("🚀 Server started. Database initialized and models registered.")

    yield

    # Shutdown
    print("🛑 Server shutting down.")


# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="AI Toolkit",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)


# =========================
# 🔥 IMPORTANT FIX: CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ✅ allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Chat-Id"],
)


# =========================
# ROUTERS
# =========================
app.include_router(v1_router, prefix="/api/v1")


# =========================
# CUSTOM DOCS (SCALAR)
# =========================
@app.get("/docs", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="AI Toolkit"
    )