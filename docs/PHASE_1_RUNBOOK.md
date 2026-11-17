# Phase 1 — RunPod implementation runbook

## Approved target

RunPod Secure Cloud; one NVIDIA H200 141GB; 24 vCPU; 276GB RAM; Ubuntu 24.04; 500GB persistent standard Network Volume; planned 160 GPU-hours/month; USD 1,000–1,500 monthly ceiling; Qwen/Qwen2.5-7B-Instruct as the initial integration candidate; inference plus controlled LoRA/QLoRA fine-tuning.

The official RunPod pricing page updated November 12, 2026 lists H200 Secure Cloud at USD 5.29/GPU-hour and standard Network Volume under 1TB at USD 0.07/GB/month. At 160 GPU-hours and 500GB, the base estimate is USD 881.40/month ($846.40 compute + $35 storage), before optional disks, taxes, or account-specific adjustments. This is not a checkout quote. Verify the selected data center and final total before provisioning. Never exceed the approved USD 1,500 ceiling.

## Provisioning checklist

1. Use a dedicated RunPod project.
2. Confirm Secure Cloud H200 141GB availability in the selected data center and the full checkout estimate.
3. Attach a 500GB persistent Network Volume in a compatible data center.
4. Use Ubuntu 24.04 with a verified NVIDIA-compatible runtime.
5. Confirm nvidia-smi and CUDA visibility inside the actual workload container.
6. Store credentials in RunPod Secrets; never in Git, image layers, or logs.
7. Restrict inbound ports. Never expose vLLM directly to the public internet.
8. Avoid recursive chown of a large mounted volume at every startup.
9. Test restart, checkpoint persistence, cancellation, and shutdown.
10. Record data center, actual rates, image digest, driver, runtime, and provisioning time.

## Framework compatibility

Do not pin a CUDA/PyTorch/vLLM combination from an old planning note. Select a currently supported vLLM image whose bundled CUDA, PyTorch, driver, and GPU architecture compatibility is documented by its publisher. Pin the immutable image digest, record the exact versions, and run a generation smoke test before accepting the worker. Do not install an unrelated host CUDA toolkit into the container.

## Cost controls

- Cap planned GPU runtime at 160 hours/month.
- Stop GPU workers when no scheduled workload needs them.
- Require owner, purpose, duration, and budget tag for each GPU job.
- Set hard timeouts and cancellation.
- Track GPU-hours and persistent storage separately.
- Alert at 70%, 85%, and 100% of the monthly ceiling.
- No automatic GPU scaling in Phase 1.
- Additional GPUs require manual approval.

## Acceptance criteria

GPU visible inside the container; health/readiness pass; authenticated model smoke test succeeds; weights/checkpoints survive worker restart; training dry-run is isolated; logs contain no credentials or raw prompts; shutdown and budget procedures are tested.

## Provisioning status

No RunPod Pod or volume has been created by these repository changes. Provisioning requires access to the RunPod account, data-center availability confirmation, and approval of the live checkout total.
