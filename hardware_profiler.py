# hardware_profiler.py
"""Utility to profile device hardware (RAM, CPU cores, GPU if available).
Provides `DeviceSpecs` dataclass and `detect_specs()` function used by the UI.
"""
import os
from dataclasses import dataclass

try:
    import psutil
except ImportError:
    psutil = None

@dataclass
class DeviceSpecs:
    total_ram_gb: float
    cpu_cores: int
    has_gpu: bool = False

def detect_specs() -> DeviceSpecs:
    """Detect total RAM, CPU core count, and simple GPU presence.
    Falls back to parsing /proc/meminfo if psutil is unavailable.
    """
    if psutil:
        mem = psutil.virtual_memory().total / (1024**3)
        cores = psutil.cpu_count(logical=False) or 0
    else:
        # fallback reading /proc/meminfo
        mem = 0.0
        try:
            with open('/proc/meminfo') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        mem = int(line.split()[1]) / 1024 / 1024
                        break
        except Exception:
            mem = 4.0
        cores = os.cpu_count() or 0
    # Simple GPU detection: check for CUDA lib path (approximation)
    has_gpu = any('cuda' in p.lower() for p in os.listdir('/data/data/com.termux/files/home/.gemini/antigravity-cli/venv/lib') if os.path.isdir(os.path.join('/data/data/com.termux/files/home/.gemini/antigravity-cli/venv/lib', p))) if os.path.isdir('/data/data/com.termux/files/home/.gemini/antigravity-cli/venv/lib') else False
    return DeviceSpecs(total_ram_gb=mem, cpu_cores=cores, has_gpu=has_gpu)
