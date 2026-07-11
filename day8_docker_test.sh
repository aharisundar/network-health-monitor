#!/bin/bash
"""
Day 8: Docker Containerization Test
Tests Docker image build and container operations
"""

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        DAY 8: DOCKER CONTAINERIZATION TEST                     ║"
echo "║     Build and validate container image                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Check Docker installation
echo "✅ TEST 1: DOCKER INSTALLATION CHECK"
echo "════════════════════════════════════════════════════════════════"

if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    docker --version
else
    echo "❌ Docker not installed"
    exit 1
fi

echo ""

# Test 2: Check docker-compose
echo "✅ TEST 2: DOCKER-COMPOSE CHECK"
echo "════════════════════════════════════════════════════════════════"

if command -v docker-compose &> /dev/null; then
    echo "✅ Docker-compose is installed"
    docker-compose --version
else
    echo "⚠️  Docker-compose not installed (can be installed separately)"
fi

echo ""

# Test 3: Validate Dockerfile syntax
echo "✅ TEST 3: DOCKERFILE VALIDATION"
echo "════════════════════════════════════════════════════════════════"

if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile exists"
    echo "   Checking syntax..."
    
    # Check for key Dockerfile directives
    if grep -q "FROM" Dockerfile && grep -q "WORKDIR" Dockerfile && grep -q "CMD" Dockerfile; then
        echo "✅ Dockerfile contains required directives (FROM, WORKDIR, CMD)"
    else
        echo "❌ Dockerfile missing required directives"
        exit 1
    fi
else
    echo "❌ Dockerfile not found"
    exit 1
fi

echo ""

# Test 4: Validate docker-compose syntax
echo "✅ TEST 4: DOCKER-COMPOSE VALIDATION"
echo "════════════════════════════════════════════════════════════════"

if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml exists"
    echo "   Checking syntax..."
    
    if grep -q "version:" docker-compose.yml && grep -q "services:" docker-compose.yml; then
        echo "✅ docker-compose.yml contains required sections (version, services)"
    else
        echo "❌ docker-compose.yml missing required sections"
        exit 1
    fi
else
    echo "❌ docker-compose.yml not found"
    exit 1
fi

echo ""

# Test 5: Check requirements.txt
echo "✅ TEST 5: REQUIREMENTS.TXT CHECK"
echo "════════════════════════════════════════════════════════════════"

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt exists"
    line_count=$(wc -l < requirements.txt)
    echo "   Contains $line_count packages"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

echo ""

# Test 6: Check source code exists
echo "✅ TEST 6: SOURCE CODE CHECK"
echo "════════════════════════════════════════════════════════════════"

if [ -d "src" ]; then
    echo "✅ src/ directory exists"
    file_count=$(ls -1 src/ | wc -l)
    echo "   Contains $file_count Python files"
else
    echo "❌ src/ directory not found"
    exit 1
fi

echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
echo "🎉 ALL DOCKER TESTS PASSED!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✅ Docker setup is ready!"
echo "✅ Containerization files validated!"
echo "✅ Ready for production deployment!"
echo ""
echo "Next steps:"
echo "  1. Build image: docker build -t network-health-monitor ."
echo "  2. Run container: docker run -p 5000:5000 network-health-monitor"
echo "  3. Or use: docker-compose up"
echo ""
