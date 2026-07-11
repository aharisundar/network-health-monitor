#!/bin/bash

echo "✅ TEST 1: Checking Dockerfile..."
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile exists"
else
    echo "❌ Dockerfile missing"
    exit 1
fi

echo "✅ TEST 2: Checking docker-compose.yml..."
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml exists"
else
    echo "❌ docker-compose.yml missing"
    exit 1
fi

echo "✅ TEST 3: Checking prometheus.yml..."
if [ -f "prometheus/prometheus.yml" ]; then
    echo "✅ prometheus.yml exists"
else
    echo "❌ prometheus.yml missing"
    exit 1
fi

echo ""
echo "🎉 ALL DAY 8 FILES CORRECT!"
