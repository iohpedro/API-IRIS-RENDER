"""
Configuracoes globais da API Iris v2.

Centraliza variaveis de ambiente, versao da API e logger.
Importe daqui para manter configuracao unica em todo o projeto.
"""
import os

from app.logging_config import setup_logging


ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
API_VERSION = "2.0.0"  # Versao major 2 = nova versao com breaking changes

# Reconfigura o logger global com o nivel desejado
logger = setup_logging(os.getenv("LOG_LEVEL", "INFO"))

