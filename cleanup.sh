#!/bin/bash

# Banking Logs Analysis - Cleanup Script
# This script stops and removes all containers and data

echo "========================================="
echo "Banking Logs Analysis - Cleanup"
echo "========================================="
echo ""

read -p "This will remove all containers and data. Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled"
    exit 0
fi

echo "Stopping containers..."
docker-compose down

read -p "Remove volumes (all Elasticsearch data will be lost)? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing volumes..."
    docker-compose down -v
    echo "✓ Volumes removed"
fi

read -p "Remove generated log files? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing log files..."
    rm -f logs/*.log
    echo "✓ Log files removed"
fi

echo ""
echo "========================================="
echo "Cleanup complete!"
echo "========================================="
