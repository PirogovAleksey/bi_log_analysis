@echo off
REM Banking Logs Analysis - Cleanup Script for Windows
REM This script stops and removes all containers and data

echo =========================================
echo Banking Logs Analysis - Cleanup
echo =========================================
echo.

set /p confirm="This will remove all containers and data. Continue? (y/N) "
if /i not "%confirm%"=="y" (
    echo Cleanup cancelled
    exit /b 0
)

echo Stopping containers...
docker-compose down

set /p volumes="Remove volumes (all Elasticsearch data will be lost)? (y/N) "
if /i "%volumes%"=="y" (
    echo Removing volumes...
    docker-compose down -v
    echo [OK] Volumes removed
)

set /p logs="Remove generated log files? (y/N) "
if /i "%logs%"=="y" (
    echo Removing log files...
    del /q logs\*.log 2>nul
    echo [OK] Log files removed
)

echo.
echo =========================================
echo Cleanup complete!
echo =========================================
