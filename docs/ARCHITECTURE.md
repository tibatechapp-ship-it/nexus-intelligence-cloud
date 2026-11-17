# NEXUS Intelligence Cloud — Architecture

## Mission and ownership
NEXUS CORE owns organization goals, governance, and resource allocation. NOVAMIND owns agent lifecycle, orchestration, memory, and agent performance. NEXUS Intelligence Cloud owns GPU compute, model serving, training workflows, evaluation execution, and infrastructure telemetry. It does not replace the other two systems.

## Logical layers
1. Control Plane — FastAPI resource/job APIs, lifecycle state, quotas, audit events.
2. Model Gateway — authenticated internal API in front of vLLM; model allow-list, rate/concurrency limits, timeouts.
3. Agent Integration — stable service contracts for NOVAMIND. Agent orchestration remains owned by NOVAMIND.
4. Training Cluster — isolated PyTorch/Transformers jobs, bounded runtime, durable checkpoints.
5. Inference Cluster — vLLM GPU workers, independently deployed and scaled.
6. Data Platform — PostgreSQL metadata, Redis cache/queue, S3-compatible datasets/checkpoints, Qdrant only for approved retrieval workloads.
7. Security & Evaluation — identity, least privilege, secrets, provenance, offline evaluations and promotion gates.
8. Storage & Observability — durable artifacts, Prometheus, Grafana, structured logs, traces, audit records.

## Approved Phase 1 capacity plan (2026-11-17)
- Provider: RunPod Secure Cloud.
- GPU: 1 × NVIDIA H200, 141GB VRAM.
- Host target: 24 vCPU, 276GB RAM, Ubuntu 24.04.
- Persistent volume: 500GB Network Volume.
- Planned GPU usage: 160 hours/month.
- Monthly budget envelope: USD 1,000–1,500.
- Initial model candidate: Qwen/Qwen2.5-7B-Instruct.
- Workloads: inference and controlled fine-tuning/training workflows.
- Prior planning estimate: USD 1,116–1,296/month, based on assumed pricing and usage. This is not a live quote; verify current rates, region, storage, egress, and taxes before provisioning.

## Deployment topology
Phase 1 uses one RunPod Secure Cloud GPU Pod and a persistent volume. Keep the model server private behind an authenticated gateway. Training is explicit, isolated, time-bounded, and cancellable. Kubernetes is deferred until multiple workers or scheduling needs justify its operational cost.

## Security boundaries
Prompts, datasets, model weights, checkpoints, and logs are sensitive. Never commit credentials. Do not log raw prompts by default. Separate control-plane and worker identities. Restrict mounts and network access. Treat downloaded models and datasets as untrusted until provenance checks pass. Never execute arbitrary repository code in the control plane.

## Recovery
Persist job metadata and artifacts independently of worker lifetime. Worker loss marks active jobs interrupted and preserves the last durable checkpoint. Readiness must fail until the model server responds. Backups and restore drills are required before production data is stored.
