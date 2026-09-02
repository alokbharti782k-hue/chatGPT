from backend.security.rate_limit import RateLimiter
from backend.security.redaction import redact_secrets


def test_redacts_common_credentials():
    value = redact_secrets("api_key=abc123 password=hunter2 token=xyz")
    assert "abc123" not in value
    assert "hunter2" not in value
    assert "xyz" not in value
    assert "[REDACTED]" in value


def test_rate_limiter_blocks_after_budget():
    limiter = RateLimiter(limit=2, window_seconds=60)
    assert limiter.allow("client") is True
    assert limiter.allow("client") is True
    assert limiter.allow("client") is False


def test_rate_limiters_are_scoped_by_key():
    limiter = RateLimiter(limit=1, window_seconds=60)
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False
    assert limiter.allow("b") is True
