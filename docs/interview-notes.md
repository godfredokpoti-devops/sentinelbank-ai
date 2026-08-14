# Engineering Notes for Interviews

## Why not let the LLM assign the final case disposition?
Because a generative model is probabilistic and its output can be affected by prompt injection, retrieval errors, provider changes, or incomplete context. SentinelBank AI keeps consequential state changes behind a separate authenticated analyst endpoint.

## Why keep deterministic risk logic next to the LLM?
It separates measurable transaction signals from natural-language reasoning. An analyst can inspect the score inputs even when the model is unavailable.

## Why use local TF-IDF retrieval in development?
It makes the repository reproducible without paid infrastructure. The retriever is isolated behind a component boundary so production deployments can move to OpenSearch or another managed vector/hybrid search system.

## What would I change for a real bank?
Enterprise SSO, fine-grained entitlement checks before retrieval, private network endpoints, dedicated security accounts, immutable audit storage, managed secrets, formal model validation, production-grade PII detection, data-loss prevention, red-team testing, approved model inventory, kill-switch/runbook processes, and independent compliance/security review.
