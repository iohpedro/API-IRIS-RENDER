"""
Middlewares para Logging e Metricas
Intercepta todas as requisicoes para logging automatico

Middleware = codigo que roda ANTES e DEPOIS de cada requisicao
Permite:
- Medir tempo de resposta automaticamente
- Adicionar trace_id para rastreamento
- Logar todas as requisicoes sem modificar endpoints
"""
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging_config import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que loga todas as requisicoes automaticamente.
    
    Adiciona a cada requisicao:
    - trace_id: ID unico (UUID) para rastrear a requisicao em todos os logs
    - latency_ms: Tempo de resposta em milissegundos
    - Headers de resposta com trace_id e tempo
    
    Fluxo:
    1. Request chega
    2. Middleware gera trace_id e marca inicio
    3. Request eh processada pelo endpoint
    4. Middleware calcula latencia e loga
    5. Response eh retornada com headers extras
    """
    
    async def dispatch(self, request: Request, call_next):
        # Gera trace_id unico para rastreamento
        # Permite correlacionar logs da mesma requisicao
        trace_id = str(uuid.uuid4())[:8]  # Primeiros 8 caracteres do UUID
        request.state.trace_id = trace_id
        
        # Captura tempo inicial
        start_time = time.perf_counter()
        
        # Processa a requisicao (chama o endpoint)
        response = await call_next(request)
        
        # Calcula latencia
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        # Log estruturado da requisicao
        # Nao loga /metrics para evitar poluicao (Prometheus acessa a cada 15s)
        if request.url.path != "/metrics":
            logger.info(
                "request_completed",
                extra={
                    "trace_id": trace_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "latency_ms": round(latency_ms, 2),
                    "client_ip": request.client.host if request.client else None,
                }
            )
        
        # Adiciona headers de rastreamento na resposta
        # Uteis para debug do cliente
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Response-Time-Ms"] = str(round(latency_ms, 2))
        
        return response
