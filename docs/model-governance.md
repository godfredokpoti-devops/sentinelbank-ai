# Model Governance

SentinelBank AI treats model behavior as a governed dependency.

## Model inventory

Each generated investigation stores provider, model identifier, timestamp, request correlation ID, and source document identifiers.

## Change control

A provider/model/prompt/retrieval change should pass:

- unit and integration tests
- golden-set retrieval evaluation
- citation checks
- prompt-injection tests
- schema validation
- latency/error review
- human sample review

## Human oversight

The system can summarize evidence and recommend review steps. It cannot autonomously freeze an account, reject a customer, file a regulatory report, or close a case.

## Rollback

Model configuration is externalized. A prior approved provider/model can be restored without changing case records or the API contract.
