from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from time import monotonic


@dataclass(frozen=True, slots=True)
class MetricsSnapshot:
    requests_total: int
    errors_total: int
    security_blocks_total: int
    total_latency_ms: float

    @property
    def average_latency_ms(self) -> float:
        if self.requests_total == 0:
            return 0.0
        return self.total_latency_ms / self.requests_total


class Metrics:
    """Small dependency-free in-process metrics collector.

    It stores counters and aggregate latency only; request content and secrets are
    intentionally never recorded.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._requests = 0
        self._errors = 0
        self._security_blocks = 0
        self._latency_ms = 0.0

    def observe_request(self, started: float, *, error: bool = False) -> None:
        elapsed_ms = max(0.0, (monotonic() - started) * 1000.0)
        with self._lock:
            self._requests += 1
            self._latency_ms += elapsed_ms
            if error:
                self._errors += 1

    def observe_security_block(self) -> None:
        with self._lock:
            self._security_blocks += 1

    def snapshot(self) -> MetricsSnapshot:
        with self._lock:
            return MetricsSnapshot(
                requests_total=self._requests,
                errors_total=self._errors,
                security_blocks_total=self._security_blocks,
                total_latency_ms=self._latency_ms,
            )

    def reset(self) -> None:
        with self._lock:
            self._requests = 0
            self._errors = 0
            self._security_blocks = 0
            self._latency_ms = 0.0


metrics = Metrics()
