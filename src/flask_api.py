"""
Flask API Module
REST API endpoints for metrics queries
"""
from flask import Flask, jsonify
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY
import logging
import random
import threading
import time

from prometheus_exporter import export_device_metrics  # NEW IMPORT

logger = logging.getLogger(__name__)

app = Flask(__name__)

request_count = Counter('flask_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Gauge('flask_request_duration_seconds', 'Request duration')

# --- NEW: mock device fleet + background collector ---
MOCK_FLEET = [
    {"name": "catalyst-9300", "vendor": "cisco"},
    {"name": "ex-switch-01", "vendor": "juniper"},
    {"name": "aruba-6300",   "vendor": "aruba"},
    {"name": "arista-7050",  "vendor": "arista"},
]

def generate_mock_metrics():
    """Simulate CPU/memory/interface stats and push to Prometheus gauges."""
    while True:
        for dev in MOCK_FLEET:
            cpu = round(random.uniform(15, 75), 1)
            memory = round(random.uniform(20, 80), 1)
            interfaces = {
                f"eth0/{i}": {"utilization": round(random.uniform(0, 100), 1)}
                for i in range(4)
            }
            export_device_metrics(dev["name"], dev["vendor"], cpu, memory, interfaces)
        time.sleep(15)  # refresh every 15s

# Start background thread once, at import time
collector_thread = threading.Thread(target=generate_mock_metrics, daemon=True)
collector_thread.start()
# --- END NEW ---

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "network-health-monitor"}), 200

@app.route('/devices', methods=['GET'])
def devices():
    return jsonify({"devices": MOCK_FLEET}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
