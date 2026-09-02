from backend.security.auth import authenticate_request
from backend.security.file_guard import validate_document_bytes


def test_authentication_is_optional_without_configured_key():
    assert authenticate_request(None, None) is True


def test_authentication_requires_matching_bearer_key():
    assert authenticate_request("Bearer good-key", "good-key") is True
    assert authenticate_request("Bearer bad-key", "good-key") is False
    assert authenticate_request(None, "good-key") is False


def test_document_guard_accepts_utf8_text():
    validate_document_bytes("# safe\ntext".encode("utf-8"))


def test_document_guard_rejects_binary_content():
    try:
        validate_document_bytes(b"safe\x00payload")
    except ValueError:
        return
    raise AssertionError("binary content should be rejected")


def test_document_guard_rejects_invalid_utf8():
    try:
        validate_document_bytes(b"\xff\xfe")
    except ValueError:
        return
    raise AssertionError("invalid UTF-8 should be rejected")
