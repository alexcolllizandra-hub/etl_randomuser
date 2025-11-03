# 4.2. Arquitectura del Proyecto

## Diagrama de Módulos

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│                    (Punto de entrada)                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ETLController                                │
│  (Orquesta el flujo completo del proceso ETL)                  │
└───────────┬─────────────┬───────────────┬──────────────────────┘
            │             │               │
            ▼             ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  ETLService     │ │ TransformerSvc  │ │ VisualizationSvc │
│  (Extract)      │ │  (Transform)    │ │   (Visualizar)   │
└─────────────────┘ └─────────────────┘ └──────────────────┘
            │             │
            ▼             ▼
┌───────────────────────────────────────────────────────────────┐
│                      Loaders                                   │
│  ┌───────────────┐      ┌───────────────┐                   │
│  │  CSVLoader    │      │  SQLLoader    │                   │
│  │  (CSV)        │      │  (SQLite)     │                   │
│  └───────────────┘      └───────────────┘                   │
│         ↕                      ↕                             │
│  ┌───────────────────────────────────────┐                  │
│  │      BaseLoader (Abstract Class)      │                  │
│  └───────────────────────────────────────┘                  │
└───────────────────────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────┐
│                      Storage                                   │
│  ┌─────────────────┐      ┌─────────────────┐               │
│  │  usuarios.csv   │      │  usuarios.db    │               │
│  └─────────────────┘      └─────────────────┘               │
└───────────────────────────────────────────────────────────────┘
```

## Estructura de Carpetas y Archivos

```
etl_randomuser/
│
├── src/                          # Código fuente principal
│   ├── main.py                   # Punto de entrada del programa
│   ├── config.py                 # Configuración centralizada
│   │
│   ├── controller/               # Controladores
│   │   └── etl_controller.py     # Orquesta el flujo ETL completo
│   │
│   ├── services/                 # Lógica de negocio
│   │   ├── etl_service.py        # Extracción y transformación básica
│   │   ├── transformer_service.py # Transformación avanzada
│   │   └── visualization_service.py # Generación de gráficos
│   │
│   ├── models/                   # Modelos de datos
│   │   └── user_model.py         # Modelo User (dataclass)
│   │
│   ├── loaders/                  # Carga de datos
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
├── data/                         # Datos generados
│   ├── usuarios.csv
│   ├── usuarios.db
│   └── stats.json
│
├── plots/                        # Gráficos generados
│
├── scripts_project/              # Scripts de ejecución
│   ├── run_etl_with_tests.py
│   ├── serve_dashboard.py
│   └── ...
│
├── docs/                         # Documentación
│   ├── ARQUITECTURA.md           # Este archivo
│   ├── README.md
│   ├── EXPLICACION_ETL.md
│   └── ...
│
└── requirements.txt              # Dependencias Python
```

## Breve Explicación de Cada Componente

### Controller (Controladores)

**Responsabilidad**: Coordinación y orquestación del flujo completo del proceso ETL.

**Componentes**:
- `ETLController`: Controlador principal que invoca todos los servicios en el orden correcto

**Funciones principales**:
- Inicializar y configurar los servicios necesarios
- Ejecutar las fases ETL en secuencia (Extract → Transform → Load)
- Gestionar directorios de salida (data, plots)
- Coordinar la generación de visualizaciones

**Código de ejemplo**:
```python
class ETLController:
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
        
        # 3. Carga de datos
        CSVLoader("usuarios.csv").load(data_dicts, self.output_dir)
        SQLLoader("usuarios.db").load(data_dicts, self.output_dir)
        
        # 4. Visualizaciones
        self.visualizer.plot_age_distribution(users)
```

---

### Services (Servicios)

**Responsabilidad**: Contener la lógica de negocio específica de cada fase del ETL.

**Componentes**:
1. **ETLService**: Extracción básica y transformaciones iniciales
   - `extract_users()`: Descarga usuarios de la API RandomUser
   - `clean_users()`: Valida y limpia datos inválidos
   - `transform_users()`: Calcula estadísticas básicas (media, mediana, desviación estándar)

2. **TransformerService**: Transformaciones avanzadas y enriquecimiento
   - `enrich_data()`: Agrega campos derivados (grupos de edad, categorías, dominios)
   - `detect_outliers()`: Detecta valores atípicos usando método IQR
   - `enrich_with_country_data()`: Enriquece con datos de RestCountries API
   - `compute_statistics()`: Calcula estadísticas avanzadas (CV, IQR, percentiles)

3. **VisualizationService**: Generación de gráficos
   - `plot_age_distribution()`: Histograma de edades
   - `plot_gender_distribution()`: Distribución por género
   - `plot_top_countries()`: Top 10 países
   - `plot_age_by_country()`: Boxplots de edad por país
   - `plot_correlation_matrix()`: Matriz de correlación
   - Y 3 gráficos adicionales

**Código de ejemplo**:
```python
class ETLService:
    def extract_users(self, n: int = None, seed: str = None) -> List[User]:
        url = build_randomuser_url(n_users=n, seed=seed)
        response = requests.get(url, timeout=API_TIMEOUT)
        data = response.json().get("results", [])
        return [User.from_api(u) for u in data]
```

---

### Loaders (Cargadores)

**Responsabilidad**: Gestionar la persistencia de datos en diferentes formatos.

**Componentes**:
1. **BaseLoader**: Clase abstracta base que define la interfaz común
2. **CSVLoader**: Implementación para guardar datos en CSV
3. **SQLLoader**: Implementación para guardar datos en SQLite

**Patrón utilizado**: Template Method / Strategy

**Código de ejemplo**:
```python
# Clase abstracta base
class BaseLoader(ABC):
    @abstractmethod
    def load(self, data: Any, output_dir: str) -> None:
        pass

# Implementación para CSV
class CSVLoader(BaseLoader):
    def load(self, data: List[Dict[str, Any]], output_dir: str) -> None:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

# Implementación para SQLite
class SQLLoader(BaseLoader):
    def load(self, data: List[Dict[str, Any]], output_dir: str) -> None:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (...)")
        # ... inserts
```

---

### Utils (Utilidades)

**Responsabilidad**: Proporcionar funcionalidades transversales utilizadas en todo el proyecto.

**Componentes**:
- `logger.py`: Configuración centralizada de logging usando el módulo `logging` de Python

**Funciones principales**:
- Configurar nivel de logging (INFO, DEBUG, ERROR)
- Formatear mensajes de log con timestamps
- Crear archivos de log en carpeta dedicada

**Código de ejemplo**:
```python
import logging
import os

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formateador
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

---

## Herencia y Programación Orientada a Objetos (OOP)

### Patrón de Herencia en Loaders

El proyecto utiliza **herencia** para implementar el patrón de diseño **Template Method**, donde una clase abstracta define la estructura común y las clases hijas implementan los detalles específicos.

#### Jerarquía de Herencia

```
BaseLoader (Abstract Class)
    ├── CSVLoader
    └── SQLLoader
```

#### Beneficios de este Diseño

1. **Polimorfismo**: El controlador puede tratar todos los loaders de forma uniforme
2. **Extensibilidad**: Fácil agregar nuevos tipos de loaders (JSON, XML, etc.)
3. **Reutilización**: La interfaz común evita duplicación de código
4. **Mantenimiento**: Cambios en la interfaz se propagan automáticamente

#### Código de Ejemplo del Uso Polimórfico

```python
# El controlador puede usar cualquier loader sin conocer su implementación
def load_data(data):
    loaders = [
        CSVLoader("usuarios.csv"),
        SQLLoader("usuarios.db")
    ]
    
    for loader in loaders:
        loader.load(data, output_dir)  # Polimorfismo en acción
```

### Otros Conceptos OOP Utilizados

1. **Encapsulación**: Atributos privados mediante convenciones (`self.`) y métodos públicos
2. **Abstracción**: `BaseLoader` es una clase abstracta que define qué hacer, no cómo
3. **Composición**: `ETLController` compone múltiples servicios (ETL, Transformer, Visualizer)
4. **Dataclasses**: El modelo `User` usa `@dataclass` para automatizar `__init__`, `__repr__`, etc.

#### Ejemplo de Encapsulación y Abstracción

```python
class TransformerService:
    def __init__(self, users: list[User]):
        self.users = users  # Estado encapsulado
    
    def enrich_data(self):
        """Interfaz pública"""
        for u in self.users:
            u.age_group = self._classify_age(u.age)  # Método privado conceptual
    
    def _classify_age(self, age: int) -> str:
        """Implementación interna (privada por convención)"""
        if age < 30:
            return "18-30"
        elif age < 45:
            return "31-45"
        # ...
```

### Resumen de Principios OOP Aplicados

| Principio | Ejemplo | Beneficio |
|-----------|---------|-----------|
| **Herencia** | `CSVLoader extends BaseLoader` | Reutilización, polimorfismo |
| **Abstracción** | `BaseLoader` con métodos abstractos | Interface común, oculta complejidad |
| **Encapsulación** | Atributos `self.users` en servicios | Control de acceso, modularidad |
| **Polimorfismo** | `loader.load()` funciona con cualquier implementación | Código flexible, extensible |
| **Composición** | `ETLController` usa múltiples servicios | Separación de responsabilidades |

---

## Flujo de Datos Completo

```
1. main.py
   ↓
2. ETLController.run()
   ↓
3. ETLService.extract_users() → Lista de objetos User
   ↓
4. ETLService.clean_users() → Lista de objetos User validados
   ↓
5. ETLService.transform_users() → Estadísticas básicas
   ↓
6. TransformerService.enrich_data() → Usuarios con campos derivados
   ↓
7. TransformerService.detect_outliers() → Usuarios marcados
   ↓
8. TransformerService.enrich_with_country_data() → Usuarios enriquecidos
   ↓
9. TransformerService.compute_statistics() → Estadísticas avanzadas
   ↓
10. CSVLoader.load() → usuarios.csv generado
    ↓
11. SQLLoader.load() → usuarios.db generado
    ↓
12. VisualizationService.plot_*() → Gráficos PNG generados
    ↓
13. Dashboard HTML muestra los resultados
```

---

## Ventajas de esta Arquitectura

### 1. **Separación de Responsabilidades**
Cada componente tiene una responsabilidad única y bien definida:
- Controller → Orquestación
- Services → Lógica de negocio
- Loaders → Persistencia
- Utils → Funcionalidades transversales

### 2. **Modularidad**
Los módulos son independientes y pueden modificarse sin afectar otros:
- Cambiar SQLite por PostgreSQL solo afecta a `SQLoader`
- Agregar nuevos gráficos solo modifica `VisualizationService`

### 3. **Extensibilidad**
Fácil agregar nuevas funcionalidades:
- Nuevo loader: crear clase que extienda `BaseLoader`
- Nueva visualización: añadir método a `VisualizationService`
- Nueva transformación: agregar servicio o método existente

### 4. **Testabilidad**
Los componentes pueden testearse de forma aislada:
- Mock de `ETLService` para testear `ETLController`
- Test unitarios de cada loader independientemente

### 5. **Reutilización**
El código común se comparte:
- `BaseLoader` elimina duplicación entre loaders
- `config.py` centraliza configuración global

---

## Configuración Centralizada

El archivo `src/config.py` contiene todas las constantes, URLs y parámetros del proyecto:

```python
# URLs de APIs
RANDOMUSER_API_URL = "https://randomuser.me/api/"
RESTCOUNTRIES_API_URL = "https://restcountries.com/v3.1/name/{country}"

# Parámetros
DEFAULT_N_USERS = 1000
API_TIMEOUT = 30

# Archivos
CSV_FILENAME = "usuarios.csv"
SQLITE_FILENAME = "usuarios.db"

# Funciones helper
def build_randomuser_url(n_users: int = None, seed: str = None) -> str:
    # Construye la URL completa
    pass
```

**Ventajas**: Fácil cambiar configuración sin tocar código de negocio, centralización, mejor mantenimiento.

---

## Conclusión

Esta arquitectura sigue principios SOLID y patrones de diseño OOP modernos, resultando en un código:
- ✅ **Mantenible**: Fácil entender y modificar
- ✅ **Escalable**: Creciente sin complejidad innecesaria
- ✅ **Testeable**: Componentes aislados y mockeables
- ✅ **Reutilizable**: Interfaces comunes y abstracciones bien definidas

