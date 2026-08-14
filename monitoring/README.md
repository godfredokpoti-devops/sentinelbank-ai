# Monitoring

The API exposes Prometheus metrics at `/metrics` and structured application events through stdout.

Recommended production signals:

- HTTP request/error/latency
- model-provider latency and failures
- retrieval empty-result rate
- prompt-block rate
- investigation schema-validation failures
- analyst review backlog
- token and model cost metrics when a hosted provider is enabled

Suggested SLO starting point for the synchronous analyst API: 99.9% monthly availability excluding approved maintenance, with a separately tracked model-provider dependency SLI.
