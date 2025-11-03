"""
main.py
---------
Punto de entrada del proyecto ETL.
Orquesta el flujo de extracción, transformación, carga y visualización.
"""

import os
import sys

# Asegurar que el directorio raíz esté en el PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controller.etl_controller import ETLController

def main():
    """Ejecuta el proceso ETL completo."""
    print("Iniciando proceso ETL de usuarios...\n")

    # Instanciamos el controlador principal del proceso
    controller = ETLController()

    # Ejecutamos el pipeline (por defecto extrae 100 usuarios)
    controller.run(n_users=1000)

    print("\nProceso ETL finalizado con éxito.")

if __name__ == "__main__":
    main()
