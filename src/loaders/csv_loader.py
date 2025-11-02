import csv
import os
from typing import List, Dict, Any
from src.loaders.base_loader import BaseLoader
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class CSVLoader(BaseLoader):
    """Carga datos en un archivo CSV dentro del directorio especificado."""

    def __init__(self, filename: str = "users.csv") -> None:
        self.filename = filename

    def load(self, data: List[Dict[str, Any]], output_dir: str) -> None:
        if not data:
            logger.warning("No hay datos para exportar en CSV.")
            return

        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, self.filename)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"Datos guardados correctamente en {filepath}")
