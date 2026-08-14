# Demo Script

1. Seed the repository and start FastAPI.
2. Open `/docs`.
3. Authenticate using `X-API-Key: dev-analyst-key` and `X-Analyst: godfred.demo`.
4. Retrieve `CASE-1001` and explain the synthetic transaction pattern.
5. Run an investigation and point out deterministic signals, policy citations, provider identity, and `human_review_required=true`.
6. Submit a prompt-injection attempt and show that it is blocked and audited.
7. Submit the human review endpoint and explain why this is the only path that changes case disposition.
8. Show `/audit` and `/metrics`.
9. Run `pytest -q` and `python scripts/evaluate.py`.
10. Explain the production path: private AWS networking, EKS, encrypted RDS/S3, IAM workload identity, Bedrock, centralized logging, formal model validation, and entitlement-aware retrieval.
