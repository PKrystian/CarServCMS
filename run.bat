@echo off
if "%1"=="build_start" goto build_start
if "%1"=="stop" goto stop

echo Usage: run.bat [build_start^|stop]
goto end

:build_start
echo Building project and starting...
docker-compose build
docker-compose up -d
goto end

:stop
echo Stopping project...
docker-compose down
goto end

:end
