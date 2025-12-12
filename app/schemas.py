"""
Schemas (Pydantic models) da API Iris v2.

Separar schemas do main.py deixa o arquivo principal focado em
configurar a aplicacao e facilita reutilizacao/testes.
"""
from typing import List

from pydantic import BaseModel, Field


# --- Autenticacao ---
class LoginRequest(BaseModel):
    """Credenciais de login."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Resposta do login com token JWT."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


# --- Predicao Individual ---
class IrisRequest(BaseModel):
    """Dados de uma flor Iris para predicao."""

    sepal_length: float = Field(..., ge=0, le=10, description="Comprimento da sepala (cm)")
    sepal_width: float = Field(..., ge=0, le=10, description="Largura da sepala (cm)")
    petal_length: float = Field(..., ge=0, le=10, description="Comprimento da petala (cm)")
    petal_width: float = Field(..., ge=0, le=10, description="Largura da petala (cm)")

    class Config:
        json_schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        }


class IrisResponse(BaseModel):
    """Resposta de predicao individual."""

    sucesso: bool
    classe: str
    probabilidades: dict
    usuario: str


# --- Predicao em Lote ---
class BatchPredictRequest(BaseModel):
    """
    Request para predicao em lote.
    Permite processar multiplas flores de uma vez.
    """

    items: List[IrisRequest] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Lista de flores para predizer (max 100)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "sepal_length": 5.1,
                        "sepal_width": 3.5,
                        "petal_length": 1.4,
                        "petal_width": 0.2,
                    },
                    {
                        "sepal_length": 7.0,
                        "sepal_width": 3.2,
                        "petal_length": 4.7,
                        "petal_width": 1.4,
                    },
                    {
                        "sepal_length": 6.3,
                        "sepal_width": 3.3,
                        "petal_length": 6.0,
                        "petal_width": 2.5,
                    },
                ]
            }
        }


class BatchPredictItem(BaseModel):
    """Resultado de uma predicao no lote."""

    indice: int
    classe: str
    confianca: float
    probabilidades: dict


class BatchPredictResponse(BaseModel):
    """Resposta de predicao em lote."""

    sucesso: bool
    total: int
    tempo_total_ms: float
    predicoes: List[BatchPredictItem]
    usuario: str

