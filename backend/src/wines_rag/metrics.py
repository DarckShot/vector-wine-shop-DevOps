from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from threading import Lock
from time import perf_counter


@dataclass
class _DurationStat:
    total_seconds: float = 0.0
    count: int = 0


class MetricsRegistry:
    def __init__(self) -> None:
        self._started_at = perf_counter()
        self._requests_total: defaultdict[tuple[str, str, str], int] = defaultdict(int)
        self._duration: defaultdict[tuple[str, str], _DurationStat] = defaultdict(_DurationStat)
        self._lock = Lock()

    def observe_request(self, method: str, path: str, status_code: int, duration_seconds: float) -> None:
        status = str(status_code)
        with self._lock:
            self._requests_total[(method, path, status)] += 1
            duration_bucket = self._duration[(method, path)]
            duration_bucket.count += 1
            duration_bucket.total_seconds += duration_seconds

    def render_prometheus(self) -> str:
        with self._lock:
            request_samples = list(self._requests_total.items())
            duration_samples = list(self._duration.items())

        lines: list[str] = [
            "# HELP backend_uptime_seconds Backend process uptime in seconds.",
            "# TYPE backend_uptime_seconds gauge",
            f"backend_uptime_seconds {max(perf_counter() - self._started_at, 0.0):.6f}",
            "# HELP backend_requests_total Total count of HTTP requests by method, route, and status code.",
            "# TYPE backend_requests_total counter",
        ]

        for (method, path, status), value in sorted(request_samples):
            lines.append(
                f'backend_requests_total{{method="{_esc(method)}",path="{_esc(path)}",status="{_esc(status)}"}} {value}'
            )

        lines.extend(
            [
                "# HELP backend_request_duration_seconds_sum Sum of observed request durations in seconds by method and route.",
                "# TYPE backend_request_duration_seconds_sum counter",
                "# HELP backend_request_duration_seconds_count Count of observed request durations by method and route.",
                "# TYPE backend_request_duration_seconds_count counter",
            ]
        )

        for (method, path), stat in sorted(duration_samples):
            labels = f'method="{_esc(method)}",path="{_esc(path)}"'
            lines.append(f"backend_request_duration_seconds_sum{{{labels}}} {stat.total_seconds:.6f}")
            lines.append(f"backend_request_duration_seconds_count{{{labels}}} {stat.count}")

        return "\n".join(lines) + "\n"


def _esc(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


metrics_registry = MetricsRegistry()
