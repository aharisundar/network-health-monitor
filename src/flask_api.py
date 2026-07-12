"""
Flask API Module
REST API endpoints for metrics queries
"""
from flask import Flask, jsonify
from prometheus_client import Counter, Gauge, generate_latest
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

request_count = Counter('flask_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Gauge('flask_request_duration_seconds', 'Request duration')

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "network-health-monitor"})

@app.route('/devices', methods=['GET'])
def devices():
    return jsonify({"devices": []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
