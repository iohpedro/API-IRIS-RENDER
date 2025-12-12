"""
Carregamento do modelo Iris.

Separado do main.py para evitar efeitos colaterais em rotas e facilitar testes.
O carregamento acontece na importacao do modulo.
"""
import pickle
from pathlib import Path

from app.core import logger
from app.metrics import MODEL_LOADED


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATHS = [
    BASE_DIR / "models/modelo_iris.pkl",
    Path("app/models/modelo_iris.pkl"),
    Path("/app/app/models/modelo_iris.pkl"),
    Path("modelo_iris.pkl"),
]

modelo = None
classes = None

for model_path in MODEL_PATHS:
    if model_path.exists():
        with open(model_path, "rb") as f:
            modelo = pickle.load(f)
        classes_path = model_path.parent / "classes_iris.pkl"
        if classes_path.exists():
            with open(classes_path, "rb") as f:
                classes = pickle.load(f)
        logger.info("model_loaded", extra={"path": str(model_path)})
        break

MODELO_OK = modelo is not None and classes is not None

# Atualiza metrica do Prometheus
MODEL_LOADED.set(1 if MODELO_OK else 0)

if not MODELO_OK:
    logger.warning(
        "model_not_found",
        extra={"searched_paths": [str(p) for p in MODEL_PATHS]},
    )
