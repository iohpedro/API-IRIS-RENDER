"""
Metricas Customizadas com Prometheus
Define contadores, histogramas e gauges para monitoramento

Prometheus coleta metricas numericas que permitem:
- Monitorar performance em tempo real
- Criar alertas automaticos
- Visualizar dashboards no Grafana

Tipos de metricas:
- Counter: So aumenta (total de requisicoes, erros)
- Histogram: Distribuicao de valores (latencia, tamanho)
- Gauge: Sobe e desce (usuarios ativos, memoria)
"""
from prometheus_client import Counter, Histogram, Gauge


# =============================================================================
# CONTADORES (Counter)
# Somam eventos que so aumentam (nunca diminuem)
# Uteis para: total de requisicoes, erros, logins
# =============================================================================

# Total de predicoes realizadas
# Labels permitem filtrar por classe e usuario
PREDICTIONS_TOTAL = Counter(
    'iris_predictions_total',
    'Total de predicoes realizadas',
    ['classe', 'user']  # Labels para filtrar no Prometheus/Grafana
)
# Exemplo: PREDICTIONS_TOTAL.labels(classe="setosa", user="admin").inc()

# Predicoes em lote (batch)
BATCH_PREDICTIONS_TOTAL = Counter(
    'iris_batch_predictions_total',
    'Total de predicoes em lote',
    ['user', 'batch_size']
)

# Tentativas de login (sucesso/falha)
LOGIN_ATTEMPTS = Counter(
    'login_attempts_total',
    'Total de tentativas de login',
    ['status']  # success ou failed
)
# Exemplo: LOGIN_ATTEMPTS.labels(status="success").inc()

# Erros por tipo
ERRORS_TOTAL = Counter(
    'api_errors_total',
    'Total de erros',
    ['endpoint', 'error_type']
)

# Rate limit excedido
RATE_LIMIT_EXCEEDED = Counter(
    'rate_limit_exceeded_total',
    'Total de requisicoes bloqueadas por rate limit',
    ['endpoint', 'client_ip']
)


# =============================================================================
# HISTOGRAMAS (Histogram)
# Distribuicao de valores (ex: latencia)
# Permite calcular percentis (p50, p95, p99)
# =============================================================================

# Latencia das predicoes individuais
PREDICTION_LATENCY = Histogram(
    'iris_prediction_latency_seconds',
    'Latencia das predicoes em segundos',
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)
# Exemplo: PREDICTION_LATENCY.observe(0.045)  # 45ms

# Latencia das predicoes em lote
BATCH_PREDICTION_LATENCY = Histogram(
    'iris_batch_prediction_latency_seconds',
    'Latencia das predicoes em lote',
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Latencia geral das requisicoes HTTP
REQUEST_LATENCY = Histogram(
    'http_request_latency_seconds',
    'Latencia das requisicoes HTTP',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)


# =============================================================================
# GAUGES (Gauge)
# Valores que podem subir e descer (estado atual)
# Uteis para: usuarios ativos, memoria, status
# =============================================================================

# Modelo carregado? (1 = sim, 0 = nao)
MODEL_LOADED = Gauge(
    'model_loaded',
    'Indica se o modelo esta carregado (1) ou nao (0)'
)
# Exemplo: MODEL_LOADED.set(1)

# Confianca media das ultimas predicoes
AVG_CONFIDENCE = Gauge(
    'prediction_avg_confidence',
    'Confianca media das ultimas predicoes'
)
