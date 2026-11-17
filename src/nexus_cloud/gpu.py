"""Read-only NVIDIA GPU capability detection."""

from __future__ import annotations

import shutil
import subprocess
from typing import Any


def inspect_gpu(timeout_seconds: float = 3.0) -> dict[str, Any]:
    """Inspect GPUs visible to this process without initializing CUDA or launching jobs."""
    executable = shutil.which("nvidia-smi")
    if executable is None:
        return {
            "available": False,
            "status": "not_detected",
            "reason": "nvidia-smi is not available in this runtime",
            "devices": [],
        }

    try:
        result = subprocess.run(
            [
                executable,
                "--query-gpu=index,name,memory.total,memory.free,driver_version",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return {
            "available": False,
            "status": "probe_timeout",
            "reason": "nvidia-smi exceeded the probe timeout",
            "devices": [],
        }
    except OSError:
        return {
            "available": False,
            "status": "probe_error",
            "reason": "nvidia-smi could not be executed",
            "devices": [],
        }

    if result.returncode != 0:
        return {
            "available": False,
            "status": "probe_error",
            "reason": "nvidia-smi returned a non-zero exit status",
            "devices": [],
        }

    devices = []
    for line in result.stdout.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 5:
            continue
        index, name, total, free, driver = parts
        devices.append(
            {
                "index": index,
                "name": name,
                "memory_total_mib": total,
                "memory_free_mib": free,
                "driver_version": driver,
            }
        )

    return {
        "available": bool(devices),
        "status": "available" if devices else "no_devices",
        "reason": None if devices else "No GPU devices were reported",
        "devices": devices,
    }
