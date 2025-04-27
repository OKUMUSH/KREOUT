from fastapi import Request, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
import os

# Set your API token in the environment variable 'KREOUT_API_TOKEN' for security
API_TOKEN = os.getenv("KREOUT_API_TOKEN", "changeme")

api_key_header = APIKeyHeader(name="X-API-Token", auto_error=False)

async def verify_token(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API token",
        )
