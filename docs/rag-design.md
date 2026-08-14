# RAG Design

The local implementation uses TF-IDF retrieval to stay deterministic and runnable without external services. Policy chunks include document ID, section, jurisdiction, classification, version, and effective date.

A production AWS deployment can replace the local retriever with OpenSearch or a managed knowledge-base layer while preserving the `Retriever` interface.

Retrieval quality is evaluated separately from generation quality. A fluent answer with incorrect evidence is considered a failure.
