# ALICE Services

This package contains provider-neutral boundaries for speech and notifications.

Providers should be injected explicitly. Service modules must not expose secrets or perform side effects merely because an LLM requested them; authorization belongs in the safety/permission layer.
