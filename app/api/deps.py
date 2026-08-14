from fastapi import Header, HTTPException
from app.core.config import get_settings


def analyst_identity(x_api_key: str = Header(default=""), x_analyst: str = Header(default="demo.analyst")) -> str:
    settings = get_settings()
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_analyst
