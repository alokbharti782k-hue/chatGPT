# ALICE Tool Runtime

The tool runtime is the controlled execution boundary between ALICE's reasoning layer and application capabilities.

## Guarantees

- Tools must be explicitly allowlisted when an allowlist is configured.
- Tool names are resolved through `ToolRegistry`; the model cannot supply arbitrary Python callables.
- Each agent run has a maximum step and tool-call budget.
- Each asynchronous tool call has a bounded timeout.
- Tool arguments and returned text pass through the defensive threat-detection/containment layer.
- Existing permission policy remains authoritative; IoT and external tools stay disabled by default.
- A failed tool stops the current execution sequence rather than allowing uncontrolled continuation.
- Uploaded data and tool output are treated as data, not executable instructions.

## Safety boundary

This runtime is intentionally not a shell, code interpreter, autonomous penetration-testing engine, or physical-actuation controller. High-impact capabilities should be exposed only through separately reviewed deterministic services and explicit permission/confirmation policies.

## Typical flow

`Agent plan -> bounded executor -> allowlist -> permission policy -> threat check -> tool -> output threat check -> result -> next step`
