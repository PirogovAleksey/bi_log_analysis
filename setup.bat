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

REM Start Docker Compose
echo [2/6] Starting ELK Stack containers...
docker-compose up -d
if %errorlevel% neq 0 (
    echo Error: Failed to start containers
    exit /b 1
)
echo [OK] Containers started
echo.

REM Wait for Elasticsearch
echo [3/6] Waiting for Elasticsearch to be ready...
timeout /t 10 /nobreak >nul

set max_attempts=30
set attempt=0

:wait_elasticsearch
if %attempt% geq %max_attempts% (
    echo.
    echo Error: Elasticsearch failed to start
    exit /b 1
)

curl -s http://localhost:9200 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Elasticsearch is ready
    goto elasticsearch_ready
)

echo | set /p=.
timeout /t 2 /nobreak >nul
set /a attempt+=1
goto wait_elasticsearch

:elasticsearch_ready
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
timeout /t 15 /nobreak >nul
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
