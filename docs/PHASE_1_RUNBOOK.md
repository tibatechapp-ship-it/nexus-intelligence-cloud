# Phase 1 — RunPod implementation runbook

## Approved target
RunPod Secure Cloud; one NVIDIA H200 141GB; 24 vCPU; 276GB RAM; Ubuntu 24.04; 500GB persistent Network Volume; planned 160 GPU-hours/month; USD 1,000–1,500 monthly ceiling; Qwen/Qwen2.5-7B-Instruct as the initial candidate; inference plus controlled fine-tuning.

The previous estimate was USD 1,116–1,296/month under the planning rate and 160 GPU-hours. It is not a current quote. Before creating resources, verify current H200 Secure Cloud availability and the complete cost including volume, idle/stopped behavior, network, snapshots, and taxes. Do not exceed the approved ceiling without explicit approval.

## Provisioning checklist
1. Use a dedicated RunPod project.
2. Select Secure Cloud H200 141GB meeting the CPU/RAM target.
3. Attach a 500GB persistent Network Volume in a compatible region.
4. Use Ubuntu 24.04 with a verified NVIDIA-compatible runtime.
5. Confirm nvidia-smi and CUDA visibility inside the actual workload container.
6. Store credentials in RunPod Secrets; never in Git, image layers, or logs.
7. Restrict inbound ports. Never expose vLLM directly to the public internet.
8. Avoid recursive chown of a large mounted volume at every startup.
9. Test restart, checkpoint persistence, cancellation, and shutdown.
10. Record region, actual rates, image digest, driver, runtime, and provisioning time.

## Framework compatibility
The initial planning baseline was PyTorch 2.7.0 with CUDA 12.8 (cu128). Verify compatibility against the selected RunPod image and current framework support; do not blindly install a host CUDA toolkit. CUDA 13.5 is deferred. Use a tested NVIDIA/PyTorch image and record its immutable digest. Use a compatible vLLM image for inference rather than mixing arbitrary CUDA and framework packages in the API container.

## Cost controls
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
No RunPod Pod or volume has been created by these repository changes. Provisioning requires access to the RunPod account and confirmation of the live cost estimate.
