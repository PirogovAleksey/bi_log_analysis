@echo off
REM Banking Logs Analysis - Setup Script for Windows
REM This script sets up the entire ELK stack environment

echo =========================================
echo Banking Logs Analysis - ELK Stack Setup
echo =========================================
echo.

REM Check if Docker is running
echo [1/6] Checking Docker...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not running. Please start Docker Desktop.
    exit /b 1
)
echo [OK] Docker is running
echo.

REM Start Elasticsearch first
echo [2/6] Starting Elasticsearch...
docker-compose up -d elasticsearch
if %errorlevel% neq 0 (
    echo Error: Failed to start Elasticsearch
    exit /b 1
)
echo [OK] Elasticsearch container started
echo.

REM Wait for Elasticsearch
echo [3/6] Waiting for Elasticsearch to be ready (this may take 1-2 minutes)...
echo Please wait while Elasticsearch initializes...
ping -n 31 127.0.0.1 >nul 2>&1

set max_attempts=60
set attempt=0

:wait_elasticsearch
if %attempt% geq %max_attempts% (
    echo.
    echo Error: Elasticsearch failed to start after 2 minutes
    echo Checking logs:
    docker-compose logs elasticsearch
    exit /b 1
)

docker exec elasticsearch curl -s http://localhost:9200 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Elasticsearch is ready
    goto elasticsearch_ready
)

ping -n 3 127.0.0.1 >nul 2>&1
set /a attempt+=1
goto wait_elasticsearch

:elasticsearch_ready
echo.
echo [OK] Starting Logstash and Kibana...
docker-compose up -d logstash kibana
if %errorlevel% neq 0 (
    echo Warning: Some containers may have failed to start
)
ping -n 11 127.0.0.1 >nul 2>&1
echo.

REM Setup Elasticsearch index template
echo [4/6] Setting up Elasticsearch index template...
where python >nul 2>&1
if %errorlevel% equ 0 (
    python setup_elasticsearch.py
) else (
    echo Warning: Python not found. Please run 'python setup_elasticsearch.py' manually
)
echo.

REM Generate sample logs
echo [5/6] Generating sample banking logs...
where python >nul 2>&1
if %errorlevel% equ 0 (
    python generate_logs.py -n 10000
) else (
    echo Warning: Python not found. Please run 'python generate_logs.py' manually
)
echo.

REM Wait for Logstash to process
echo [6/6] Waiting for Logstash to process logs...
ping -n 16 127.0.0.1 >nul 2>&1
echo [OK] Setup complete
echo.

echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Access your services:
echo   - Elasticsearch: http://localhost:9200
echo   - Kibana:        http://localhost:5601
echo   - Logstash:      http://localhost:9600
echo.
echo Next steps:
echo   1. Open Kibana at http://localhost:5601
echo   2. Create a data view (see LAB_MANUAL.md)
echo   3. Start exploring your data!
echo.
echo To view logs: docker-compose logs -f
echo To stop:      docker-compose down
echo =========================================
