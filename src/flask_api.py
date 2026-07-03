"""
Flask API Module
REST API endpoints for metrics queries
"""

from flask import Flask, jsonify
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "network-health-monitor"})


@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    # TODO: Week 3 - Implement metrics export
    return jsonify({"message": "Metrics endpoint - Coming in Week 3"})


@app.route('/devices', methods=['GET'])
def devices():
    """Get list of monitored devices"""
    # TODO: Week 3 - Implement device listing
    return jsonify({"devices": []})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
