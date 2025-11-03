@echo off
REM Script para ejecutar el ETL en Windows
REM Configura PYTHONPATH y ejecuta el proyecto

REM Configurar PYTHONPATH
set PYTHONPATH=%cd%\..

REM Ejecutar el ETL
cd ..
python -m src.main

