@echo off
chcp 65001 >nul
cls
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
echo Abriendo navegador en: http://localhost:8000/dashboard/dashboard.html
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python scripts_project\serve_dashboard.py
pause

