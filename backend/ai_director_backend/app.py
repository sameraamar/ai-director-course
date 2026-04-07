import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_director_backend.api.routes import router
from ai_director_backend.services.gemini_service import (
    get_gemini_model,
    gemini_synthesis_enabled,
    verbose_ai_logging_enabled,
)


def configure_backend_logging() -> logging.Logger:
    backend_logger = logging.getLogger("ai_director_backend")
    uvicorn_error_logger = logging.getLogger("uvicorn.error")

    if uvicorn_error_logger.handlers:
        backend_logger.handlers = uvicorn_error_logger.handlers

    if not backend_logger.handlers:
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(logging.Formatter("%(levelname)s:     %(message)s"))
        backend_logger.addHandler(stream_handler)

    backend_logger.setLevel(logging.INFO)
    backend_logger.propagate = False
    return backend_logger


backend_logger = configure_backend_logging()


app = FastAPI(
    title="AI Director Course Backend",
    description="Initial API skeleton for the grounded course assistant.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.on_event("startup")
async def log_backend_runtime_configuration() -> None:
    configure_backend_logging()
    backend_logger.info(
        "AI Director backend startup: gemini_enabled=%s verbose_logging=%s model=%s",
        gemini_synthesis_enabled(),
        verbose_ai_logging_enabled(),
        get_gemini_model(),
    )
