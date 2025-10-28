#!/bin/bash

# Banking Logs Analysis - Setup Script
# This script sets up the entire ELK stack environment

set -e

echo "========================================="
echo "Banking Logs Analysis - ELK Stack Setup"
echo "========================================="
echo ""

# Check if Docker is running
echo "[1/6] Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "✓ Docker is running"
echo ""

# Start Docker Compose
echo "[2/6] Starting ELK Stack containers..."
docker-compose up -d
echo "✓ Containers started"
echo ""

# Wait for Elasticsearch
echo "[3/6] Waiting for Elasticsearch to be ready..."
sleep 10
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:9200 > /dev/null; then
        echo "✓ Elasticsearch is ready"
        break
    fi
    echo -n "."
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo ""
    echo "Error: Elasticsearch failed to start"
    exit 1
fi
echo ""

# Setup Elasticsearch index template
echo "[4/6] Setting up Elasticsearch index template..."
if command -v python3 &> /dev/null; then
    python3 setup_elasticsearch.py
elif command -v python &> /dev/null; then
    python setup_elasticsearch.py
else
    echo "Warning: Python not found. Please run 'python setup_elasticsearch.py' manually"
fi
echo ""

# Generate sample logs
echo "[5/6] Generating sample banking logs..."
if command -v python3 &> /dev/null; then
    python3 generate_logs.py -n 10000
elif command -v python &> /dev/null; then
    python generate_logs.py -n 10000
else
    echo "Warning: Python not found. Please run 'python generate_logs.py' manually"
fi
echo ""

# Wait for Logstash to process
echo "[6/6] Waiting for Logstash to process logs..."
sleep 15
echo "✓ Setup complete"
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Access your services:"
echo "  - Elasticsearch: http://localhost:9200"
echo "  - Kibana:        http://localhost:5601"
echo "  - Logstash:      http://localhost:9600"
echo ""
echo "Next steps:"
echo "  1. Open Kibana at http://localhost:5601"
echo "  2. Create a data view (see LAB_MANUAL.md)"
echo "  3. Start exploring your data!"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop:      docker-compose down"
echo "========================================="
