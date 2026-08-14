# Architecture

## Trust boundaries

The API layer is the first trust boundary. Requests are authenticated before case data is loaded. The investigation orchestrator separates deterministic risk logic from generative analysis. Policy retrieval and model invocation are independent components so each can be tested and replaced.

The model never receives database credentials, IAM credentials, raw secrets, or authority to mutate case disposition.

## Request path

1. Authenticate caller.
2. Validate request schema.
3. Screen analyst-supplied text for prompt-injection indicators.
4. Load case and transaction evidence.
5. Compute deterministic risk indicators.
6. Retrieve policy passages constrained by metadata.
7. Redact PII from model-bound context.
8. Invoke model provider.
9. Validate structured output and source references.
10. Persist investigation artifact and audit record.
11. Await human disposition.

## Failure behavior

If policy retrieval returns no evidence, the system does not pretend policy support exists. If the provider fails, the case remains reviewable from deterministic evidence. If validation fails, generated content is not promoted to an analyst-ready result.
