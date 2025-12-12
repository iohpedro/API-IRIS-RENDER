"""
Rotas de autenticacao JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth import (
    TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_token,
    get_current_user,
)
from app.core import logger
from app.metrics import LOGIN_ATTEMPTS
from app.rate_limit import LOGIN_RATE_LIMIT, limiter
from app.schemas import LoginRequest, TokenResponse


router = APIRouter(tags=["Autenticacao"])


@router.post("/login", response_model=TokenResponse)
@limiter.limit(LOGIN_RATE_LIMIT)
def login(request: Request, credentials: LoginRequest):
    """
    Faz login e retorna token JWT.

    **Rate Limit:** 10 requisicoes por minuto

    Usuarios disponiveis:
    - admin / admin123 (role: admin)
    - user / user123 (role: user)
    """
    user = authenticate_user(credentials.username, credentials.password)
    trace_id = getattr(request.state, "trace_id", "N/A")

    if not user:
        LOGIN_ATTEMPTS.labels(status="failed").inc()
        logger.warning(
            "login_failed",
            extra={"username": credentials.username, "trace_id": trace_id},
        )
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")

    LOGIN_ATTEMPTS.labels(status="success").inc()
    token = create_token(user["username"], user["role"])

    logger.info(
        "login_success",
        extra={
            "username": user["username"],
            "role": user["role"],
            "trace_id": trace_id,
        },
    )

    return TokenResponse(access_token=token, expires_in=TOKEN_EXPIRE_MINUTES * 60)


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Retorna informacoes do usuario logado."""
    return current_user

