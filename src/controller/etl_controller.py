import os
from src.services.etl_service import ETLService
from src.services.transformer_service import TransformerService
from src.services.visualization_service import VisualizationService
from src.loaders.csv_loader import CSVLoader
from src.loaders.sql_loader import SQLLoader
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class ETLController:
    """Controlador principal del flujo ETL completo."""

    def __init__(self):
        self.etl_service = ETLService()
        self.output_dir = os.path.join(os.path.dirname(__file__), "../../data")
        self.plots_dir = os.path.join(os.path.dirname(__file__), "../../plots")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.plots_dir, exist_ok=True)
        self.visualizer = VisualizationService(output_dir=self.plots_dir)

    def run(self, n_users: int = 1000):
        logger.info("=== Iniciando proceso ETL extendido ===")

        # 1. Extracción y limpieza
        users = self.etl_service.extract_users(n_users)
        users = self.etl_service.clean_users(users)

        # 2. Transformación inicial básica
        basic_stats = self.etl_service.transform_users(users)
        logger.info(f"Estadísticas básicas: {basic_stats}")

        # 3. Transformación avanzada sin pandas
        transformer = TransformerService(users)
        transformer.enrich_data()
        transformer.detect_outliers()
        transformer.enrich_with_country_data()
        advanced_stats = transformer.compute_statistics()
        users = transformer.get_users()  # Sustituimos get_dataframe()

        logger.info(f"Estadísticas avanzadas: {advanced_stats}")

        # 4. Carga de datos (convertimos objetos a dict)
        data_dicts = [u.__dict__ for u in users]
        CSVLoader("usuarios.csv").load(data_dicts, self.output_dir)
        SQLLoader("usuarios.db").load(data_dicts, self.output_dir)

        # 5. Visualizaciones
        logger.info("Generando visualizaciones...")
        self.visualizer.plot_age_distribution(users)
        self.visualizer.plot_gender_distribution(users)
        self.visualizer.plot_top_countries(users)
        self.visualizer.plot_age_by_country(users)
        self.visualizer.plot_correlation_matrix(users)

        logger.info("=== Proceso ETL completado con éxito ===")
