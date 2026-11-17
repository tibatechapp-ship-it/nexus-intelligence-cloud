"""FastAPI application for the NEXUS Intelligence Cloud control plane."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nexus_cloud import __version__
from nexus_cloud.config import get_settings
from nexus_cloud.gateway import router as model_gateway
from nexus_cloud.gpu import inspect_gpu

settings = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Own outbound model connections and bounded generation concurrency."""
    application.state.vllm_client = httpx.AsyncClient(
        base_url=settings.vllm_base_url.rstrip("/"),
        timeout=httpx.Timeout(settings.model_request_timeout),
        limits=httpx.Limits(
            max_connections=settings.max_concurrent_generations,
            max_keepalive_connections=settings.max_concurrent_generations,
        ),
    )
    import asyncio

    application.state.generation_semaphore = asyncio.Semaphore(
        settings.max_concurrent_generations
    )
    try:
        yield
    finally:
        await application.state.vllm_client.aclose()


app = FastAPI(
    title="NEXUS Intelligence Cloud",
    version=__version__,
    description="Control-plane API for NEXUS compute and model infrastructure.",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
    lifespan=lifespan,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )

app.include_router(model_gateway)


@app.get("/health/live", tags=["health"])
def live() -> dict[str, str]:
    return {"status": "alive", "service": settings.service_name}


@app.get("/health/ready", tags=["health"])
def ready() -> dict[str, str]:
    return {"status": "ready", "service": settings.service_name}


@app.get("/v1/compute/gpu", tags=["compute"])
def gpu_capability() -> dict:
    """Return local GPU visibility; this endpoint never provisions infrastructure."""
    return inspect_gpu()
