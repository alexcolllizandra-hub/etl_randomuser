# Implementación del Proceso ETL

## 5.1. Extracción (Extract)

### Descripción de la API RandomUser

RandomUser API es una API REST gratuita que genera usuarios aleatorios ficticios para proyectos de desarrollo y testing. La elección de esta API se basó en su simplicidad de uso, ausencia de requisitos de autenticación y capacidad para generar datasets variados y realistas.

Las principales características que la convierten en una herramienta ideal para proyectos ETL incluyen la ausencia de autenticación requerida, la generación de datos realistas pero completamente ficticios que respetan la privacidad, su parametrización flexible mediante número de resultados y semilla para reproducibilidad, y una documentación completa disponible en https://randomuser.me/documentation.

### Extracción de datos

La API RandomUser permite solicitar hasta 5000 usuarios en una sola petición mediante una única llamada HTTP GET. Esta capacidad reduce significativamente el número de peticiones necesarias cuando se requiere trabajar con datasets grandes, optimizando el tiempo de extracción y minimizando la carga sobre el servidor.

El proceso de extracción se realiza mediante una petición HTTP utilizando la librería `requests` de Python. La respuesta del servidor es un objeto JSON estructurado que contiene todos los usuarios solicitados dentro de un campo denominado "results".

```python
url = f"https://randomuser.me/api/?results={n}"
if seed:
    url += f"&seed={seed}"

response = requests.get(url, timeout=30)
data = response.json().get("results", [])
users = [User.from_api(u) for u in data]
```

Este fragmento de código ilustra cómo se construye la URL de la API, incorporando el parámetro `seed` opcional cuando es proporcionado. El timeout de 30 segundos garantiza que las peticiones no se queden bloqueadas indefinidamente en caso de problemas de conectividad. La conversión de JSON a objetos `User` estructurados se realiza mediante list comprehension, aplicando el método `from_api()` a cada registro.

### Seed (Semilla) - Reproducibilidad

El parámetro `seed` constituye un mecanismo fundamental para garantizar la reproducibilidad en procesos de extracción de datos. Consiste en una cadena de texto que se envía a la API junto con los parámetros de solicitud, permitiendo que el servidor genere exactamente la misma secuencia de usuarios aleatorios en cada ejecución.

Sin el parámetro seed, cada llamada a la API devuelve una secuencia completamente diferente de usuarios, lo cual es adecuado para exploración inicial pero problemático cuando se requiere consistencia en los resultados. Con un seed específico, la API garantiza que el mismo seed produzca siempre el mismo conjunto de datos, independientemente del momento en que se realice la petición.

Las principales ventajas de utilizar seed incluyen la capacidad de realizar pruebas con datasets idénticos, facilitando la validación de cambios en el código, la obtención de resultados reproducibles en investigaciones académicas o profesionales, la reproducción de errores específicos durante el debugging al disponer exactamente de los mismos datos, y la presentación de ejemplos consistentes en demostraciones y documentación.

En el siguiente ejemplo se muestra la diferencia entre una extracción sin seed y con seed:

```python
# Sin seed - usuarios aleatorios diferentes en cada ejecución
users = extract_users(100)  

# Con seed - siempre los mismos usuarios para el mismo seed
users = extract_users(100, seed="proyecto_etl")
```

La implementación del parámetro seed se realiza de forma opcional mediante una comprobación condicional que agrega el parámetro a la URL únicamente cuando es proporcionado:

```python
def extract_users(self, n: int = 1000, seed: str = None) -> List[User]:
    url = f"https://randomuser.me/api/?results={n}"
    if seed:
        url += f"&seed={seed}"  # Agrega parámetro seed a la URL
```

### Ejemplo de Endpoint y Datos

Para ilustrar el funcionamiento de la API, consideremos una solicitud para obtener 1000 usuarios utilizando el seed "abc123". La URL completa tendría el siguiente formato:

```
https://randomuser.me/api/?results=1000&seed=abc123
```

La respuesta del servidor es un objeto JSON que contiene un campo "results" con un array de objetos, donde cada objeto representa un usuario con sus atributos correspondientes. A continuación se muestra un ejemplo simplificado de la estructura de respuesta:

```json
{
  "results": [
    {
      "gender": "male",
      "name": {"first": "John", "last": "Doe"},
      "location": {"country": "Spain"},
      "email": "john.doe@example.com",
      "dob": {"age": 35}
    },
    {
      "gender": "female",
      "name": {"first": "Jane", "last": "Smith"},
      "location": {"country": "United States"},
      "email": "jane.smith@example.com",
      "dob": {"age": 28}
    }
  ]
}
```

Esta estructura JSON se procesa mediante las siguientes líneas de código, que extraen el array de resultados y lo convierten en una lista de objetos User estructurados mediante el método estático `from_api()`:

```python
data = response.json().get("results", [])
users = [User.from_api(u) for u in data]
```

El resultado es una colección de objetos Python tipados que facilitan el trabajo posterior con los datos.

---

## 5.2. Transformación (Transform)

La fase de transformación constituye el núcleo del proceso ETL, donde los datos extraídos se validan, limpian, enriquecen y analizan para asegurar su calidad y utilidad para los análisis posteriores. Esta etapa se subdivide en varias operaciones que progresan desde la validación básica hasta el análisis estadístico avanzado.

### Limpieza de Datos

La limpieza de datos representa el primer paso crítico para garantizar la calidad del dataset. Durante este proceso se aplican validaciones estrictas a cada registro para identificar y eliminar aquellos que presentan información incompleta o inconsistente. Las reglas de validación implementadas son las siguientes:

1. El campo email debe contener un valor no vacío, garantizando que cada usuario tenga un identificador de correo electrónico válido.
2. La edad debe ser mayor que 0, eliminando valores inválidos o malformados que podrían comprometer los análisis estadísticos.
3. El país debe estar presente y no ser una cadena vacía, asegurando que cada usuario tenga asociada una ubicación geográfica.

```python
def clean_users(self, users: List[User]) -> List[User]:
    cleaned = [u for u in users if u.email and u.age > 0 and u.country]
    return cleaned
```

La función `clean_users` implementa estas validaciones mediante una list comprehension que filtra únicamente aquellos registros que cumplen simultáneamente con todas las condiciones. Este enfoque funcional garantiza una ejecución eficiente y un código legible. Como resultado de este proceso, se obtiene un conjunto de datos limpio y consistente, libre de registros incompletos o inválidos que podrían afectar la calidad de los análisis posteriores.

### Cálculo de Estadísticas sin Pandas

Una decisión de diseño fundamental del proyecto ha sido evitar el uso de librerías de análisis de datos como pandas o numpy, optando por implementar manualmente las funciones estadísticas necesarias. Este enfoque proporciona un control total sobre los cálculos realizados, mejora la comprensión de los algoritmos subyacentes y reduce las dependencias externas del proyecto.

Las estadísticas implementadas manualmente incluyen medidas de tendencia central y dispersión, así como análisis de frecuencias. A continuación se detallan las implementaciones de las principales funciones estadísticas:

#### Media Aritmética

La media aritmética es la suma de todos los valores dividida por el número de elementos. Su implementación aprovecha las funciones built-in de Python para obtener un código conciso:

```python
def _mean(data: list) -> float:
    return sum(data) / len(data) if data else 0.0
```

La expresión condicional previene la división por cero cuando la lista está vacía, devolviendo 0.0 en ese caso.

#### Mediana

La mediana representa el valor central de un conjunto de datos ordenados. Su cálculo requiere ordenar los datos y aplicar diferentes lógicas según si el número de elementos es par o impar:

```python
def _median(data: list) -> float:
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid-1] + sorted_data[mid]) / 2
    return sorted_data[mid]
```

En caso de número par de elementos, se toma el promedio de los dos valores centrales; en caso contrario, se selecciona directamente el valor medio.

#### Desviación Estándar Poblacional

La desviación estándar mide la dispersión de los datos respecto a la media. La implementación utiliza la fórmula poblacional (dividiendo por n en lugar de n-1):

```python
def _pstdev(data: list) -> float:
    mu = _mean(data)
    return (sum((x - mu) ** 2 for x in data) / n) ** 0.5
```

El cálculo se realiza en dos pasos: primero se computa la media, y posteriormente se aplica la raíz cuadrada de la suma de las diferencias al cuadrado dividida por el número de elementos.

Además de estas medidas estadísticas básicas, el sistema calcula automáticamente el mínimo y máximo de las edades, genera la distribución de frecuencias por género, y identifica los diez países con mayor representación en el dataset.

### Enriquecimiento con RestCountries API

El proceso de enriquecimiento añade información demográfica y geográfica externa a cada usuario mediante la integración con RestCountries API. Esta fase amplía significativamente el valor analítico del dataset al incorporar datos contextuales sobre los países de origen.

La API utilizada, disponible en https://restcountries.com/, proporciona acceso gratuito a información completa sobre países del mundo. Para optimizar el rendimiento, se solicitan únicamente los campos esenciales: nombre del país, región geográfica y población total.

Durante el proceso de enriquecimiento, se añaden dos nuevos campos a cada usuario: `region`, que identifica la región continental (Europa, América, Asia, etc.), y `population`, que contiene el número de habitantes del país según datos oficiales actualizados.

El flujo de enriquecimiento sigue una estrategia eficiente en tres etapas. Primero, se extraen los países únicos presentes en el conjunto de usuarios mediante un set comprehension, evitando consultas redundantes. Posteriormente, se realiza una petición HTTP a RestCountries por cada país único, almacenando los resultados en un diccionario temporal. Finalmente, se itera sobre todos los usuarios asignando la información correspondiente según su país de origen.

```python
def enrich_with_country_data(self):
    unique_countries = {u.country for u in self.users}
    country_data = {}
    
    for country in unique_countries:
        resp = requests.get(
            f"https://restcountries.com/v3.1/name/{country}?fields=name,region,population"
        )
        if resp.status_code == 200:
            country_data[country] = resp.json()[0]
    
    for u in self.users:
        u.region = country_data.get(u.country, {}).get("region", "N/A")
        u.population = country_data.get(u.country, {}).get("population", 0)
```

Esta implementación garantiza que, incluso si la API no devuelve información para algún país específico, el proceso continúa asignando valores por defecto sin interrumpir el flujo general.

### Detección de Outliers (Método IQR)

La detección de valores atípicos, también conocidos como outliers, es fundamental para identificar registros que se desvían significativamente del patrón general del dataset. Para este propósito se implementó el método IQR (Interquartile Range), ampliamente reconocido en estadística descriptiva por su robustez y simplicidad.

El método IQR se basa en el cálculo de tres medidas cuartílicas clave: Q1 representa el percentil 25, Q3 representa el percentil 75, e IQR se define como la diferencia entre Q3 y Q1. A partir de estas medidas, se establecen límites de normalidad mediante las fórmulas Q1 - 1.5×IQR (límite inferior) y Q3 + 1.5×IQR (límite superior). Cualquier valor que se encuentre fuera de este rango se considera un outlier.

```python
def detect_outliers(self):
    q1 = self._percentiles(ages, 25)
    q3 = self._percentiles(ages, 75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    
    for u in self.users:
        u.is_outlier = u.age < lower or u.age > upper
```

La implementación calcula los percentiles mediante una función auxiliar manual y marca cada usuario como outlier si su edad cae fuera del rango definido. Este campo booleano puede utilizarse posteriormente para análisis segmentados o para identificar posibles errores en los datos.

### Agrupación por Edad

Para facilitar análisis segmentados y comparativos, se implementó un sistema de clasificación automática de usuarios en grupos de edad predefinidos. Esta categorización permite realizar estudios demográficos más granular que el análisis de edades individuales.

Los rangos establecidos siguen categorías demográficas convencionales: menores de 18 años etiquetados como "Menores", de 18 a 30 años como "Jóvenes adultos", de 31 a 45 años como "Adultos", de 46 a 60 años como "Maduros", de 61 a 80 años como "Seniors", y mayores de 80 años como "Longevos".

La asignación de cada usuario a su grupo correspondiente se realiza mediante una serie de condicionales encadenadas que determinan la categoría según el valor de la edad. El resultado se almacena en un nuevo campo denominado `age_group`, que enriquece los registros con información categórica adicional para análisis posteriores.

---

## 5.3. Carga (Load)

La fase final del proceso ETL consiste en persistir los datos transformados en sistemas de almacenamiento adecuados para su posterior consulta y análisis. Se implementó una estrategia de almacenamiento dual, combinando la portabilidad del formato CSV con la potencia de consultas de SQLite.

### Almacenamiento en CSV

El archivo Comma-Separated Values (CSV) representa un formato universal de intercambio de datos tabulares, ampliamente soportado por herramientas de análisis y hojas de cálculo. El archivo se genera en la ruta `data/usuarios.csv` con codificación UTF-8 para garantizar la correcta representación de caracteres internacionales.

```python
with open(filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
```

La implementación utiliza el módulo `csv` estándar de Python, específicamente la clase `DictWriter` que permite escribir registros como diccionarios. Primero se escribe la fila de encabezados conteniendo los nombres de las columnas, y posteriormente se escriben todas las filas de datos mediante el método `writerows()`. El parámetro `newline=""` es requerido por Python para evitar la inserción de líneas en blanco adicionales en Windows.

### Almacenamiento en SQLite

La base de datos SQLite proporciona capacidades de consulta mediante SQL, permitiendo análisis más sofisticados que las operaciones lineales sobre CSV. El archivo se genera en `data/usuarios.db` como una base de datos autocontenida que no requiere servidor adicional.

La estructura de la tabla se define mediante DDL estándar:

```sql
CREATE TABLE IF NOT EXISTS users (
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    country TEXT,
    age INTEGER,
    email TEXT
)
```

Cada registro se inserta individualmente en la base de datos utilizando parámetros vinculados para prevenir inyecciones SQL:

```python
for u in data:
    cursor.execute(
        "INSERT INTO users (first_name, last_name, gender, country, age, email) VALUES (?, ?, ?, ?, ?, ?)",
        (u.get("first_name"), u.get("last_name"), u.get("gender"), 
         u.get("country"), u.get("age"), u.get("email"))
    )
conn.commit()
```

La utilización de placeholders `?` en lugar de interpolación de strings garantiza la seguridad y evita problemas con caracteres especiales. La transacción se confirma mediante `commit()` para asegurar la persistencia de los datos.

### Ejemplo de Registros

Tanto en CSV como en SQLite se almacenan los mismos datos, aunque en formatos distintos. Un ejemplo de representación CSV sería:

```csv
first_name,last_name,gender,country,age,email
John,Doe,male,Spain,35,john.doe@example.com
Jane,Smith,female,United States,28,jane.smith@example.com
```

En SQLite, la misma información se almacena de forma estructurada en una tabla relacional, permitiendo consultas complejas mediante SELECT, WHERE, GROUP BY y JOIN, entre otras operaciones SQL estándar.

La estrategia de doble almacenamiento ofrece ventajas complementarias: CSV facilita la importación directa en herramientas como Excel, Python o R sin configuración adicional, mientras que SQLite permite realizar consultas SQL complejas, agregaciones y relaciones entre tablas para análisis más profundos. Adicionalmente, mantener los datos en dos formatos proporciona redundancia y flexibilidad para elegir la herramienta más apropiada según el caso de uso específico.

---

## Resumen del Flujo Completo

El proceso ETL implementado sigue una secuencia estructurada que garantiza la calidad, trazabilidad y utilidad de los datos procesados. A continuación se presenta un resumen del flujo completo:

**1. EXTRACT (Extracción)**
   - Descarga de usuarios desde RandomUser API mediante peticiones HTTP
   - Soporte para hasta 5000 usuarios por petición
   - Parámetro seed opcional para reproducibilidad
   - Conversión de JSON a objetos User estructurados
   
**2. CLEAN (Limpieza)**
   - Validación de campos obligatorios (email, edad, país)
   - Eliminación de registros inválidos o incompletos
   - Logging de estadísticas de limpieza
   
**3. TRANSFORM BÁSICO (Transformación Básica)**
   - Cálculo manual de estadísticas descriptivas
   - Media, mediana, desviación estándar
   - Mínimo, máximo, distribuciones de frecuencias
   
**4. TRANSFORM AVANZADO (Transformación Avanzada)**
   - Enriquecimiento con datos de RestCountries API
   - Detección de outliers mediante método IQR
   - Agrupación por rangos de edad
   - Extracción de dominios de email
   - Estadísticas avanzadas con múltiples dimensiones
   
**5. LOAD (Carga)**
   - Exportación a archivo CSV con codificación UTF-8
   - Inserción en base de datos SQLite con SQL
   - Doble persistencia para redundancia
   
**6. VISUALIZE (Visualización)**
   - Generación automática de cinco gráficos estadísticos
   - Guardado en formato PNG con alta resolución
   - Distribuciones, comparativas y análisis correlacional

En conjunto, este flujo constituye un proceso ETL completo y reproducible, desarrollado íntegramente sin dependencias de pandas o numpy, utilizando únicamente bibliotecas estándar de Python y herramientas de análisis manuales que garantizan total control y comprensión del procesamiento de datos.

