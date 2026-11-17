# RunPod deployment target

Phase 1 target: one RunPod Secure Cloud H200 141GB Pod, 24 vCPU, 276GB RAM, Ubuntu 24.04, and a 500GB persistent Network Volume. Planned usage is 160 GPU-hours/month within the USD 1,000–1,500 monthly envelope.

Do not provision until current pricing and availability are checked and the full estimate fits the approved ceiling. This repository does not create cloud resources.

Use RunPod Secrets for credentials. Keep model serving private behind an authenticated gateway. Validate GPU passthrough from inside the actual workload container using nvidia-smi and a CUDA framework check. Never expose the vLLM port publicly.
