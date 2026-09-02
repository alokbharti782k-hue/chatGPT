# Streaming Phase Roadmap

1. Keep the existing authenticated `/api` boundary.
2. Validate and threat-assess the complete user message before generation.
3. Add provider-native async streaming behind the provider-neutral `StreamingLLM` contract.
4. Stream only generated text fragments; never stream secrets, tool credentials, or raw internal state.
5. Support client cancellation and provider timeout/cancellation propagation.
6. Persist the final assistant response only after successful completion; represent cancellation/failure explicitly.
7. Add end-to-end API tests before enabling streaming by default.
