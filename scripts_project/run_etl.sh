#!/bin/bash
# Script para ejecutar el ETL en Linux/Mac
# Configura PYTHONPATH y ejecuta el proyecto

# Configurar PYTHONPATH
export PYTHONPATH=$(cd .. && pwd)

# Ejecutar el ETL
cd ..
python3 -m src.main

