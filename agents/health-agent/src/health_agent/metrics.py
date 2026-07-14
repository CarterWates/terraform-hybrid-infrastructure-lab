"""System metric collection with best-effort failure isolation."""

from __future__ import annotations

import os
import platform
import shutil
import time
from collections.abc import Callable
from typing import Any


def collect_system_metrics() -> dict[str, Any]:
    """Collect host metrics without letting one failed metric abort the payload."""

    return {
        "hostname": _safe_value(_hostname),
        "cpuPercent": _safe_value(_cpu_percent),
        "memoryPercent": _safe_value(_memory_percent),
        "diskPercent": _safe_value(_disk_percent),
        "uptimeSeconds": _safe_value(_uptime_seconds),
    }


def _safe_value(func: Callable[[], Any]) -> Any:
    try:
        return func()
    except Exception:
        return None


def _hostname() -> str:
    return platform.node() or "unknown-host"


def _cpu_percent() -> float | None:
    load_average = getattr(os, "getloadavg", None)
    if load_average is None:
        return None

    one_minute_load = load_average()[0]
    cpu_count = os.cpu_count() or 1
    return round(min((one_minute_load / cpu_count) * 100, 100.0), 2)


def _memory_percent() -> float | None:
    if platform.system() == "Darwin":
        return None

    meminfo = _read_meminfo()
    total = meminfo.get("MemTotal")
    available = meminfo.get("MemAvailable")
    if not total or available is None:
        return None

    return round((1 - (available / total)) * 100, 2)


def _read_meminfo() -> dict[str, int]:
    result: dict[str, int] = {}
    with open("/proc/meminfo", encoding="utf-8") as meminfo:
        for line in meminfo:
            key, raw_value = line.split(":", 1)
            parts = raw_value.strip().split()
            if parts:
                result[key] = int(parts[0])
    return result


def _disk_percent() -> float:
    usage = shutil.disk_usage("/")
    return round((usage.used / usage.total) * 100, 2)


def _uptime_seconds() -> int | None:
    if platform.system() == "Darwin":
        return None

    with open("/proc/uptime", encoding="utf-8") as uptime:
        return int(float(uptime.read().split()[0]))


def utc_timestamp() -> str:
    """Return a UTC timestamp formatted for JSON payloads."""

    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
