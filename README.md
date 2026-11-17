# NEXUS Intelligence Cloud

Cloud infrastructure for GPU compute, model serving, fine-tuning, training workflows, and model evaluation across the NEXUS ecosystem.

## Project boundaries

- **NEXUS CORE** owns organization-level goals, projects, policies, and resource allocation.
- **NOVAMIND** owns agent lifecycle, orchestration, memory, and agent performance.
- **NEXUS Intelligence Cloud** owns compute provisioning interfaces, GPU workloads, model serving, training jobs, and evaluation infrastructure.

This repository is the infrastructure layer. It does not assume ownership of agent reasoning or organization-wide policy.

## Engineering principles

1. Secure by default; no public inference endpoint without an authenticated gateway.
2. Separate control plane from GPU data plane.
3. Make expensive GPU operations explicit, observable, and cancellable.
4. Keep provider credentials in a secret manager; never commit secrets.
5. Test control-plane behavior without requiring a GPU.
6. Treat model weights, datasets, and user prompts as sensitive assets.
7. Prefer reproducible images, pinned dependencies, and evidence-backed releases.

## Initial implementation

The first milestone establishes a small FastAPI control-plane service, health endpoints, configuration validation, and a GPU capability probe. Actual GPU provisioning and model serving are intentionally separate follow-up milestones.

## Local development

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn nexus_cloud.app:app --app-dir src --reload
pytest
```

The API listens on `127.0.0.1:8000` by default when run locally. Do not expose it directly to the public internet.

## API

- `GET /health/live` — process liveness.
- `GET /health/ready` — control-plane readiness.
- `GET /v1/compute/gpu` — reports locally visible NVIDIA GPU capability; it does not provision infrastructure.

## Status

Early foundation. No cloud provider is provisioned and no GPU workload is launched by this repository yet.
