"""
Configuracao de Logs Estruturados (JSON)
Facilita analise em ferramentas como CloudWatch, Kibana, Loggly

Logs estruturados permitem:
- Filtrar por campos especificos (user, endpoint, status)
- Correlacionar eventos com trace_id
- Integrar com ferramentas de observabilidade
"""
import logging
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Formatter customizado que adiciona campos extras a cada log.
    
    Campos adicionados automaticamente:
    - timestamp: Data/hora em formato ISO 8601
    - level: Nivel do log (INFO, WARNING, ERROR)
    - service: Nome do servico (api-iris-v2)
    - logger: Nome do logger
    """
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Campos padrao em todo log
        log_record['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        log_record['level'] = record.levelname
        log_record['service'] = 'api-iris-v2'
        log_record['logger'] = record.name
        
        # Garante que message existe
        if not log_record.get('message'):
            log_record['message'] = record.getMessage()


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Configura e retorna um logger com formato JSON.
    
    Args:
        level: Nivel minimo de log (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Logger configurado para JSON estruturado
    
    Exemplo de uso:
        logger = setup_logging("INFO")
        logger.info("user_login", extra={"username": "admin", "ip": "192.168.1.1"})
    
    Saida:
        {"timestamp": "2025-12-11T10:30:00Z", "level": "INFO", "service": "api-iris-v2", 
         "message": "user_login", "username": "admin", "ip": "192.168.1.1"}
    """
    logger = logging.getLogger("api")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Handler para stdout (container-friendly)
    # Containers capturam stdout/stderr automaticamente
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    ))
    
    # Remove handlers anteriores (evita duplicacao)
    logger.handlers = []
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger


# Logger global para importar em outros modulos
logger = setup_logging()
