"""
Rotas de predicao (individual e em lote).
"""
import time

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth import get_current_user
from app.core import logger
from app.metrics import (
    BATCH_PREDICTION_LATENCY,
    BATCH_PREDICTIONS_TOTAL,
    PREDICTION_LATENCY,
    PREDICTIONS_TOTAL,
)
from app.model_loader import MODELO_OK, classes, modelo
from app.rate_limit import BATCH_RATE_LIMIT, PREDICT_RATE_LIMIT, limiter
from app.schemas import (
    BatchPredictItem,
    BatchPredictRequest,
    BatchPredictResponse,
    IrisRequest,
    IrisResponse,
)


router = APIRouter(tags=["Predicao"])


@router.post("/predict", response_model=IrisResponse)
@limiter.limit(PREDICT_RATE_LIMIT)
def predict(
    request: Request,
    payload: IrisRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Faz predicao para uma unica flor Iris.

    **Rate Limit:** 30 requisicoes por minuto

    **Requer autenticacao:** Inclua o header `Authorization: Bearer <token>`
    """
    if not MODELO_OK:
        raise HTTPException(status_code=503, detail="Modelo nao disponivel")

    trace_id = getattr(request.state, "trace_id", "N/A")
    start = time.perf_counter()

    features = np.array(
        [
            [
                payload.sepal_length,
                payload.sepal_width,
                payload.petal_length,
                payload.petal_width,
            ]
        ]
    )

    pred_idx = modelo.predict(features)[0]
    probs = modelo.predict_proba(features)[0]
    classe = classes[pred_idx]
    confidence = float(max(probs))

    latency = time.perf_counter() - start

    # Metricas
    PREDICTIONS_TOTAL.labels(classe=classe, user=current_user["username"]).inc()
    PREDICTION_LATENCY.observe(latency)

    # Log
    logger.info(
        "prediction_completed",
        extra={
            "trace_id": trace_id,
            "user": current_user["username"],
            "classe": classe,
            "confidence": round(confidence, 4),
            "latency_ms": round(latency * 1000, 2),
        },
    )

    return IrisResponse(
        sucesso=True,
        classe=classe,
        probabilidades={classes[i]: round(float(p), 4) for i, p in enumerate(probs)},
        usuario=current_user["username"],
    )


@router.post("/predict/batch", response_model=BatchPredictResponse)
@limiter.limit(BATCH_RATE_LIMIT)
def predict_batch(
    request: Request,
    payload: BatchPredictRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Faz predicao para multiplas flores Iris de uma vez.

    **Rate Limit:** 10 requisicoes por minuto

    **Maximo:** 100 flores por requisicao

    **Requer autenticacao:** Inclua o header `Authorization: Bearer <token>`

    **Vantagens do Batch:**
    - Mais eficiente que multiplas chamadas individuais
    - Menor overhead de rede
    - Ideal para processamento em massa
    """
    if not MODELO_OK:
        raise HTTPException(status_code=503, detail="Modelo nao disponivel")

    trace_id = getattr(request.state, "trace_id", "N/A")
    start = time.perf_counter()

    # Prepara features de todas as flores
    features_list = [
        [
            item.sepal_length,
            item.sepal_width,
            item.petal_length,
            item.petal_width,
        ]
        for item in payload.items
    ]
    features = np.array(features_list)

    # Predicao em lote (mais eficiente que loop)
    pred_indices = modelo.predict(features)
    all_probs = modelo.predict_proba(features)

    # Monta resposta
    predicoes = []
    for i, (pred_idx, probs) in enumerate(zip(pred_indices, all_probs)):
        classe = classes[pred_idx]
        confidence = float(max(probs))

        predicoes.append(
            BatchPredictItem(
                indice=i,
                classe=classe,
                confianca=round(confidence, 4),
                probabilidades={
                    classes[j]: round(float(p), 4) for j, p in enumerate(probs)
                },
            )
        )

        # Metrica por classe
        PREDICTIONS_TOTAL.labels(classe=classe, user=current_user["username"]).inc()

    latency = time.perf_counter() - start
    batch_size = len(payload.items)

    # Metricas
    BATCH_PREDICTIONS_TOTAL.labels(
        user=current_user["username"], batch_size=str(batch_size)
    ).inc()
    BATCH_PREDICTION_LATENCY.observe(latency)

    # Log
    logger.info(
        "batch_prediction_completed",
        extra={
            "trace_id": trace_id,
            "user": current_user["username"],
            "batch_size": batch_size,
            "latency_ms": round(latency * 1000, 2),
            "avg_latency_per_item_ms": round((latency * 1000) / batch_size, 2),
        },
    )

    return BatchPredictResponse(
        sucesso=True,
        total=batch_size,
        tempo_total_ms=round(latency * 1000, 2),
        predicoes=predicoes,
        usuario=current_user["username"],
    )

