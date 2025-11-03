@echo off
REM Pipeline completo: Ejecuta el ETL y verifica todos los resultados

echo ============================================================
echo PIPELINE ETL CON VERIFICACIONES AUTOMATICAS
echo ============================================================
echo.

REM Configurar PYTHONPATH
set PYTHONPATH=%CD%

REM Ejecutar el pipeline con tests
python run_etl_with_tests.py

echo.
echo ============================================================
echo Pipeline completado
echo ============================================================
pause

