# SentinelBank AI

A governed Generative AI investigation platform for banking risk, AML/KYC, and transaction-review workflows.

I built this project to explore a practical question: **how can a bank use generative AI to help investigators without allowing the model to become the decision maker?**

The application combines deterministic risk signals, policy-grounded retrieval, structured LLM analysis, human review, and audit logging. It uses synthetic banking data only.

## Why this project exists

A useful banking GenAI system needs more than a prompt and a model endpoint. It must control what data can be retrieved, keep sensitive fields out of inappropriate contexts, explain where policy statements came from, survive model-provider changes, support analyst review, and leave an audit trail.

SentinelBank AI therefore treats the LLM as an **investigation copilot**, not a system of record and not an autonomous enforcement engine.

## What it does

- Creates and reviews synthetic AML/transaction-risk cases.
- Computes deterministic transaction-risk signals.
- Retrieves relevant AML/KYC policy passages from an approved knowledge base.
- Produces structured investigation summaries with source citations.
- Detects obvious prompt-injection patterns before model invocation.
- Redacts common PII patterns from model-bound text.
- Requires analyst review for case disposition.
- Records model, evidence, request metadata, and analyst action in an audit log.
- Exposes health and operational metrics suitable for containerized deployment.
- Includes evaluation hooks for retrieval, groundedness, citation quality, safety, and regression testing.

## Architecture

```text
Analyst / Client
      |
      v
 FastAPI API
      |
      +--> Auth / role guard
      +--> Input validation
      +--> PII redaction
      +--> Prompt-injection checks
      |
      v
 Investigation Orchestrator
      |
      +--> Risk Engine --------> deterministic signals
      |
      +--> RAG Retriever ------> approved policy corpus
      |
      +--> Model Provider -----> local deterministic provider by default
      |                          Bedrock adapter supported by configuration
      |
      +--> Output Validator ---> citations / schema / safety
      |
      v
 Human Review
      |
      v
 Audit Log + Case State
```

## Important design decisions

### 1. The model does not decide whether to block a customer
The generated analysis is advisory. Final case disposition is stored only through the analyst-review endpoint.

### 2. Local mode works without cloud credentials
The default `local` model provider generates deterministic evidence-based summaries. This keeps development and CI reproducible. A Bedrock adapter can be enabled with environment variables.

### 3. Retrieval is authorization-aware by design
Policy documents contain classification and jurisdiction metadata. Retrieval filters can be extended to enforce user entitlements before context assembly.

### 4. Synthetic data only
No real banking customer data is included or required.

## Technology

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL in production / SQLite for local development
- Pydantic
- scikit-learn TF-IDF retrieval for local reproducibility
- Amazon Bedrock adapter
- Docker / Docker Compose
- Kubernetes manifests
- Terraform AWS scaffolding for VPC, EKS, RDS, S3, ECR, KMS, IAM
- GitHub Actions
- Prometheus-compatible metrics

## Run locally

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/seed.py
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

Run tests:

```bash
pytest -q
```

Docker:

```bash
docker compose up --build
```

## Useful API flow

1. `GET /api/v1/cases`
2. `GET /api/v1/cases/CASE-1001`
3. `POST /api/v1/cases/CASE-1001/investigate`
4. `POST /api/v1/cases/CASE-1001/review`
5. `GET /api/v1/audit?case_id=CASE-1001`

Example investigation request:

```json
{
  "analyst_question": "Summarize the material risk indicators and relevant policy evidence.",
  "jurisdiction": "US"
}
```

Example review request:

```json
{
  "decision": "ESCALATE",
  "reason": "Transaction velocity and new-beneficiary activity require enhanced review."
}
```

## Repository layout

```text
app/                 application code
  api/               HTTP routes
  core/              configuration and logging
  db/                database setup
  models/            SQLAlchemy entities
  schemas/           API contracts
  services/          orchestration, case and audit logic
  rag/               policy retrieval
  security/          PII and prompt-injection controls
  evaluation/        evaluation utilities
data/                 synthetic cases and policy documents
docs/                 architecture, governance and threat model
infra/                Terraform and Kubernetes deployment assets
monitoring/           metrics notes and alert examples
tests/                unit and API tests
scripts/              setup and evaluation scripts
```

## Evaluation philosophy

The repository does not advertise fabricated accuracy metrics. Evaluation scripts generate measurements from the checked-in synthetic golden set. The goal is to make quality regressions visible before deployment.

Tracked categories:

- retrieval hit rate
- citation presence
- policy-grounded response rate
- safety-control pass rate
- schema validity
- latency

## Security posture

This is a portfolio/reference implementation, not production banking software. Production adoption would require organization-specific identity integration, entitlement-aware retrieval, formal model validation, legal/compliance review, hardened network controls, secrets rotation, data-retention controls, red-team testing, vendor-risk review, incident playbooks, and independent security assessment.

See [SECURITY.md](SECURITY.md), [docs/threat-model.md](docs/threat-model.md), and [docs/model-governance.md](docs/model-governance.md).

## License

MIT. See [LICENSE](LICENSE).
