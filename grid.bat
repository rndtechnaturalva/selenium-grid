@echo off

REM Selenium Grid Management Script for Windows

if "%1"=="start" (
    echo Starting Selenium Grid...
    docker-compose up -d
    echo Grid started! Access console at: http://localhost:4444/ui
    goto end
)

if "%1"=="stop" (
    echo Stopping Selenium Grid...
    docker-compose down
    goto end
)

if "%1"=="restart" (
    echo Restarting Selenium Grid...
    docker-compose restart
    goto end
)

if "%1"=="status" (
    echo Selenium Grid Status:
    docker-compose ps
    goto end
)

if "%1"=="logs" (
    if "%2"=="" (
        docker-compose logs
    ) else (
        docker-compose logs %2
    )
    goto end
)

if "%1"=="scale" (
    if "%2"=="" (
        echo Usage: grid.bat scale ^<service^> ^<replicas^>
        echo Example: grid.bat scale chrome 3
    ) else if "%3"=="" (
        echo Usage: grid.bat scale ^<service^> ^<replicas^>
        echo Example: grid.bat scale chrome 3
    ) else (
        docker-compose up -d --scale %2=%3
    )
    goto end
)

if "%1"=="clean" (
    echo Cleaning up Selenium Grid...
    docker-compose down -v --remove-orphans
    docker system prune -f
    goto end
)

echo Selenium Grid Management Script
echo.
echo Usage: %0 {start^|stop^|restart^|status^|logs^|scale^|clean}
echo.
echo Commands:
echo   start     - Start the Selenium Grid
echo   stop      - Stop the Selenium Grid
echo   restart   - Restart the Selenium Grid
echo   status    - Show grid status
echo   logs      - Show logs (optionally specify service name)
echo   scale     - Scale a service (usage: scale ^<service^> ^<replicas^>)
echo   clean     - Stop and remove all containers, volumes, and orphans
echo.
echo Examples:
echo   %0 start
echo   %0 logs selenium-hub
echo   %0 scale chrome 3

:end