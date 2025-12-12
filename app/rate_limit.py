"""
Rate Limiting com SlowAPI
Protege a API contra abuso e ataques DDoS

Rate Limiting = limitar quantidade de requisicoes por tempo
Exemplo: 30 requisicoes por minuto por IP

Por que usar:

SlowAPI eh baseado no Flask-Limiter, adaptado para FastAPI
"""
import os

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

from app.logging_config import logger
from app.metrics import RATE_LIMIT_EXCEEDED


# =============================================================================
# CONFIGURACAO DO LIMITER
# =============================================================================

# Funcao que identifica o cliente (por IP)
# Em producao, pode usar header X-Forwarded-For se estiver atras de proxy
def get_client_identifier(request: Request) -> str:
    """
    Retorna identificador unico do cliente para rate limiting.
    
    Usa o IP do cliente. Em producao atras de load balancer,
    considere usar X-Forwarded-For header.
    """
    # Se estiver atras de proxy (Render, AWS, etc), pega IP real
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)


# Limites padrão (podem ser sobrescritos por endpoint)
# Formato: "X per Y" onde Y pode ser: second, minute, hour, day
DEFAULT_RATE_LIMIT = os.getenv("RATE_LIMIT_DEFAULT", "60/minute")
PREDICT_RATE_LIMIT = os.getenv("RATE_LIMIT_PREDICT", "30/minute")
BATCH_RATE_LIMIT = os.getenv("RATE_LIMIT_BATCH", "10/minute")
LOGIN_RATE_LIMIT = os.getenv("RATE_LIMIT_LOGIN", "10/minute")

# Cria o limiter
limiter = Limiter(
    key_func=get_client_identifier,
    default_limits=[DEFAULT_RATE_LIMIT],
    storage_uri="memory://",  # Em producao, use Redis para multiplas instancias
)


# =============================================================================
# HANDLER DE ERRO CUSTOMIZADO
# =============================================================================

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """
    Handler customizado quando rate limit eh excedido.
    
    Retorna JSON amigavel em vez de texto puro.
    Tambem loga e incrementa metrica Prometheus.
    """
    client_ip = get_client_identifier(request)
    endpoint = request.url.path
    
    # Log estruturado
    logger.warning(
        "rate_limit_exceeded",
        extra={
            "client_ip": client_ip,
            "endpoint": endpoint,
            "limit": str(exc.detail),
        }
    )
    
    # Metrica Prometheus
    RATE_LIMIT_EXCEEDED.labels(endpoint=endpoint, client_ip=client_ip).inc()
    
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "message": f"Muitas requisicoes. Limite: {exc.detail}",
            "retry_after_seconds": 60,  # Sugestao de quando tentar novamente
        },
        headers={"Retry-After": "60"}
    )
