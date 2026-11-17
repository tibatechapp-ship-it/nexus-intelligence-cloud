"""FastAPI application for the NEXUS Intelligence Cloud control plane."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nexus_cloud import __version__
from nexus_cloud.config import get_settings
from nexus_cloud.gpu import inspect_gpu

settings = get_settings()

app = FastAPI(
    title="NEXUS Intelligence Cloud",
    version=__version__,
    description="Control-plane API for NEXUS compute and model infrastructure.",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )


@app.get("/health/live", tags=["health"])
def live() -> dict[str, str]:
    return {"status": "alive", "service": settings.service_name}


@app.get("/health/ready", tags=["health"])
def ready() -> dict[str, str]:
    return {"status": "ready", "service": settings.service_name}


@app.get("/v1/compute/gpu", tags=["compute"])
def gpu_capability() -> dict:
    """Return local GPU visibility; this endpoint never provisions compute."""
    return inspect_gpu()
