#!/bin/bash
# ============================================================
# PIPELINE COMPLETO: ETL + VERIFICACIONES + DASHBOARD
# ============================================================

clear
echo "============================================================"
echo "     PIPELINE ETL COMPLETO"
echo "============================================================"
echo "Ejecutando: ETL | Verificaciones | Dashboard"
echo "============================================================"
echo ""

export PYTHONPATH=$(pwd)

# Fase 1: Ejecutar ETL
echo "[1/3] Ejecutando proceso ETL..."
python3 -m src.main
if [ $? -ne 0 ]; then
    echo "ERROR: El proceso ETL falló"
    exit 1
fi

echo ""
echo "[2/3] Verificando resultados..."
python3 scripts_project/run_etl_with_tests.py --skip-etl
if [ $? -ne 0 ]; then
    echo "ERROR: Las verificaciones fallaron"
    exit 1
fi

echo ""
echo "[3/3] Iniciando Dashboard..."
echo ""
echo "Abre en tu navegador: http://localhost:8000/dashboard/dashboard.html"
echo "Presiona Ctrl+C para detener el servidor"
echo "============================================================"
echo ""

python3 scripts_project/serve_dashboard.py

