"""
main.py
---------
Punto de entrada del proyecto ETL.
Orquesta el flujo de extracción, transformación, carga y visualización.
"""

from src.controller.etl_controller import ETLController

def main():
    """Ejecuta el proceso ETL completo."""
    print("🚀 Iniciando proceso ETL de usuarios...\n")

    # Instanciamos el controlador principal del proceso
    controller = ETLController()

    # Ejecutamos el pipeline (por defecto extrae 100 usuarios)
    controller.run(n_users=100)

    print("\nProceso ETL finalizado con éxito.")

if __name__ == "__main__":
    main()
