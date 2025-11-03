@echo off
chcp 65001 >nul
cls

REM Cerrar servidores anteriores que puedan estar ocupando el puerto 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Cerrando proceso anterior en puerto 8000...
    taskkill /F /PID %%a >nul 2>&1
)

echo ============================================================
echo       PIPELINE ETL COMPLETO
echo ============================================================
echo Ejecutando: ETL ^| Verificaciones ^| Dashboard
echo ============================================================
echo.

set PYTHONPATH=%CD%

REM Fase 1: Ejecutar ETL
echo [1/3] Ejecutando proceso ETL...
python -m src.main
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: El proceso ETL fallo
    pause
    exit /b 1
)

echo.
echo [2/3] Verificando resultados...
python scripts_project\run_etl_with_tests.py --skip-etl
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Las verificaciones fallaron
    pause
    exit /b 1
)

echo.
echo [3/3] Iniciando Dashboard...
echo.
echo Dashboard abierto en: http://localhost:8000/dashboard/dashboard.html
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python scripts_project\serve_dashboard.py
pause

