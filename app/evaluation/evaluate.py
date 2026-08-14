from app.rag.retriever import LocalPolicyRetriever

GOLDEN = [
    ("new beneficiaries transaction velocity geographic deviation", "AML-POL-001"),
    ("customer profile expected activity enhanced due diligence", "KYC-POL-004"),
    ("AI human review model source evidence", "AI-GOV-002"),
    ("sensitive data minimization least privilege", "DATA-SEC-007"),
]


def run_evaluation() -> dict:
    retriever = LocalPolicyRetriever()
    hits = 0
    for query, expected in GOLDEN:
        docs = retriever.search(query, "US", k=3)
        hits += int(expected in {d.document_id for d in docs})
    return {"retrieval_hit_rate_at_3": hits / len(GOLDEN), "cases": len(GOLDEN)}


if __name__ == "__main__":
    print(run_evaluation())
