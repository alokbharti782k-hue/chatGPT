# ALICE Streaming Baseline

ALICE now has a dependency-free async text-streaming primitive that yields bounded chunks and gives the event loop a cancellation point between chunks.

## Safety boundary

This layer does not bypass authentication, validation, threat detection, tool permissions, or deterministic safety controls. It only controls delivery of already-produced text.

## Cancellation

Consumers can stop an async generator with `aclose()` or cancel the consuming task. The implementation deliberately yields control between chunks so cancellation is observable without introducing a new runtime dependency.

## Future provider streaming

The next integration step is to expose provider-native streaming from the LLM interface. That should preserve the same security/orchestration path and must not commit partial assistant messages to persistent memory until the stream completes successfully (or explicitly records a cancelled/failed generation).
