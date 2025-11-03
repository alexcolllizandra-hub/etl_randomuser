#!/bin/bash
# Abre el dashboard HTML en el navegador usando un servidor local

echo "============================================================"
echo "ACTIVANDO DASHBOARD ETL"
echo "============================================================"
echo ""

# Configurar PYTHONPATH
export PYTHONPATH=$(cd .. && pwd)

# Ejecutar el servidor
cd ..
python3 scripts_project/serve_dashboard.py

