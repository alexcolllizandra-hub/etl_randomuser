#!/bin/bash
# ============================================================
# PIPELINE COMPLETO: ETL + VERIFICACIONES + DASHBOARD
# ============================================================

echo "============================================================"
echo "  PIPELINE ETL COMPLETO"
echo "  ===================="
echo "  Ejecutando: ETL | Verificaciones | Dashboard"
echo "============================================================"
echo ""

# Configurar PYTHONPATH
export PYTHONPATH=$(pwd)

echo "[1/3] Ejecutando proceso ETL..."
echo ""
python3 -m src.main
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: El proceso ETL falló"
    exit 1
fi

echo ""
echo "============================================================"
echo "[2/3] Verificando resultados..."
echo "============================================================"
echo ""
python3 scripts_project/run_etl_with_tests.py --skip-etl
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Las verificaciones fallaron"
    exit 1
fi

echo ""
echo "============================================================"
echo "[3/3] Iniciando Dashboard..."
echo "============================================================"
echo ""
echo "Dashboard iniciado en: http://localhost:8000/dashboard.html"
echo ""
echo "Presiona Ctrl+C para detener el servidor cuando termines."
echo "============================================================"
echo ""

python3 scripts_project/serve_dashboard.py

