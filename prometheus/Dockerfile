FROM prom/prometheus:v2.47.0

COPY alerts.yml /etc/prometheus/alerts.yml
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 9090

ENTRYPOINT ["/entrypoint.sh"]
