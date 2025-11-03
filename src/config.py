"""
config.py
---------
Configuración centralizada del proyecto ETL.
Contiene todas las URLs, parámetros y constantes.
"""

# ==============================================================================
# URLs DE APIs
# ==============================================================================

# API RandomUser - Genera usuarios aleatorios
RANDOMUSER_API_URL = "https://randomuser.me/api/"

# API RestCountries - Información sobre países
RESTCOUNTRIES_API_URL = "https://restcountries.com/v3.1/name/{country}"
RESTCOUNTRIES_FIELDS = "fields=name,region,population"

# ==============================================================================
# PARÁMETROS DE EXTRACCIÓN
# ==============================================================================

# Número de usuarios a extraer por defecto
DEFAULT_N_USERS = 1000

# Número máximo de usuarios que permite RandomUser API en una sola petición
MAX_USERS_PER_REQUEST = 5000

# Semilla para reproducibilidad (opcional)
DEFAULT_SEED = None

# Timeout para peticiones HTTP (segundos)
API_TIMEOUT = 30

# ==============================================================================
# ARCHIVOS Y DIRECTORIOS
# ==============================================================================

# Nombres de archivos de salida
CSV_FILENAME = "usuarios.csv"
SQLITE_FILENAME = "usuarios.db"
STATS_FILENAME = "stats.json"

# Directorios relativos desde la raíz del proyecto
DATA_DIR = "data"
PLOTS_DIR = "plots"
DASHBOARD_DIR = "dashboard"

# ==============================================================================
# PARÁMETROS DE TRANSFORMACIÓN
# ==============================================================================

# Grupos de edad
AGE_GROUPS = {
    "ADOLESCENTE": {"max": 18, "label": "<18"},
    "JOVEN_ADULTO": {"min": 18, "max": 30, "label": "18-30"},
    "ADULTO_JOVEN": {"min": 30, "max": 45, "label": "31-45"},
    "ADULTO_MADURO": {"min": 45, "max": 60, "label": "46-60"},
    "SENIOR": {"min": 60, "max": 80, "label": "61-80"},
    "LONGEVO": {"min": 80, "label": "80+"}
}

# Dominios de email populares para clasificación
POPULAR_EMAIL_DOMAINS = [
    'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'outlook.com'
]

# Coeficiente IQR para detección de outliers
OUTLIER_IQR_COEFFICIENT = 1.5

# ==============================================================================
# PARÁMETROS DE VISUALIZACIÓN
# ==============================================================================

# DPI para guardado de gráficos
PLOT_DPI = 300

# Tamaño de figura para gráficos
PLOT_FIGSIZE = {
    "DEFAULT": (8, 5),
    "WIDE": (10, 6),
    "LARGE": (12, 8)
}

# Color principal para gráficos
PLOT_COLOR = "#1f77b4"

# ==============================================================================
# PARÁMETROS DEL DASHBOARD
# ==============================================================================

# Puerto del servidor HTTP
DASHBOARD_PORT = 8000

# Host del servidor HTTP
DASHBOARD_HOST = "localhost"

# URL completa del dashboard
DASHBOARD_URL = f"http://{DASHBOARD_HOST}:{DASHBOARD_PORT}/dashboard/dashboard.html"

# ==============================================================================
# TOP N PARA ESTADÍSTICAS
# ==============================================================================

TOP_COUNTRIES_COUNT = 10
TOP_EMAIL_DOMAINS_COUNT = 5

# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

def build_randomuser_url(n_users: int = None, seed: str = None) -> str:
    """
    Construye la URL completa para la API RandomUser.
    
    Args:
        n_users: Número de usuarios a extraer
        seed: Semilla para reproducibilidad
        
    Returns:
        URL completa con parámetros
    """
    n_users = n_users or DEFAULT_N_USERS
    url = f"{RANDOMUSER_API_URL}?results={n_users}"
    
    if seed:
        url += f"&seed={seed}"
    
    return url


def build_restcountries_url(country: str) -> str:
    """
    Construye la URL completa para la API RestCountries.
    
    Args:
        country: Nombre del país
        
    Returns:
        URL completa con parámetros
    """
    return f"https://restcountries.com/v3.1/name/{country}?{RESTCOUNTRIES_FIELDS}"
