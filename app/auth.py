"""
Modulo de Autenticacao JWT
Funcoes para criar e validar tokens JWT
"""
import os
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# =============================================================================
# CONFIGURACOES
# =============================================================================
def _get_env(*names: str, default: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value is None:
            continue

        cleaned = value.strip()
        if not cleaned:
            continue

        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
            cleaned = cleaned[1:-1].strip()

        if cleaned:
            return cleaned

    return default


SECRET_KEY = _get_env("JWT_SECRET", "SECRET_KEY", default="dev-secret-change-in-production")
ALGORITHM = _get_env("ALGORITHM", default="HS256")
try:
    TOKEN_EXPIRE_MINUTES = int(
        _get_env("TOKEN_EXPIRE_MINUTES", "ACCESS_TOKEN_EXPIRE_MINUTES", default="30")
    )
except ValueError:
    TOKEN_EXPIRE_MINUTES = 30

# Usuarios (em producao, use banco de dados!)
USERS_DB = {
    "admin": {
        "password": _get_env("ADMIN_PASSWORD", "DEMO_PASSWORD", default="admin123"),
        "role": "admin",
    },
    "user": {
        "password": _get_env("USER_PASSWORD", default="user123"),
        "role": "user",
    },
}


# =============================================================================
# SEGURANCA
# =============================================================================
security = HTTPBearer()


def create_token(username: str, role: str) -> str:
    """Cria um token JWT com expiracao."""
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Valida o token JWT e retorna o usuario."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"], "role": payload["role"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido")


def authenticate_user(username: str, password: str) -> dict | None:
    """Verifica credenciais do usuario."""
    user = USERS_DB.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None
