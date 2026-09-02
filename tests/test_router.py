from backend.core.router import route_message


def test_routes_normal_message_to_chat():
    assert route_message("Hello ALICE").route == "chat"


def test_routes_empty_message_to_invalid():
    assert route_message("   ").route == "invalid"
