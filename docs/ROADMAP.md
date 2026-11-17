# Delivery roadmap

## Phase 0 — Repository foundation
- [x] Python package, FastAPI health endpoints, GPU probe, tests, Dockerfile, CI workflow.
- [x] Approved RunPod architecture and cost envelope documented.
- [ ] Validate CI on GitHub Actions.

## Phase 1 — Secure cloud foundation
- [ ] Verify live RunPod H200 availability and full cost estimate.
- [ ] Provision one Secure Cloud H200 and 500GB persistent volume after cost confirmation.
- [ ] Bootstrap Ubuntu 24.04/NVIDIA runtime and verify GPU passthrough.
- [ ] Add authenticated ingress, service identities, secrets, and network restrictions.
- [ ] Add durable job metadata and audit events.

## Phase 2 — Model serving
- [ ] Deploy compatible vLLM image on the GPU worker.
- [ ] Keep model server private behind the Model Gateway.
- [ ] Add auth, model allow-list, request limits, timeouts, and concurrency controls.
- [ ] Smoke-test Qwen/Qwen2.5-7B-Instruct.
- [ ] Measure throughput, latency, VRAM, and cost per request.

## Phase 3 — Fine-tuning and evaluation
- [ ] Add isolated, bounded training jobs.
- [ ] Begin with a small LoRA/QLoRA experiment, not full-model training.
- [ ] Persist datasets, configs, logs, and checkpoints in controlled storage.
- [ ] Add evaluation and safety/regression gates before model promotion.

## Phase 4 — Data and observability
- [ ] PostgreSQL migrations and backup/restore tests.
- [ ] Redis lifecycle and queue policy.
- [ ] Object storage for immutable artifacts.
- [ ] Prometheus/Grafana, structured logs, traces, and budget alerts.

## Phase 5 — Ecosystem integration
- [ ] Integrate gateway with NOVAMIND through a stable service contract.
- [ ] Integrate resource/job governance with NEXUS CORE.
- [ ] Verify identity boundaries, quotas, auditability, and failure recovery.

## Deferred
Training a foundation model from scratch, multi-GPU clusters, automatic GPU autoscaling, and Kubernetes until scale justifies them.
