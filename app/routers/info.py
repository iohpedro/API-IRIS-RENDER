"""
Rotas de informacao/saude da API.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.core import API_VERSION, ENVIRONMENT
from app.model_loader import MODELO_OK, modelo, classes


router = APIRouter(tags=["Info"])


@router.get("/")
def home():
    """Informacoes da API."""
    return {
        "api": "Iris Classifier",
        "versao": API_VERSION,
        "ambiente": ENVIRONMENT,
        "modelo_carregado": MODELO_OK,
        "docs": "/docs",
        "redoc": "/redoc",
        "metrics": "/metrics",
        "health": "/health",
        "endpoints": {
            "login": "POST /login",
            "predict": "POST /predict",
            "predict_batch": "POST /predict/batch",
        },
    }


@router.get("/health")
def health():
    """Health check para monitoramento."""
    return {
        "status": "healthy" if MODELO_OK else "degraded",
        "modelo": MODELO_OK,
        "ambiente": ENVIRONMENT,
        "version": API_VERSION,
    }


@router.get("/model/info")
def model_info(current_user: dict = Depends(get_current_user)):
    """
    Retorna informacoes sobre o modelo carregado.

    Util para debugging e documentacao.
    """
    if not MODELO_OK:
        raise HTTPException(status_code=503, detail="Modelo nao disponivel")

    return {
        "modelo_carregado": True,
        "tipo": type(modelo).__name__,
        "classes": list(classes) if classes else [],
        "n_classes": len(classes) if classes else 0,
        "features_esperadas": [
            "sepal_length",
            "sepal_width",
            "petal_length",
            "petal_width",
        ],
        "versao_api": API_VERSION,
    }
