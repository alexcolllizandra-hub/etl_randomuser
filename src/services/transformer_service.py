import requests
from collections import Counter
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

class TransformerService:
    """Transformaciones avanzadas y enriquecimiento de datos de usuarios (sin pandas)."""

    def __init__(self, users: list[User]):
        self.users = users
        logger.info(f"Inicializando Transformer con {len(users)} registros.")

    # ----------------------------
    # ENRIQUECIMIENTO DE DATOS
    # ----------------------------
    def enrich_data(self):
        """Crea nuevas columnas derivadas: grupos de edad y dominio de email."""
        for u in self.users:
            # Clasificación de grupo de edad
            if u.age < 18:
                age_group = "<18"
            elif u.age < 30:
                age_group = "18-30"
            elif u.age < 45:
                age_group = "31-45"
            elif u.age < 60:
                age_group = "46-60"
            elif u.age < 80:
                age_group = "61-80"
            else:
                age_group = "80+"

            u.age_group = age_group
            u.email_domain = u.email.split("@")[-1] if "@" in u.email else "unknown"

        logger.info("Datos enriquecidos: grupos de edad y dominios de email agregados.")

    # ----------------------------
    # DETECCIÓN DE OUTLIERS
    # ----------------------------
    def detect_outliers(self):
        """Detecta valores atípicos (outliers) de edad usando el método IQR."""
        ages = [u.age for u in self.users]
        if not ages:
            logger.warning("No hay datos para detectar outliers.")
            return
            
        q1, q3 = self._percentiles(ages, 25), self._percentiles(ages, 75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr

        for u in self.users:
            u.is_outlier = u.age < lower or u.age > upper

        n_outliers = sum(u.is_outlier for u in self.users)
        logger.info(f"Detectados {n_outliers} outliers de edad (método IQR).")

    def _percentiles(self, data: list, percent: float) -> float:
        """Calcula percentiles sin usar numpy."""
        if not data:
            return 0.0
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * (percent / 100)
        f, c = int(k), min(int(k) + 1, len(data_sorted) - 1)
        if f == c:
            return data_sorted[int(k)] if int(k) < len(data_sorted) else data_sorted[-1]
        return data_sorted[f] + (data_sorted[c] - data_sorted[f]) * (k - f)

    # ----------------------------
    # ENRIQUECIMIENTO EXTERNO (API RESTCOUNTRIES)
    # ----------------------------
    def enrich_with_country_data(self):
        """Agrega información externa (región, población) usando RestCountries API."""
        unique_countries = {u.country for u in self.users if u.country}
        country_data = {}

        for country in unique_countries:
            try:
                resp = requests.get(
                    f"https://restcountries.com/v3.1/name/{country}?fields=name,region,population",
                    timeout=30
                )
                if resp.status_code == 200:
                    info = resp.json()[0]
                    country_data[country] = {
                        "region": info.get("region", "N/A"),
                        "population": info.get("population", 0)
                    }
            except Exception as e:
                logger.warning(f"No se pudo obtener información para {country}: {e}")

        for u in self.users:
            u.region = country_data.get(u.country, {}).get("region", "N/A")
            u.population = country_data.get(u.country, {}).get("population", 0)

        logger.info("Datos de países enriquecidos con información de RestCountries.")

    # ----------------------------
    # ESTADÍSTICAS AVANZADAS
    # ----------------------------
    def compute_statistics(self) -> dict:
        """Calcula estadísticas agregadas avanzadas sobre los usuarios."""
        ages = [u.age for u in self.users]
        genders = [u.gender for u in self.users]
        countries = [u.country for u in self.users]
        domains = [getattr(u, "email_domain", "unknown") for u in self.users]
        regions = [getattr(u, "region", "N/A") for u in self.users]

        stats = {
            "total_users": len(self.users),
            "avg_age": round(_mean(ages), 2),
            "std_age": round(_pstdev(ages), 2),
            "q1_age": round(self._percentiles(ages, 25), 2),
            "median_age": round(_median(ages), 2),
            "q3_age": round(self._percentiles(ages, 75), 2),
            "gender_distribution": dict(Counter(genders)),
            "top_countries": dict(Counter(countries).most_common(10)),
            "top_email_domains": dict(Counter(domains).most_common(5)),
            "regions": dict(Counter(regions)),
        }

        logger.info(f"Estadísticas avanzadas calculadas: {stats}")
        return stats

    def get_users(self) -> list[User]:
        """Devuelve la lista de usuarios transformados."""
        return self.users
