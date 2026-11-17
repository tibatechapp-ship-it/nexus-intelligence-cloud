# Coding model evaluation — first gate

This repository now includes a small, reproducible smoke harness for comparing candidate coding models through a private OpenAI-compatible vLLM endpoint.

## What it measures

- Whether a response contains code.
- Whether the returned Python parses with the standard-library AST parser.
- Request latency (mean and p95) across a fixed task set.

It **does not execute model output**. It does not measure functional correctness, security, repository-level repair ability, or pass@k. A syntax-valid response is not necessarily a correct solution. Do not publish these smoke results as a competitive leaderboard.

## Run

Install the project and development dependencies, then point the runner at a private vLLM service:

```bash
python -m pip install -e ".[dev]"
export NEXUS_BENCHMARK_API_KEY="provided-through-your-secret-manager"
python scripts/evaluate_coding_model.py \
  --base-url http://127.0.0.1:8001 \
  --model Qwen/Qwen2.5-7B-Instruct \
  --cases benchmarks/coding_smoke.json \
  --output reports/coding-evaluation.json
```

The bearer key is optional for a private endpoint with no authentication, but the service must remain network-private. If authentication is enabled, inject the key through the environment/secret manager. Never commit it.

The runner defaults to concurrency 1 to avoid overloading a single GPU. It writes full model responses to the chosen local report path; treat that report as potentially sensitive.

## Promotion gates — not yet implemented

Before a model can be called production-ready, add isolated container execution with no network, read-only root filesystem, dropped Linux capabilities, CPU/memory/PID/time limits, curated hidden tests, static security scanning, regression tasks, and human-reviewed promotion. Do not run generated code directly on the control-plane host.

## Initial cases

The initial five Python tasks are smoke tests only. Expand the suite with multi-file repository tasks, bug-fix tasks, tests-first tasks, dependency/security cases, multilingual requirements, and adversarial prompt-injection fixtures. Version and hash each dataset release to preserve comparability.
