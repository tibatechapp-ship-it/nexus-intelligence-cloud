# Phase 1 cost model

Approved monthly budget envelope: **USD 1,000–1,500**.

## Current public rate snapshot

RunPod's official pricing page, updated **November 12, 2026**, lists the Secure Cloud H200 Pod at **USD 5.29/GPU-hour** with 141GB VRAM, 276GB RAM, and 24 vCPU. The same page lists standard Network Storage under 1TB at **USD 0.07/GB/month**.

| Resource | Plan | Published rate | Monthly estimate |
|---|---:|---:|---:|
| H200 Secure Cloud | 160 GPU-hours | $5.29/hour | **$846.40** |
| Standard Network Volume | 500GB | $0.07/GB/month | **$35.00** |
| **Base subtotal** | | | **$881.40** |

The estimate is a rate-based calculation, not a checkout quote. It excludes any optional container/volume disks, taxes or account-specific adjustments. The GPU rate is billed for actual running time; the persistent Network Volume continues to incur storage charges while retained. Confirm the selected data center, actual availability, billing granularity, and final checkout total before provisioning.

## Budget controls

- Keep the planned GPU runtime at 160 hours/month (about 5.3 hours/day).
- Set a hard owner-approved GPU-hour cap; stop the Pod when the allocated runtime is exhausted.
- Treat USD 1,000 as the operational alert threshold and USD 1,500 as the absolute approved ceiling.
- Preserve at least USD 118.60 of headroom above the base subtotal before optional services and taxes.
- Track GPU compute and persistent storage as separate line items.
- Do not enable automatic GPU scaling or create additional GPUs without explicit approval.

## Sources

- [RunPod official GPU and storage pricing](https://www.runpod.io/pricing) — pricing page updated November 12, 2026.

No RunPod resources are provisioned by this repository. Any change to the approved budget requires explicit approval.
