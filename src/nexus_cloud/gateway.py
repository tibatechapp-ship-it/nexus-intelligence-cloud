"""Private, authenticated gateway to an OpenAI-compatible vLLM server."""

from __future__ import annotations

import asyncio
import secrets
from typing import Any

import httpx
from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field

from nexus_cloud.config import get_settings

router = APIRouter(prefix="/v1", tags=["models"])


class GenerationRequest(BaseModel):
    """Public generation contract; callers cannot choose the model."""

    prompt: str = Field(min_length=1, max_length=32_000)
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class GenerationResponse(BaseModel):
    text: str
    model_id: str
    finish_reason: str | None = None


def _authorize(authorization: str | None, expected_key: str) -> None:
    if not expected_key:
        raise HTTPException(status_code=503, detail="Model gateway is not configured")
    scheme, _, supplied = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not supplied or not secrets.compare_digest(
        supplied, expected_key
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token")


@router.post("/generate", response_model=GenerationResponse)
async def generate(
    payload: GenerationRequest,
    request: Request,
    authorization: str | None = Header(default=None),
) -> GenerationResponse:
    """Generate text through the server-selected model on the private vLLM network."""
    settings = get_settings()
    if not settings.gateway_enabled:
        raise HTTPException(status_code=503, detail="Model serving is disabled")
    _authorize(authorization, settings.gateway_api_key.get_secret_value())

    semaphore: asyncio.Semaphore = request.app.state.generation_semaphore
    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=settings.gateway_queue_timeout)
    except TimeoutError as exc:
        raise HTTPException(status_code=429, detail="Model capacity is currently full") from exc

    try:
        client: httpx.AsyncClient = request.app.state.vllm_client
        upstream = await client.post(
            "/v1/chat/completions",
            json={
                "model": settings.model_id,
                "messages": [{"role": "user", "content": payload.prompt}],
                "max_tokens": payload.max_tokens,
                "temperature": payload.temperature,
                "stream": False,
            },
        )
        if upstream.status_code >= 400:
            raise HTTPException(status_code=502, detail="Model backend returned an error")
        try:
            data: dict[str, Any] = upstream.json()
            choice = data["choices"][0]
            text = choice["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise HTTPException(status_code=502, detail="Invalid model backend response") from exc
        if not isinstance(text, str):
            raise HTTPException(status_code=502, detail="Invalid model backend response")
        return GenerationResponse(
            text=text,
            model_id=settings.model_id,
            finish_reason=choice.get("finish_reason"),
        )
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Model backend timed out") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Model backend is unavailable") from exc
    finally:
        semaphore.release()
