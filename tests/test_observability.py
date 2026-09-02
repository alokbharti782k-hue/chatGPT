from time import monotonic, sleep

from backend.observability.metrics import Metrics


def test_metrics_track_requests_and_average_latency() -> None:
    metrics = Metrics()
    started = monotonic()
    sleep(0.001)
    metrics.observe_request(started)
    metrics.observe_request(monotonic(), error=True)
    metrics.observe_security_block()

    snapshot = metrics.snapshot()
    assert snapshot.requests_total == 2
    assert snapshot.errors_total == 1
    assert snapshot.security_blocks_total == 1
    assert snapshot.total_latency_ms >= 0
    assert snapshot.average_latency_ms >= 0


def test_metrics_reset() -> None:
    metrics = Metrics()
    metrics.observe_request(monotonic())
    metrics.reset()
    snapshot = metrics.snapshot()
    assert snapshot.requests_total == 0
    assert snapshot.errors_total == 0
    assert snapshot.security_blocks_total == 0
    assert snapshot.total_latency_ms == 0.0
