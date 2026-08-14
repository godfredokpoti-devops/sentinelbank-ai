# Security Policy

SentinelBank AI uses synthetic data and is intended as a reference implementation.

## Security principles

- Treat model output as untrusted input.
- Never let an LLM directly execute a consequential banking action.
- Keep authentication and authorization outside the model.
- Minimize sensitive data before model invocation.
- Retrieve only documents the caller is entitled to access.
- Record security-relevant AI interactions for audit.
- Keep provider credentials in a secret manager, never source control.
- Fail closed when a security control cannot make a safe decision.

## Reporting

Do not submit real customer data, credentials, secrets, or exploitable production information in a public issue. Use a private channel for sensitive reports.
