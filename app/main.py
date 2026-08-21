from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, FileResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from app.api.routes import router
from app.health.routes import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import Base, engine


settings = get_settings()
configure_logging(settings.log_level)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Governed GenAI investigation platform for synthetic banking risk workflows.",
)


app.include_router(router)
app.include_router(health_router)


REQUESTS = Counter(
    "sentinelbank_http_requests_total",
    "HTTP requests",
    ["path", "method"],
)


@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)

    REQUESTS.labels(
        path=request.url.path,
        method=request.method,
    ).inc()

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"

    return response


@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.app_env,
        "model_provider": settings.model_provider,
    }


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return PlainTextResponse(
        generate_latest().decode(),
        media_type=CONTENT_TYPE_LATEST,
    )