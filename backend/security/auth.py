from __future__ import annotations

import secrets


def authenticate_request(authorization: str | None, configured_api_key: str | None) -> bool:
    """Validate a bearer API key when authentication is configured.

    Local development remains compatible when no API key is configured.
    """
    if not configured_api_key:
        return True
    if not authorization or not authorization.startswith("Bearer "):
        return False
    presented = authorization.removeprefix("Bearer ").strip()
    return secrets.compare_digest(presented, configured_api_key)
