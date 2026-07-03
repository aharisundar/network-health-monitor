# Network Health Monitor & Auto-Alert System

Production-ready network monitoring tool with real-time anomaly detection and automated alerting for multi-vendor network environments.

## Overview

Network Health Monitor is an enterprise-grade infrastructure monitoring solution that:

- Connects to network devices (Cisco, Juniper, Aruba, Arista) via SSH
- Collects real-time metrics (CPU, memory, interface utilization)
- Detects anomalies using threshold-based analysis
- Sends alerts via Slack, Email, or PagerDuty
- Visualizes metrics in Grafana dashboards
- Stores historical data for trending and compliance
- Provides REST API for integration
- Runs in Docker for easy deployment

## Problem Statement

Network operations teams spend hours manually:
- SSH-ing into devices to check status
- Waiting for issues to escalate
- Creating ad-hoc monitoring solutions
- Correlating metrics from multiple sources

This tool automates all of that!

## Architecture

Network Devices (Multi-Vendor)
    ↓ (SSH via Netmiko)
Device Collector
    ↓
Metrics Processor
    ↓
Anomaly Detector
    ├→ Alerter (Slack)
    ├→ Database (SQLite)
    ├→ Prometheus Export
    └→ Flask API
    ↓
Grafana Dashboard

## Tech Stack

- Language: Python 3.9+
- Device Connection: Netmiko 4.3+
- Metrics Export: Prometheus Client
- Visualization: Grafana (Docker)
- Alerting: Slack SDK
- Web Framework: Flask
- Database: SQLite
- Containerization: Docker & Docker Compose
- CI/CD: GitHub Actions
- Testing: Pytest

## Supported Vendors & Devices

### Cisco
- Catalyst (2960, 3850, 9200, 9300, 9500)
- ASR (1000, 9000 series edge routers)
- Nexus (3000, 5000, 7000, 9000 data center)

### Juniper
- EX Series (EX2200, EX4200, EX9200)
- SRX Series (SRX110, SRX210, SRX5400)

### Aruba
- ArubaOS Series (6300, 6400, 8200, 8400)

### Arista
- EOS Series (7050, 7150, 7250, 7300)

## Quick Start

### Prerequisites
- Python 3.9+
- Git
- Network device SSH access
- (Later) Docker & Docker Compose

### Installation

git clone https://github.com/yourusername/network-health-monitor.git
cd network-health-monitor

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

pytest tests/ -v --cov=src

## Metrics Collected

Each device reports:

{
  "timestamp": "2026-07-03T14:42:18Z",
  "device": "switch-01",
  "vendor": "cisco",
  "cpu_usage": 45.2,
  "memory_usage": 62.8,
  "interfaces": {
    "Gi0/0/1": {"state": "up", "utilization": 35.2},
    "Gi0/0/2": {"state": "up", "utilization": 72.1}
  },
  "uptime_seconds": 864000
}

## Alert Examples

CRITICAL: Device sw1-core
CPU utilization: 95% (threshold: 90%)
Recommended: Investigate running processes

WARNING: Device rt1-edge
Memory utilization: 82% (threshold: 85%)
Trending toward critical over 30 minutes

## Project Timeline

Week 1 (Jul 3-9): Architecture & Setup - In Progress
Week 2 (Jul 10-16): Core Functionality - Pending
Week 3 (Jul 17-23): Integration & Monitoring - Pending
Week 4 (Jul 24-30): Production Ready - Pending

## Files Structure

network-health-monitor/
├── src/ (Source code)
│   ├── main.py
│   ├── device_collector.py
│   ├── metrics_processor.py
│   ├── anomaly_detector.py
│   ├── alerter.py
│   ├── flask_api.py
│   └── prometheus_exporter.py
│
├── tests/ (Unit tests)
│   ├── test_device_collector.py
│   └── test_metrics_processor.py
│
├── config/ (Configuration)
│   ├── devices.yaml
│   └── thresholds.yaml
│
├── prometheus/
├── grafana/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

## Configuration

Create .env file:

DEVICE_HOST=192.168.1.1
DEVICE_USERNAME=admin
DEVICE_PASSWORD=password

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

CPU_THRESHOLD=90
MEMORY_THRESHOLD=85

## Testing

Run all tests:
pytest tests/ -v

Run with coverage:
pytest tests/ --cov=src --cov-report=html

Run specific test:
pytest tests/test_device_collector.py -v

## Contributing

1. Fork repository
2. Create feature branch
3. Add tests
4. Submit pull request

## License

MIT License

## Author

Hari Sundar A
Network Engineer | Infrastructure Automation | Python Developer
GitHub: https://github.com/aharisundar
LinkedIn: https://linkedin.com/in/harisundar21

---

Status: Active Development
Last Updated: July 3, 2026
Version: 0.1.0
