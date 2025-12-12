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
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))

# Usuarios (em producao, use banco de dados!)
USERS_DB = {
    "admin": {"password": os.getenv("ADMIN_PASSWORD", "admin123"), "role": "admin"},
    "user": {"password": os.getenv("USER_PASSWORD", "user123"), "role": "user"},
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
