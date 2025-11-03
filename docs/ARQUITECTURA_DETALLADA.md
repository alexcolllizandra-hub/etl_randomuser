# 4. Arquitectura y Diseño del Sistema

## 4.1. Estructura de Carpetas y Archivos

El código fuente se organiza de manera modular, separando las capas de control, servicios, modelos de datos y utilidades generales:

```
etl_randomuser/
│
├── src/                          # Código fuente principal
│   ├── main.py                   # Punto de entrada del sistema
│   ├── config.py                 # Configuración centralizada
│   │
│   ├── controller/               # Controladores
│   │   └── etl_controller.py    # Orquesta el flujo ETL completo
│   │
│   ├── services/                 # Lógica de negocio
│   │   ├── etl_service.py        # Extracción y transformación básica
│   │   ├── transformer_service.py # Transformación avanzada
│   │   └── visualization_service.py # Generación de gráficos
│   │
│   ├── models/                   # Modelos de datos
│   │   └── user_model.py         # Modelo User (dataclass)
│   │
│   ├── loaders/                  # Carga de datos (herencia)
│   │   ├── base_loader.py        # Clase abstracta BaseLoader
│   │   ├── csv_loader.py         # Implementación para CSV
│   │   └── sql_loader.py         # Implementación para SQLite
│   │
│   └── utils/                    # Utilidades
│       └── logger.py             # Configuración de logging
│
├── dashboard/                    # Dashboard HTML interactivo
│   └── dashboard.html
│
├── data/                         # Datos generados por ejecución
│   ├── usuarios.csv              # Exportación en formato CSV
│   ├── usuarios.db               # Base de datos SQLite
│   └── stats.json                # Estadísticas para dashboard
│
├── plots/                        # Gráficos generados
│   ├── distribucion_edades.png
│   ├── distribucion_genero.png
│   ├── top_paises.png
│   └── ... (8 gráficos totales)
│
├── logs/                         # Registro de ejecución
│   └── etl.log                   # Logs del proceso ETL
│
├── scripts_project/              # Scripts de ejecución
│   ├── run_etl_with_tests.py    # Pipeline con verificaciones
│   ├── serve_dashboard.py        # Servidor HTTP del dashboard
│   └── ...
│
├── docs/                         # Documentación
│   ├── ARQUITECTURA.md           # Este archivo
│   ├── EXPLICACION_ETL.md        # Detalles técnicos del ETL
│   └── MEMORIA_ETL_UNIVERSITARIA.md # Documento académico
│
├── requirements.txt              # Dependencias Python
├── PIPELINE.bat/.sh              # Scripts de ejecución completa
└── README.md                     # Documentación principal
```

Esta jerarquía modular refleja un diseño multicapa típico de un sistema ETL, donde cada carpeta representa una capa funcional del flujo.

---

## 4.2. Componentes Principales

### a) main.py - Punto de Entrada

El archivo `main.py` actúa como el punto único de entrada al sistema. Inicializa el entorno de ejecución y ejecuta el pipeline completo mediante una única llamada.

**Código 4.1. Implementación de main.py**

```python
def main():
    """Ejecuta el proceso ETL completo."""
    print("Iniciando proceso ETL de usuarios...\n")
    
    # Instanciamos el controlador principal
    controller = ETLController()
    
    # Ejecutamos el pipeline (1000 usuarios por defecto)
    controller.run(n_users=1000)
    
    print("\nProceso ETL finalizado con éxito.")

if __name__ == "__main__":
    main()
```

**Funciones**:
- Carga configuración centralizada desde `config.py`
- Inicializa el sistema de logging global mediante `utils/logger.py`
- Ejecuta el flujo ETL definido en el controlador
- Garantiza reproducibilidad y registro del proceso

---

### b) Configuración (config.py)

El módulo `config.py` centraliza todos los parámetros del sistema, permitiendo adaptar el comportamiento sin modificar el código fuente.

**Código 4.2. Configuración centralizada en config.py**

```python
# ==============================================================================
# URLs DE APIs
# ==============================================================================
RANDOMUSER_API_URL = "https://randomuser.me/api/"
RESTCOUNTRIES_API_URL = "https://restcountries.com/v3.1/name/{country}"
RESTCOUNTRIES_FIELDS = "fields=name,region,population"

# ==============================================================================
# PARÁMETROS DE EXTRACCIÓN
# ==============================================================================
DEFAULT_N_USERS = 1000            # Usuarios a extraer por defecto
MAX_USERS_PER_REQUEST = 5000      # Límite de RandomUser API
API_TIMEOUT = 30                  # Timeout HTTP (segundos)

# ==============================================================================
# ARCHIVOS Y DIRECTORIOS
# ==============================================================================
CSV_FILENAME = "usuarios.csv"
SQLITE_FILENAME = "usuarios.db"
STATS_FILENAME = "stats.json"

DATA_DIR = "data"
PLOTS_DIR = "plots"
DASHBOARD_DIR = "dashboard"

# ==============================================================================
# FUNCIONES HELPER
# ==============================================================================
def build_randomuser_url(n_users: int = None, seed: str = None) -> str:
    """Construye la URL completa para la API RandomUser."""
    n_users = n_users or DEFAULT_N_USERS
    url = f"{RANDOMUSER_API_URL}?results={n_users}"
    if seed:
        url += f"&seed={seed}"
    return url
```

**Ventajas**:
- ✅ Centralización de configuración
- ✅ Fácil modificación sin tocar código de negocio
- ✅ Funciones helper reutilizables
- ✅ Buenas prácticas de ingeniería de software

---

### c) Controller - Orquestación

El controlador (`controller/etl_controller.py`) coordina la ejecución completa del pipeline ETL, implementando el flujo secuencial de las fases: **Extract → Transform → Load → Visualize**.

**Código 4.3. Orquestación del proceso ETL**

```python
class ETLController:
    """Controlador principal del flujo ETL completo."""

    def __init__(self):
        self.etl_service = ETLService()
        self.visualizer = VisualizationService(output_dir=self.plots_dir)
        
    def run(self, n_users: int = 1000, seed: str = None):
        # 1. Extracción y limpieza
        users = self.etl_service.extract_users(n_users, seed=seed)
        users = self.etl_service.clean_users(users)
        
        # 2. Transformación avanzada
        transformer = TransformerService(users)
        transformer.enrich_data()
        transformer.detect_outliers()
        transformer.enrich_with_country_data()
        advanced_stats = transformer.compute_statistics()
        
        # 3. Carga de datos
        data_dicts = [u.__dict__ for u in users]
        CSVLoader("usuarios.csv").load(data_dicts, self.output_dir)
        SQLLoader("usuarios.db").load(data_dicts, self.output_dir)
        
        # 4. Visualizaciones
        self.visualizer.plot_age_distribution(users)
        self.visualizer.plot_gender_distribution(users)
        # ... 6 gráficos adicionales
        
        logger.info("=== Proceso ETL completado con éxito ===")
```

**Responsabilidades**:
- Invocar los servicios en el orden correcto
- Gestionar directorios de salida (data, plots)
- Controlar excepciones y registrar mensajes
- Garantizar coherencia entre fases
- Actuar como capa de abstracción entre main.py y servicios

---

### d) Services - Lógica de Negocio

La carpeta `services/` implementa la lógica funcional principal, donde cada servicio encapsula un conjunto de operaciones específicas.

#### d.1) ETLService - Extracción Básica

**Código 4.4. Extracción de usuarios de la API**

```python
class ETLService:
    """Servicio ETL: extracción y transformación básica."""

    def extract_users(self, n: int = None, seed: str = None) -> List[User]:
        """Extrae usuarios desde la API RandomUser."""
        n = n or DEFAULT_N_USERS
        url = build_randomuser_url(n_users=n, seed=seed)
        
        response = requests.get(url, timeout=API_TIMEOUT)
        data = response.json().get("results", [])
        users = [User.from_api(u) for u in data]
        
        logger.info(f"Extracción completada: {len(users)} usuarios.")
        return users
    
    def clean_users(self, users: List[User]) -> List[User]:
        """Limpia usuarios eliminando registros inválidos."""
        cleaned = [u for u in users if u.email and u.age > 0 and u.country]
        return cleaned
```

#### d.2) TransformerService - Transformación Avanzada

**Código 4.5. Transformaciones estadísticas manuales**

```python
class TransformerService:
    """Transformaciones avanzadas sin pandas/numpy."""

    def enrich_data(self):
        """Agrega campos derivados: grupos de edad, categorías, dominios."""
        for u in self.users:
            # Clasificación de grupo de edad
            if u.age < 18:
                age_group = "<18"
                age_category = "Adolescente"
            elif u.age < 30:
                age_group = "18-30"
                age_category = "Joven Adulto"
            # ... más categorías
            
            u.age_group = age_group
            u.age_category = age_category
            u.email_domain = u.email.split("@")[-1]
    
    def detect_outliers(self):
        """Detecta outliers usando método IQR."""
        ages = [u.age for u in self.users]
        q1, q3 = self._percentiles(ages, 25), self._percentiles(ages, 75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        
        for u in self.users:
            u.is_outlier = u.age < lower or u.age > upper
    
    def compute_statistics(self) -> dict:
        """Calcula estadísticas avanzadas: CV, IQR, percentiles."""
        ages = [u.age for u in self.users]
        cv_age = round((_pstdev(ages) / _mean(ages)) * 100, 2)
        
        return {
            "total_users": len(self.users),
            "avg_age": round(_mean(ages), 2),
            "cv_age": cv_age,  # Coeficiente de variación
            "iqr_age": round(q3 - q1, 2),
            "gender_distribution": dict(Counter(genders)),
            "top_countries": dict(Counter(countries).most_common(10)),
        }
```

**Cálculos implementados manualmente** (sin pandas/numpy):
- Media, mediana, desviación estándar
- Cuartiles (Q1, Q3) y IQR
- Coeficiente de variación (CV)
- Detección de outliers por método IQR
- Contadores y distribuciones

#### d.3) VisualizationService - Gráficos

**Código 4.6. Generación de visualizaciones**

```python
class VisualizationService:
    """Generación de gráficos con matplotlib."""

    def plot_age_distribution(self, users: list[User]):
        """Histograma de distribución de edades."""
        ages = [u.age for u in users]
        plt.figure(figsize=(8, 5))
        plt.hist(ages, bins=15, color="#1f77b4", edgecolor="black", alpha=0.7)
        plt.title("Distribución de Edades")
        plt.xlabel("Edad")
        plt.ylabel("Frecuencia")
        plt.savefig(os.path.join(self.output_dir, "distribucion_edades.png"), dpi=300)
        plt.show()
    
    def plot_correlation_matrix(self, users: list[User]):
        """Matriz de correlación edad/género."""
        # Cálculo manual de correlación
        # Visualización con imshow
        pass
```

**Gráficos generados** (8 totales):
1. Distribución de Edades (histograma)
2. Distribución por Género (barras)
3. Top 10 Países (barras horizontales)
4. Edad por País (boxplots)
5. Matriz de Correlación (heatmap)
6. Distribución por Regiones (barras)
7. Grupos de Edad (pie chart)
8. Género por País (barras apiladas)

---

### e) Loaders - Herencia y Polimorfismo

La carpeta `loaders/` implementa el patrón de herencia para la carga de datos, donde todas las clases derivan de una clase abstracta común `BaseLoader`.

**Jerarquía de herencia**:
```
BaseLoader (Abstract Class)
    ├── CSVLoader
    └── SQLLoader
```

**Código 4.7. Clase abstracta BaseLoader**

```python
from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """Interfaz base para todas las clases de carga de datos."""

    @abstractmethod
    def load(self, data: Any, output_dir: str) -> None:
        """Carga los datos a un destino (archivo, base de datos, etc.)"""
        pass
```

**Código 4.8. Implementación de CSVLoader**

```python
class CSVLoader(BaseLoader):
    """Carga datos en un archivo CSV."""

    def __init__(self, filename: str = "users.csv") -> None:
        self.filename = filename

    def load(self, data: List[Dict[str, Any]], output_dir: str) -> None:
        """Escribe datos en formato CSV con UTF-8."""
        filepath = os.path.join(output_dir, self.filename)
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"Datos guardados correctamente en {filepath}")
```

**Código 4.9. Implementación de SQLLoader**

```python
class SQLLoader(BaseLoader):
    """Carga los datos en una base de datos SQLite."""

    def load(self, data: List[Dict[str, Any]], output_dir: str) -> None:
        """Almacena registros en SQLite con inserciones por lotes."""
        db_path = os.path.join(output_dir, self.db_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                first_name TEXT,
                last_name TEXT,
                gender TEXT,
                country TEXT,
                age INTEGER,
                email TEXT
            )
        """)

        # Inserciones por lotes
        for u in data:
            cursor.execute("""
                INSERT INTO users (first_name, last_name, gender, country, age, email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (u.get("first_name"), u.get("last_name"), u.get("gender"),
                  u.get("country"), u.get("age"), u.get("email")))

        conn.commit()
        conn.close()
        logger.info(f"Datos insertados correctamente en {db_path}")
```

**Uso polimórfico desde el controlador**:

```python
# El controlador puede usar cualquier loader sin conocer implementación
loaders = [
    CSVLoader("usuarios.csv"),
    SQLLoader("usuarios.db")
]

for loader in loaders:
    loader.load(data_dicts, output_dir)  # Polimorfismo en acción
```

**Beneficios del diseño**:
- ✅ **Polimorfismo**: Tratamiento uniforme de todos los loaders
- ✅ **Extensibilidad**: Fácil agregar JSONLoader, XMLLoader, etc.
- ✅ **Reutilización**: Interfaz común elimina duplicación
- ✅ **Principio Open/Closed**: Abierto a extensión, cerrado a modificación

---

### f) Models - Dataclasses

La carpeta `models/` define la estructura de datos usando el decorador `@dataclass` de Python.

**Código 4.10. Modelo User con dataclass**

```python
from dataclasses import dataclass

@dataclass
class User:
    """Modelo que representa un usuario obtenido de la API RandomUser."""
    gender: str
    first_name: str
    last_name: str
    country: str
    age: int
    email: str
    
    # Atributos derivados (enriquecimiento)
    age_group: str = ""
    age_category: str = ""
    email_domain: str = ""
    email_preference: str = ""
    is_outlier: bool = False
    region: str = ""
    population: int = 0

    @staticmethod
    def from_api(data: dict) -> "User":
        """Convierte el JSON de la API en una instancia de User."""
        return User(
            gender=data.get("gender", ""),
            first_name=data.get("name", {}).get("first", ""),
            last_name=data.get("name", {}).get("last", ""),
            country=data.get("location", {}).get("country", ""),
            age=data.get("dob", {}).get("age", 0),
            email=data.get("email", "")
        )
```

**Ventajas de usar `@dataclass`**:
- ✅ Generación automática de `__init__()`, `__repr__()`, `__eq__()`
- ✅ Tipado estático para mayor seguridad
- ✅ Código más limpio y legible
- ✅ Compatible con type hints

**Ejemplo de uso**:

```python
# Creación desde JSON de la API
user = User.from_api({
    "gender": "male",
    "name": {"first": "John", "last": "Doe"},
    "location": {"country": "Spain"},
    "dob": {"age": 35},
    "email": "john@example.com"
})

# Acceso a atributos
print(user.first_name)  # "John"
print(user.age)         # 35
print(user.__dict__)    # Convierte a diccionario para loaders
```

---

### g) Utils - Utilidades Transversales

El módulo `utils/` provee funcionalidades transversales utilizadas en todo el proyecto.

**Código 4.11. Configuración de logging centralizada**

```python
import logging
import os

def setup_logger(name: str) -> logging.Logger:
    """Configura un logger con archivo y consola."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formateador con timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para archivo
    os.makedirs("src/logs", exist_ok=True)
    file_handler = logging.FileHandler("src/logs/etl.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
```

**Uso en el proyecto**:

```python
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
logger.info("Extracción completada: 1000 usuarios.")
logger.error("Error en la extracción: timeout")
```

---

## 4.3. Pipeline ETL y Flujo de Ejecución

El sistema sigue un flujo automatizado y secuencial que refleja la naturaleza de un pipeline ETL:

**Código 4.12. Flujo completo del pipeline**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INICIALIZACIÓN                                           │
│    main.py carga configuración y lanza ETLController        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. EXTRACCIÓN (ETLService)                                  │
│    - Petición HTTP a RandomUser API                         │
│    - Conversión JSON → objetos User                         │
│    - Validación y limpieza de datos                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. TRANSFORMACIÓN (TransformerService)                      │
│    - Enriquecimiento: grupos de edad, categorías            │
│    - Detección de outliers (método IQR)                     │
│    - Enriquecimiento con RestCountries API                  │
│    - Cálculo de estadísticas (CV, IQR, percentiles)         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. CARGA (Loaders)                                          │
│    CSVLoader  → usuarios.csv                                │
│    SQLLoader  → usuarios.db                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. VISUALIZACIÓN (VisualizationService)                     │
│    - 8 gráficos PNG generados en plots/                     │
│    - Dashboard HTML con estadísticas                        │
└─────────────────────────────────────────────────────────────┘
```

**Ejemplo de log de ejecución**:

```
2025-11-03 20:47:10 - INFO - === Iniciando proceso ETL extendido ===
2025-11-03 20:47:10 - INFO - Iniciando extracción de 1000 usuarios...
2025-11-03 20:47:11 - INFO - Extracción completada: 1000 usuarios.
2025-11-03 20:47:11 - INFO - Limpieza completada: 1000 usuarios válidos
2025-11-03 20:47:11 - INFO - Datos enriquecidos: grupos de edad agregados
2025-11-03 20:47:11 - INFO - Detectados 25 outliers de edad (método IQR)
2025-11-03 20:47:58 - INFO - Datos guardados en usuarios.csv
2025-11-03 20:47:58 - INFO - Datos insertados en usuarios.db
2025-11-03 20:48:19 - INFO - === Proceso ETL completado con éxito ===
```

---

## 4.4. Dashboard HTML

Como etapa final, el sistema genera un dashboard HTML interactivo que sintetiza los resultados del proceso ETL.

**Características**:
- 📊 Estadísticas agregadas: total usuarios, edad promedio, distribución por género
- 📈 Visualizaciones integradas: 8 gráficos PNG embebidos
- 🔗 Enlaces a archivos: CSV, SQLite, gráficos
- 📱 Responsive: compatible con móviles y escritorio
- ⚡ Auto-actualizable: se regenera en cada ejecución

**Generación automática**: El dashboard se crea dinámicamente desde `stats.json` y los gráficos de `plots/`, proporcionando una vista consolidada del análisis.

---

## 4.5. Principios de Diseño Aplicados

El sistema se ha desarrollado siguiendo principios SOLID y buenas prácticas de ingeniería de software:

### 4.5.1. Principios SOLID

| Principio | Aplicación en el Proyecto |
|-----------|---------------------------|
| **Single Responsibility** | Cada módulo tiene una responsabilidad única: Controller orquesta, Services procesan, Loaders guardan |
| **Open/Closed** | BaseLoader permite extender con nuevos loaders sin modificar código existente |
| **Liskov Substitution** | CSVLoader y SQLLoader son intercambiables (polimorfismo) |
| **Interface Segregation** | BaseLoader define solo el método necesario `load()` |
| **Dependency Inversion** | Controller depende de abstracciones (BaseLoader), no de implementaciones |

### 4.5.2. Conceptos OOP

**Herencia**:
```python
BaseLoader → CSVLoader, SQLLoader
```

**Polimorfismo**:
```python
loader.load(data, output_dir)  # Funciona con cualquier implementación
```

**Encapsulación**:
```python
class TransformerService:
    def __init__(self, users):
        self.users = users  # Estado encapsulado
    
    def compute_statistics(self):  # Interfaz pública
        return {...}
```

**Abstracción**:
```python
class BaseLoader(ABC):
    @abstractmethod
    def load(self, data, output_dir):  # Interface abstracta
        pass
```

**Composición**:
```python
class ETLController:
    def __init__(self):
        self.etl_service = ETLService()        # Composición
        self.visualizer = VisualizationService() # Composición
```

---

## 4.6. Ventajas de la Arquitectura

### 4.6.1. Mantenibilidad
- Código organizado por responsabilidades claras
- Fácil localizar y modificar funcionalidades específicas
- Separación entre configuración y lógica de negocio

### 4.6.2. Escalabilidad
- Añadir nuevos loaders sin modificar código existente
- Integrar nuevas APIs solo requiere modificar Services
- Extensible a nuevos tipos de visualizaciones

### 4.6.3. Testabilidad
- Componentes aislados permiten testing unitario
- Mock de servicios facilita testing del controlador
- Logger configurable para testing automatizado

### 4.6.4. Reutilización
- `config.py` centraliza configuración global
- `BaseLoader` elimina duplicación de código
- Servicios independientes reutilizables

### 4.6.5. Portabilidad
- Sin dependencias pesadas (pandas, numpy eliminados)
- Compatible con Windows/Linux/Mac
- Ejecutable en VMs (Debian 12, Ubuntu)

---

## 4.7. Comparación con Arquitecturas Tradicionales

| Aspecto | Arquitectura Tradicional | Nuestra Arquitectura |
|---------|-------------------------|---------------------|
| **Dependencias** | pandas, numpy, seaborn | Solo requests, matplotlib |
| **Cálculos** | Librerías externas | Implementación manual |
| **Configuración** | Dispersa en el código | Centralizada en config.py |
| **Loaders** | Implementación directa | Patrón herencia/polimorfismo |
| **Testing** | Difícil por acoplamiento | Fácil por modularidad |

---

## Conclusión

La arquitectura implementada proporciona una **base sólida, escalable y mantenible**, adecuada tanto para proyectos educativos como para entornos reales de análisis y automatización de datos. La combinación de **principios OOP modernos, separación de responsabilidades y configuración centralizada** garantiza un código profesional, extensible y fácil de mantener.

