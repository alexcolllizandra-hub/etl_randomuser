@echo off
REM Script para ejecutar el ETL en Windows
REM Configura PYTHONPATH y ejecuta el proyecto

set PYTHONPATH=%cd%
python src\main.py

