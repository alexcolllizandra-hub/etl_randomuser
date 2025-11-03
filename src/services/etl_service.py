import requests
from collections import Counter
from typing import List, Dict, Any
from src.models.user_model import User
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def _mean(data: list) -> float:
    return sum(data) / len(data) if data else 0.0

def _median(data: list) -> float:
    n = len(data)
    if n == 0:
        return 0.0
    sorted_data = sorted(data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid-1] + sorted_data[mid]) / 2
    return sorted_data[mid]

def _pstdev(data: list) -> float:
    n = len(data)
    if n == 0:
        return 0.0
    mu = _mean(data)
    return (sum((x - mu) ** 2 for x in data) / n) ** 0.5

class ETLService:
    """Servicio ETL: extracción y transformación básica de usuarios."""

    def extract_users(self, n: int = 1000, seed: str = None) -> List[User]:
        """
        Extrae usuarios desde la API RandomUser.
        
        Args:
            n: Número de usuarios a extraer (por defecto 1000, máximo 5000)
            seed: Semilla opcional para reproducibilidad. Si se proporciona,
                  la API devolverá siempre los mismos usuarios para ese seed.
                  
        Returns:
            Lista de objetos User con los datos extraídos.
        """

        seed_msg = f" con seed='{seed}'" if seed else ""
        logger.info(f"Iniciando extracción de {n} usuarios{seed_msg}...")

        url = f"https://randomuser.me/api/?results={n}"
        if seed:
            url += f"&seed={seed}"
            
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json().get("results", [])
            users = [User.from_api(u) for u in data]
            logger.info(f"Extracción completada: {len(users)} usuarios.")
        except Exception as e:
            logger.error(f"Error en la extracción: {e}")
            users = []

        return users

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
            "avg_age": round(_mean(ages), 2),
            "median_age": round(_median(ages), 2),
            "std_age": round(_pstdev(ages), 2),
            "min_age": min(ages) if ages else 0,
            "max_age": max(ages) if ages else 0,
            "gender_distribution": dict(Counter(genders)),
            "top_countries": Counter(countries).most_common(10),
        }

        logger.info(f"Transformación básica completada con estadísticas: {stats}")
        return stats
