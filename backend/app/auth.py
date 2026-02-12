"""
Authentication & Security Middleware.
Handles JWT verification for staff, API keys for widgets, and webhook signature validation.
"""

import hmac
import hashlib
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
import structlog

from app.config import get_settings

settings = get_settings()
logger = structlog.get_logger()

# OAuth2 scheme for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# API Key header for widget
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_jwt(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verify JWT access token for staff/admin routes.
    Returns the decoded token payload (claims).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


async def verify_api_key(
    request: Request,
    api_key: Optional[str] = Depends(api_key_header)
) -> Optional[str]:
    """
    Verify API Key for widget access availability.
    Note: For public widget endpoints, we might allow access without key 
    if the property_id is valid, but strict mode requires key.
    For this MVP/Pilot, we just pass it through or validate if present.
    """
    # TODO: Implement strict API key validation against DB if needed.
    # For now, this is a placeholder dependency.
    return api_key


async def verify_whatsapp_signature(request: Request):
    """
    Verify WhatsApp Cloud API webhook signature (X-Hub-Signature-256).
    Prevents forged requests from attackers.
    """
    if not settings.whatsapp_app_secret:
        # Warn but allow if secret not configured (dev mode helper)
        if settings.is_production:
            logger.error("WhatsApp secret not configured in production!")
            raise HTTPException(status_code=500, detail="Server misconfiguration")
        return

    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        logger.warning("Missing WhatsApp signature")
        raise HTTPException(status_code=403, detail="Missing signature")

    # Signature format: "sha256=<hash>"
    if not signature.startswith("sha256="):
        raise HTTPException(status_code=403, detail="Invalid signature format")
        
    sig_hash = signature.split("=")[1]
    
    # Read raw body
    body = await request.body()
    
    # Calculate expected HMAC
    expected_hash = hmac.new(
        settings.whatsapp_app_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(sig_hash, expected_hash):
        logger.warning("Invalid WhatsApp signature", signature=signature)
        raise HTTPException(status_code=403, detail="Invalid signature")

