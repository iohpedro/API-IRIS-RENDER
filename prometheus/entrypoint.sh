#!/bin/sh
set -eu

# Render-friendly Prometheus config generation.
# We generate prometheus.yml at container start, so the target can be configured
# via environment variables.

SCRAPE_INTERVAL="${SCRAPE_INTERVAL:-15s}"
API_TARGET="${API_TARGET:-api:8000}"    # e.g. api-iris-v2.onrender.com
API_SCHEME="${API_SCHEME:-http}"       # http | https

cat > /etc/prometheus/prometheus.yml <<EOF
global:
  scrape_interval: ${SCRAPE_INTERVAL}

rule_files:
  - /etc/prometheus/alerts.yml

scrape_configs:
  - job_name: "api-iris-v2"
    scheme: ${API_SCHEME}
    metrics_path: /metrics
    static_configs:
      - targets: ["${API_TARGET}"]
EOF

exec /bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.listen-address=0.0.0.0:9090
