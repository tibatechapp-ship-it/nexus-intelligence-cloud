"""Typed contracts for model runtime status and generation requests."""

from typing import Literal

from pydantic import BaseModel, Field


class ModelRuntimeStatus(BaseModel):
    status: Literal["not_configured", "starting", "ready", "unavailable"]
    model_id: str | None = None
    endpoint_internal: bool = True


class GenerationRequest(BaseModel):
    """Internal gateway request; model selection remains server-controlled."""

    prompt: str = Field(min_length=1, max_length=32_000)
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class GenerationResult(BaseModel):
    text: str
    model_id: str
    finish_reason: str | None = None
