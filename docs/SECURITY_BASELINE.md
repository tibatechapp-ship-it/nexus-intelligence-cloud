# Security baseline

Before any public endpoint is enabled:
- TLS termination and authenticated gateway are mandatory.
- Use distinct least-privilege service identities.
- Keep vLLM private; no unauthenticated inference.
- Restrict CORS to exact trusted origins.
- Enforce request size, rate, concurrency, and timeout limits.
- Validate model IDs against a server-side allow-list.
- Redact tokens, prompts, and completions from logs.
- Store credentials in RunPod Secrets or an approved secret manager.
- Pin production container images by digest.
- Scan dependencies/images and review model and dataset provenance/licenses.
- Isolate training workers from the control plane and unrelated volumes.
- Audit provisioning, job start/stop, model deployment, and access changes.

The initial API scaffold is not production-ready. Authentication, durable job state, audit persistence, TLS ingress, secret integration, and observability are blockers before public exposure.
