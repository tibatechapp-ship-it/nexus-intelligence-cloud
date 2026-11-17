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

## Local development

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn nexus_cloud.app:app --app-dir src --reload
pytest
ruff check .
```

The API listens on `127.0.0.1:8000` by default when run locally. Do not expose it directly to the public internet.

## API

- `GET /health/live` — process liveness.
- `GET /health/ready` — control-plane readiness.
- `GET /v1/compute/gpu` — reports locally visible NVIDIA GPU capability; it does not provision infrastructure.
- `POST /v1/generate` — authenticated, bounded request to the configured private vLLM server. Disabled by default.

Example request after securely configuring the gateway:

```bash
curl -X POST http://127.0.0.1:8000/v1/generate \
  -H "Authorization: Bearer $NEXUS_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain GPU inference briefly","max_tokens":128}'
```

See [Model Serving](docs/MODEL_SERVING.md) for backend configuration and deployment security requirements.

## Initial infrastructure target

The approved planning target is RunPod Secure Cloud with one NVIDIA H200 141GB GPU, 24 vCPU, 276GB RAM, and a 500GB persistent Network Volume. The planned runtime is 160 GPU-hours/month, within a USD 1,000–1,500 monthly budget envelope. The initial integration candidate is Qwen2.5-7B-Instruct, followed by evaluation and controlled LoRA/QLoRA experiments.

The official RunPod pricing page updated November 12, 2026 lists H200 Secure Cloud at $5.29/GPU-hour and standard Network Volume under 1TB at $0.07/GB/month. The base estimate for 160 GPU-hours plus 500GB is $881.40/month, before optional disks, taxes, or account-specific adjustments. Confirm live data-center availability and the final checkout total before provisioning.

## Status

The repository foundation and authenticated private model gateway are implemented, and CI has passed. No cloud provider resources or GPU workloads have been provisioned. Production deployment remains blocked on live cost/availability confirmation, TLS ingress, durable job/audit state, distributed rate limiting, secret rotation, monitoring, and validation on the target GPU image.
