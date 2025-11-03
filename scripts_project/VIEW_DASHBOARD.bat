@echo off
REM Abre el dashboard HTML en el navegador usando un servidor local

echo ============================================================
echo ACTIVANDO DASHBOARD ETL
echo ============================================================
echo.

REM Configurar PYTHONPATH
set PYTHONPATH=%cd%\..

REM Ejecutar el servidor
cd ..
python scripts_project\serve_dashboard.py

pause

