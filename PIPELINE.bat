@echo off
chcp 65001 >nul
REM ============================================================
REM PIPELINE COMPLETO: ETL + VERIFICACIONES + DASHBOARD
REM ============================================================

echo ============================================================
echo   PIPELINE ETL COMPLETO
echo   ====================
echo   Ejecutando: ETL ^| Verificaciones ^| Dashboard
echo ============================================================
echo.

REM Configurar PYTHONPATH
set PYTHONPATH=%CD%

echo [1/3] Ejecutando proceso ETL...
echo.
python -m src.main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: El proceso ETL fallo
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [2/3] Verificando resultados...
echo ============================================================
echo.
python scripts_project\run_etl_with_tests.py --skip-etl
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Las verificaciones fallaron
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [3/3] Iniciando Dashboard...
echo ============================================================
echo.
echo Dashboard iniciado en: http://localhost:8000/dashboard.html
echo.
echo Presiona Ctrl+C para detener el servidor cuando termines.
echo ============================================================
echo.

python scripts_project\serve_dashboard.py

pause

