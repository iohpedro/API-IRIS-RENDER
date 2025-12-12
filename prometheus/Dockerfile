FROM prom/prometheus:v2.47.0

USER root

COPY alerts.yml /etc/prometheus/alerts.yml
COPY entrypoint.sh /entrypoint.sh

# Remove CRLF (Windows) e dá permissão de execução
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

# Garante que o diretório de dados existe e é gravável
RUN mkdir -p /prometheus && chown -R nobody:nobody /prometheus

EXPOSE 9090

ENTRYPOINT ["/entrypoint.sh"]
