# Threat Model

## Assets

- customer and transaction information
- internal policy documents
- analyst identities and entitlements
- prompts and generated investigation summaries
- model-provider credentials
- audit history

## Primary threats

### Prompt injection
Untrusted analyst text or retrieved content may attempt to override instructions. Controls: pattern screening, strict context separation, no tool authority in the model, structured output validation, and red-team tests.

### Sensitive-information disclosure
The model could echo unnecessary PII. Controls: minimization/redaction before invocation, response validation, entitlement-aware retrieval, and audit logging.

### Unauthorized retrieval
A user could attempt to retrieve policy content outside their role/jurisdiction. Controls: metadata filters and a production requirement for identity-derived document entitlements.

### Excessive agency
A model could recommend or attempt an action beyond its role. Control: the provider has no direct mutation path; case disposition requires a dedicated human-review endpoint.

### Model/provider failure
A provider can time out, change behavior, or become unavailable. Controls: provider abstraction, deterministic fallback evidence, timeout/retry policy at infrastructure layer, and no dependence on the LLM for core case state.

### Audit tampering
Investigation history may be altered. Portfolio implementation uses append-style records; production design should export security logs to a restricted account/store with immutability controls.
