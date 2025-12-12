# 🚀 API de Inferência de Modelos ML v2 - Projeto Final

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Render](https://img.shields.io/badge/Deploy-Render-purple.svg)](https://render.com)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Features v2](#features-v2)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação Local](#instalação-local)
- [Deploy no Render](#deploy-no-render)
- [Endpoints](#endpoints)
- [Autenticação](#autenticação)
- [Rate Limiting](#rate-limiting)
- [Métricas e Monitoramento](#métricas-e-monitoramento)
- [Testes](#testes)

---

## 📖 Sobre o Projeto

Este é o **Projeto Final** do curso de APIs para Inferência de Modelos de Machine Learning. 

A API v2 evolui a versão básica (aula_06) adicionando:
- 🛡️ **Rate Limiting** para proteção contra abuso
- 📊 **Métricas Prometheus** para observabilidade
- 📝 **Logs Estruturados (JSON)** para análise
- 🔄 **Batch Prediction** para processamento em lote
- 🐳 **Stack completa** com Docker Compose (API + Prometheus + Grafana)

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENTES                                    │
│                    (Web Apps, Mobile, Scripts)                          │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   CORS      │  │   Logging   │  │    Rate     │  │   JWT       │    │
│  │  Middleware │→ │  Middleware │→ │   Limiter   │→ │   Auth      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         ENDPOINTS                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   /login    │  │  /predict   │  │  /predict/  │  │   /model/   │    │
│  │    POST     │  │    POST     │  │    batch    │  │    info     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      ML MODEL (Scikit-learn)                            │
│                       🌸 Iris Classifier                                 │
│                    (Random Forest / Logistic)                           │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       OBSERVABILIDADE                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │ Prometheus  │  │   Grafana   │  │    Logs     │                     │
│  │  :9090      │→ │   :3000     │  │   (JSON)    │                     │
│  └─────────────┘  └─────────────┘  └─────────────┘                     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features v2

| Feature | v1 (aula_06) | v2 (aula_08) |
|---------|:------------:|:------------:|
| FastAPI + JWT Auth | ✅ | ✅ |
| Docker + Render Deploy | ✅ | ✅ |
| Rate Limiting | ❌ | ✅ |
| Logs Estruturados (JSON) | ❌ | ✅ |
| Métricas Prometheus | ❌ | ✅ |
| Alertas Configurados | ❌ | ✅ |
| Batch Prediction | ❌ | ✅ |
| Dashboard Grafana | ❌ | ✅ |
| Trace ID por Request | ❌ | ✅ |

---

## 📁 Estrutura do Projeto

```
aula_08/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI bootstrap + routers
│   ├── core.py               # Configs globais (versão, settings)
│   ├── schemas.py            # Modelos Pydantic (request/response)
│   ├── model_loader.py       # Carrega modelo ML + labels
│   ├── auth.py               # JWT authentication
│   ├── logging_config.py     # Logs estruturados JSON
│   ├── middleware.py         # LoggingMiddleware + trace_id
│   ├── metrics.py            # Métricas Prometheus customizadas
│   ├── rate_limit.py         # Configuração slowapi
│   ├── models/
│   │   ├── __init__.py
│   │   └── iris_model.pkl    # Modelo treinado
│   └── routers/
│       ├── __init__.py
│       ├── auth.py           # Rotas: /login, /me
│       ├── info.py           # Rotas: /, /health, /model/info
│       └── predict.py        # Rotas: /predict, /predict/batch
├── prometheus/
│   ├── prometheus.yml        # Configuração do Prometheus
│   └── alerts.yml            # Regras de alertas
├── docker-compose.yml        # Stack local (API + Prometheus + Grafana)
├── Dockerfile                # Build da imagem
├── render.yaml               # Blueprint para Render
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

---

## 🔧 Instalação Local

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Git

### Opção 1: Desenvolvimento Local (Python)

```bash
# Clone o repositório
git clone https://github.com/iohpedro/API-INFERENCIA-MODELOS.git
cd API-INFERENCIA-MODELOS/aula_08

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Execute a API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opção 2: Docker Compose (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/iohpedro/API-INFERENCIA-MODELOS.git
cd API-INFERENCIA-MODELOS/aula_08

# Suba toda a stack
docker-compose up --build

# Acesse:
# - API:        http://localhost:8000
# - Docs:       http://localhost:8000/docs
# - Prometheus: http://localhost:9090
# - Grafana:    http://localhost:3000 (admin/admin)
```

---

## ☁️ Deploy no Render

Nesta versão, você pode subir **a mesma stack do docker-compose** no Render, mas em **serviços separados** (cada um com sua própria URL):

- **API**: `https://api-iris-v2.onrender.com`
- **Prometheus**: `https://prometheus-iris-v2.onrender.com`
- **Grafana**: `https://grafana-iris-v2.onrender.com`

> Observação: no Render não existe `docker-compose up`. O equivalente é criar múltiplos **Web Services** (um por container) — manualmente ou via Blueprint (`render.yaml`).

### Método 1: Blueprint (Automático)

1. Faça fork do repositório no GitHub
2. Acesse [render.com](https://render.com) e faça login
3. Vá em **Blueprints** → **New Blueprint Instance**
4. Conecte seu repositório
5. Selecione o arquivo `aula_08/render.yaml`
6. O Render criará **3 serviços** automaticamente (API + Prometheus + Grafana)

Após subir:
- Prometheus já vem configurado para fazer scrape da API em `/metrics`.
- Grafana já vem com datasource do Prometheus provisionado.

### Método 2: Deploy Manual

1. Acesse [render.com](https://render.com)
2. **New** → **Web Service**
3. Conecte o repositório GitHub
4. Crie **3 Web Services**:

**Serviço 1 — API**
- **Name**: `api-iris-v2`
- **Root Directory**: `aula_08`
- **Runtime**: Docker
- **Dockerfile Path**: `aula_08/Dockerfile`

**Serviço 2 — Prometheus**
- **Name**: `prometheus-iris-v2`
- **Root Directory**: `aula_08/prometheus`
- **Runtime**: Docker
- **Dockerfile Path**: `aula_08/prometheus/Dockerfile`
- **Env Vars**:
  - `API_TARGET=api-iris-v2.onrender.com`
  - `API_SCHEME=https`
  - `SCRAPE_INTERVAL=15s`

**Serviço 3 — Grafana**
- **Name**: `grafana-iris-v2`
- **Root Directory**: `aula_08/grafana`
- **Runtime**: Docker
- **Dockerfile Path**: `aula_08/grafana/Dockerfile`
- **Env Vars**:
  - `GF_SECURITY_ADMIN_USER=admin`
  - `GF_SECURITY_ADMIN_PASSWORD=admin`
  - `GF_USERS_ALLOW_SIGN_UP=false`
  - `PROMETHEUS_URL=https://prometheus-iris-v2.onrender.com`

5. Clique em **Create Web Service** para cada um.

---

## 🔌 Endpoints

### Públicos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc |
| POST | `/login` | Obter token JWT |

### Protegidos (JWT)

| Método | Endpoint | Descrição | Rate Limit |
|--------|----------|-----------|------------|
| POST | `/predict` | Predição individual | 30/min |
| POST | `/predict/batch` | Predição em lote | 10/min |
| GET | `/model/info` | Info do modelo | 60/min |

### Métricas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/metrics` | Métricas Prometheus |

---

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação.

### Obter Token

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret123"}'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Usar Token

```bash
curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

---

## ⏱️ Rate Limiting

A API implementa rate limiting para proteger contra abuso:

| Endpoint | Limite | Janela |
|----------|--------|--------|
| `/login` | 10 | 1 minuto |
| `/predict` | 30 | 1 minuto |
| `/predict/batch` | 10 | 1 minuto |
| Demais | 60 | 1 minuto |

### Resposta quando limite excedido

```json
{
  "error": "Rate limit exceeded",
  "detail": "30 per 1 minute",
  "retry_after": 45
}
```

**Headers incluídos:**
- `X-RateLimit-Limit`: Limite total
- `X-RateLimit-Remaining`: Requisições restantes
- `X-RateLimit-Reset`: Timestamp de reset

---

## 📊 Métricas e Monitoramento

### Métricas Disponíveis

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| `iris_predictions_total` | Counter | Total de predições |
| `iris_batch_predictions_total` | Counter | Total de batches |
| `iris_login_attempts_total` | Counter | Tentativas de login |
| `iris_rate_limit_exceeded_total` | Counter | Rate limits atingidos |
| `iris_prediction_latency_seconds` | Histogram | Latência de predição |
| `iris_batch_prediction_latency_seconds` | Histogram | Latência de batch |
| `iris_model_loaded` | Gauge | Status do modelo |
| `iris_avg_confidence` | Gauge | Confiança média |

### Alertas Configurados

1. **APIDown**: API não respondendo por 1 minuto
2. **HighErrorRate**: Taxa de erro > 5% por 5 minutos
3. **HighLatency**: P95 latência > 1s por 5 minutos
4. **ModelNotLoaded**: Modelo não carregado
5. **HighRateLimitBlocks**: > 100 bloqueios/5min

### Acessando Grafana

1. Acesse `http://localhost:3000`
2. Login: `admin` / `admin`
3. Adicione Data Source → Prometheus → URL: `http://prometheus:9090`
4. Importe ou crie dashboards

---

## 🧪 Testes

### Teste de Predição Individual

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret123"}' | jq -r '.access_token')

# Predição
curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

### Teste de Batch Prediction

```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
      {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4},
      {"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 6.0, "petal_width": 2.5}
    ]
  }'
```

### Teste de Rate Limiting

```bash
# Execute múltiplas requisições rapidamente
for i in {1..35}; do
  echo "Request $i:"
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:8000/predict \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
done
# Após 30 requisições, você verá 429 (Too Many Requests)
```

---

## 📝 Variáveis de Ambiente

| Variável | Descrição | Default |
|----------|-----------|---------|
| `SECRET_KEY` | Chave para JWT | `dev-secret-key` |
| `ALGORITHM` | Algoritmo JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração token | `30` |
| `RATE_LIMIT_DEFAULT` | Limite padrão/min | `60` |
| `RATE_LIMIT_PREDICT` | Limite predict/min | `30` |
| `RATE_LIMIT_BATCH` | Limite batch/min | `10` |
| `RATE_LIMIT_LOGIN` | Limite login/min | `10` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `MODEL_VERSION` | Versão do modelo | `2.0.0` |

---

## 🤝 Contribuindo

1. Faça fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é parte do curso de APIs para ML e está disponível para fins educacionais.

---

## 👨‍🏫 Autor
Professor Ioannis Eleftheriou -  https://www.linkedin.com/in/ioannispedroeleftheriou/  

Desenvolvido como material didático para o curso de **APIs para Inferência de Modelos de Machine Learning**.

---

<p align="center">
  <strong>🎓 Aula 08 - Projeto Final</strong><br>
  Evoluindo uma API de ML para Produção
</p>
