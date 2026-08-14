import re

INJECTION_PATTERNS = [
    r"ignore (all|any|the|your) previous instructions",
    r"reveal (the )?system prompt",
    r"show me (the )?system prompt",
    r"bypass (security|policy|authorization)",
    r"act as (an? )?(admin|administrator|root)",
    r"retrieve .* confidential",
]

PII_PATTERNS = [
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
    (re.compile(r"\b(?:\d[ -]*?){13,16}\b"), "[REDACTED_ACCOUNT_OR_CARD]"),
    (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[REDACTED_EMAIL]"),
]


def detect_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in INJECTION_PATTERNS)


def redact_pii(text: str) -> str:
    value = text
    for pattern, replacement in PII_PATTERNS:
        value = pattern.sub(replacement, value)
    return value
