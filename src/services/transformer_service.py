import requests
from collections import Counter
from src.models.user_model import User
from src.utils.logger import setup_logger
from src.config import API_TIMEOUT, POPULAR_EMAIL_DOMAINS, OUTLIER_IQR_COEFFICIENT, TOP_COUNTRIES_COUNT, TOP_EMAIL_DOMAINS_COUNT, build_restcountries_url

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
        """Crea nuevas columnas derivadas: grupos de edad, dominio de email y categorías."""
        for u in self.users:
            # Clasificación de grupo de edad
            if u.age < 18:
                age_group = "<18"
                age_category = "Adolescente"
            elif u.age < 30:
                age_group = "18-30"
                age_category = "Joven Adulto"
            elif u.age < 45:
                age_group = "31-45"
                age_category = "Adulto Joven"
            elif u.age < 60:
                age_group = "46-60"
                age_category = "Adulto Maduro"
            elif u.age < 80:
                age_group = "61-80"
                age_category = "Senior"
            else:
                age_group = "80+"
                age_category = "Longevo"

            u.age_group = age_group
            u.age_category = age_category
            u.email_domain = u.email.split("@")[-1] if "@" in u.email else "unknown"
            
            # Calcular índice simulado de preferencia de email (basado en dominio)
            # Dominios comunes = mayor preferencia
            u.email_preference = "Popular" if u.email_domain in POPULAR_EMAIL_DOMAINS else "Otro"

        logger.info("Datos enriquecidos: grupos de edad, categorías, dominios y preferencias agregados.")




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
        lower, upper = q1 - OUTLIER_IQR_COEFFICIENT * iqr, q3 + OUTLIER_IQR_COEFFICIENT * iqr

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
                    build_restcountries_url(country),
                    timeout=API_TIMEOUT
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
        age_groups = [getattr(u, "age_group", "unknown") for u in self.users]

        # Calcular coeficiente de variación (CV = std / mean)
        cv_age = round((_pstdev(ages) / _mean(ages)) * 100, 2) if _mean(ages) > 0 else 0

        stats = {
            "total_users": len(self.users),
            "avg_age": round(_mean(ages), 2),
            "median_age": round(_median(ages), 2),
            "std_age": round(_pstdev(ages), 2),
            "min_age": min(ages) if ages else 0,
            "max_age": max(ages) if ages else 0,
            "cv_age": cv_age,
            "q1_age": round(self._percentiles(ages, 25), 2),
            "q3_age": round(self._percentiles(ages, 75), 2),
            "iqr_age": round(self._percentiles(ages, 75) - self._percentiles(ages, 25), 2),
            "gender_distribution": dict(Counter(genders)),
            "top_countries": dict(Counter(countries).most_common(TOP_COUNTRIES_COUNT)),
            "top_email_domains": dict(Counter(domains).most_common(TOP_EMAIL_DOMAINS_COUNT)),
            "regions": dict(Counter(regions)),
            "age_groups": dict(Counter(age_groups)),
        }

        logger.info(f"Estadísticas avanzadas calculadas: {stats}")
        return stats

    def get_users(self) -> list[User]:
        """Devuelve la lista de usuarios transformados."""
        return self.users
