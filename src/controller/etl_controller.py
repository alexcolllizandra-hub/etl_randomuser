import os
from services.etl_service import ETLService
from services.transformer_service import TransformerService
from services.visualization_service import VisualizationService
from loaders.csv_loader import CSVLoader
from loaders.sql_loader import SQLLoader
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ETLController:
    """Controlador principal del flujo ETL completo."""

    def __init__(self):
        self.etl_service = ETLService()
        self.visualizer = VisualizationService()
        self.output_dir = os.path.join(os.path.dirname(__file__), "../../data")
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, n_users: int = 1000):
        logger.info("=== Iniciando proceso ETL extendido ===")

        # 1️⃣ Extracción y limpieza
        users = self.etl_service.extract_users(n_users)
        users = self.etl_service.clean_users(users)

        # 2️⃣ Transformación inicial básica
        basic_stats = self.etl_service.transform_users(users)
        logger.info(f"Estadísticas básicas: {basic_stats}")

        # 3️⃣ Transformación avanzada sin pandas
        transformer = TransformerService(users)
        transformer.enrich_data()
        transformer.detect_outliers()
        transformer.enrich_with_country_data()
        advanced_stats = transformer.compute_statistics()
        users = transformer.get_users()  # ✅ Aquí sustituimos get_dataframe()

        logger.info(f"Estadísticas avanzadas: {advanced_stats}")

        # 4️⃣ Carga de datos (convertimos objetos a dict)
        data_dicts = [u.__dict__ for u in users]
        CSVLoader("usuarios.csv").load(data_dicts, self.output_dir)
        SQLLoader("usuarios.db").load(data_dicts, self.output_dir)

        # 5️⃣ Visualizaciones
        logger.info("Generando visualizaciones...")
        self.visualizer.plot_age_distribution(users)
        self.visualizer.plot_gender_distribution(users)
        self.visualizer.plot_top_countries(users)
        # Los métodos de visualización que usan DataFrame se pueden adaptar si lo necesitas

        logger.info("=== Proceso ETL completado con éxito ===")
