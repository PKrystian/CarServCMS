@echo off
echo ========================================
echo CarServ CMS - Quick Start
echo ========================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop and ensure it is running.
    pause
    exit /b 1
)

echo Docker is running!
echo.

echo Stopping existing containers...
docker-compose down

echo.
echo Building and starting containers...
echo This may take a few minutes on first run...
docker-compose up -d --build

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo CarServ CMS is now running!
echo ========================================
echo.
echo Frontend:     http://localhost:8000
echo Admin Panel:  http://localhost:8000/admin
echo API Docs:     http://localhost:8000/docs
echo PgAdmin:      http://localhost:5050/pgadmin
echo.
echo Default Login:
echo   Username: admin
echo   Password: admin
echo.
echo Press any key to view logs (Ctrl+C to exit)...
pause >nul

docker-compose logs -f

