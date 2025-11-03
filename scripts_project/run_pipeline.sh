#!/bin/bash
# Pipeline completo: Ejecuta el ETL y verifica todos los resultados

echo "============================================================"
echo "PIPELINE ETL CON VERIFICACIONES AUTOMATICAS"
echo "============================================================"
echo ""

# Configurar PYTHONPATH
export PYTHONPATH=$(pwd)

# Ejecutar el pipeline con tests
python3 run_etl_with_tests.py

echo ""
echo "============================================================"
echo "Pipeline completado"
echo "============================================================"

