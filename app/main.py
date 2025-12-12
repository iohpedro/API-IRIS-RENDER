"""
API Iris v2 - Projeto Final
Versao completa com: JWT, Rate Limiting, Logs Estruturados, Metricas Prometheus, Batch Prediction

Evolucao da aula_06:
- Base: Autenticacao JWT, predicao individual
- Novo: Rate limiting, logs JSON, metricas Prometheus
- Novo: Endpoint /predict/batch para predicao em lote
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

# Prometheus
from prometheus_fastapi_instrumentator import Instrumentator

from app.middleware import LoggingMiddleware
from app.rate_limit import limiter, rate_limit_exceeded_handler
from app.routers import auth, info, predict
from app.core import API_VERSION


# =============================================================================
# APLICACAO FASTAPI
# =============================================================================
app = FastAPI(
    title="API Iris v2 - Projeto Final",
    description="""
## API de Classificacao de Flores Iris

Versao completa com todas as features do curso:

### Features
- 🔐 **Autenticacao JWT** - Login seguro com tokens
- 🚦 **Rate Limiting** - Protecao contra abuso
- 📊 **Metricas Prometheus** - Monitoramento em tempo real
- 📝 **Logs Estruturados** - JSON para observabilidade
- 📦 **Predicao em Lote** - Processe multiplas flores de uma vez

### Endpoints Principais
- `POST /login` - Obter token JWT
- `POST /predict` - Predicao individual
- `POST /predict/batch` - Predicao em lote (NOVO!)
- `GET /metrics` - Metricas Prometheus
- `GET /health` - Health check

### Limites de Requisicao (Rate Limiting)
- `/login`: 10 req/minuto
- `/predict`: 30 req/minuto
- `/predict/batch`: 10 req/minuto
    """,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
)

# Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS (permite requisicoes de outros dominios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em producao, especifique dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Logging (intercepta todas as requisicoes)
app.add_middleware(LoggingMiddleware)

# Instrumentacao Prometheus (adiciona metricas automaticas + endpoint /metrics)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


# =============================================================================
# ROTAS (routers)
# =============================================================================
app.include_router(info.router)
app.include_router(auth.router)
app.include_router(predict.router)
