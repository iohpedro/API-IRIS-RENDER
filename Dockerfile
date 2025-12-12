# =============================================================================
# Dockerfile para API Iris com JWT 
# =============================================================================

# Imagem base: Python 3.11 slim (menor e mais segura)
FROM python:3.11-slim

# Definir diretorio de trabalho dentro do container
WORKDIR /app

# Copiar arquivo de dependencias primeiro (aproveita cache do Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o pacote app inteiro (codigo + modelos)
COPY app/ ./app/

# Expor a porta (documentacao, Render usa $PORT)
EXPOSE 8000

# Comando para iniciar a API (agora app.main:app)
# Usamos $PORT para compatibilidade com Render/Heroku
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]





