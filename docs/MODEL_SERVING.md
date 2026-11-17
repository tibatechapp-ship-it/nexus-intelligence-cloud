# Model serving gateway

The control plane exposes an authenticated, non-streaming generation endpoint at
`POST /v1/generate`. The model identifier is configured on the server; clients cannot
select arbitrary model names or backend URLs.

## Required configuration

Set these values through the deployment secret/configuration system:

- `NEXUS_GATEWAY_ENABLED=true` only after the private vLLM service is reachable.
- `NEXUS_GATEWAY_API_KEY` to a high-entropy secret (never commit it).
- `NEXUS_VLLM_BASE_URL` to the private internal vLLM URL, not a public address.
- `NEXUS_MODEL_ID` to the exact model served by vLLM.
- `NEXUS_MODEL_REQUEST_TIMEOUT` and `NEXUS_MAX_CONCURRENT_GENERATIONS` to resource-appropriate limits.

The gateway sends requests to vLLM's OpenAI-compatible `/v1/chat/completions` endpoint.
It enforces bearer authentication, request field bounds, a server-side model selection,
an in-process concurrency ceiling, queue timeout, and upstream timeout. It does not log
prompts or completions.

## Network and deployment requirements

- Keep vLLM bound to a private interface/network; expose only the authenticated gateway.
- Terminate TLS at a trusted ingress before any untrusted network.
- Use a dedicated high-entropy key from RunPod Secrets or an approved secret manager.
- For multiple API replicas, replace the in-process semaphore with a shared distributed
  concurrency/rate-limit mechanism before production.
- Add durable audit events, distributed rate limiting, secret rotation, and metrics before
  enabling public traffic.

## Local verification

The gateway is disabled by default. Run `pytest` to verify the control plane without a GPU.
