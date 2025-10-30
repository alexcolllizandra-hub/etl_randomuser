import requests
import statistics
from collections import Counter
from typing import List, Dict, Any
from models.user_model import User
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ETLService:
    """Servicio ETL: extracción y transformación básica de usuarios."""

    def extract_users(self, n: int = 1000) -> List[User]:
        """
        Extrae usuarios desde la API RandomUser con soporte para paginación.
        Puede solicitar hasta miles de registros dividiéndolos en lotes.
        """
        users = []
        batch_size = 500
        pages = n // batch_size + (1 if n % batch_size else 0)

        logger.info(f"Iniciando extracción de {n} usuarios en {pages} páginas...")

        for i in range(1, pages + 1):
            url = f"https://randomuser.me/api/?results={batch_size}&page={i}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json().get("results", [])
                users.extend([User.from_api(u) for u in data])
                logger.info(f"Página {i}/{pages} descargada: {len(data)} usuarios.")
            except Exception as e:
                logger.error(f"Error en la página {i}: {e}")

        logger.info(f"Total extraído: {len(users)} usuarios.")
        return users[:n]

    def clean_users(self, users: List[User]) -> List[User]:
        """Limpia usuarios eliminando registros incompletos o inválidos."""
        cleaned = [u for u in users if u.email and u.age > 0 and u.country]
        logger.info(f"Limpieza completada: {len(cleaned)} usuarios válidos de {len(users)} totales.")
        return cleaned

    def transform_users(self, users: List[User]) -> Dict[str, Any]:
        """Calcula estadísticas descriptivas básicas."""
        ages = [u.age for u in users]
        genders = [u.gender for u in users]
        countries = [u.country for u in users]

        stats = {
            "total_users": len(users),
            "avg_age": round(statistics.mean(ages), 2),
            "median_age": round(statistics.median(ages), 2),
            "std_age": round(statistics.pstdev(ages), 2),
            "min_age": min(ages),
            "max_age": max(ages),
            "gender_distribution": dict(Counter(genders)),
            "top_countries": Counter(countries).most_common(10),
        }

        logger.info(f"Transformación básica completada con estadísticas: {stats}")
        return stats
