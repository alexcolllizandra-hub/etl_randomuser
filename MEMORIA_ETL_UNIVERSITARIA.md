# 5. Implementación del Proceso ETL

El proceso ETL (Extract, Transform, Load) se desarrolló completamente en Python, sin el uso de librerías externas como pandas o numpy, con el objetivo de comprender y controlar cada una de las etapas del flujo de datos.

A continuación, describimos cada fase de forma detallada y natural, combinando explicación, ejemplos y fragmentos de código real extraídos del proyecto.

---

## 5.1. Extracción (Extract)

Para la fase de extracción utilizamos la API RandomUser, un servicio REST gratuito que genera datos de usuarios ficticios, ideal para proyectos de desarrollo y pruebas.

Entre sus principales características destacan:
- ✅ No requiere autenticación
- ✅ Genera datos realistas pero completamente ficticios
- ✅ Permite definir parámetros como número de resultados, páginas o seed (semilla)
- ✅ Disponible en: https://randomuser.me/documentation

### Paginación automática

El sistema descarga los usuarios por lotes de 500 registros por página, calculando automáticamente cuántas páginas son necesarias según el número total solicitado (n):

- **100 usuarios** → 1 página
- **1000 usuarios** → 2 páginas  
- **3500 usuarios** → 7 páginas

**Código 5.1. Implementación de paginación y seed en extract_users()**

```python
def extract_users(self, n: int = 1000, seed: str = None) -> List[User]:
    """Extrae usuarios desde la API RandomUser con paginación y seed."""
    users = []
    batch_size = 500
    pages = n // batch_size + (1 if n % batch_size else 0)
    
    seed_msg = f" con seed='{seed}'" if seed else ""
    logger.info(f"Iniciando extracción de {n} usuarios en {pages} páginas{seed_msg}...")
    
    for i in range(1, pages + 1):
        url = f"https://randomuser.me/api/?results={batch_size}&page={i}"
        if seed:
            url += f"&seed={seed}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json().get("results", [])
            users.extend([User.from_api(u) for u in data])
            logger.info(f"Página {i}/{pages} descargada: {len(data)} usuarios.")
        except Exception as e:
            logger.error(f"Error en la página {i}: {e}")
    
    logger.info(f"Total extraído: {len(users)} usuarios.")
    return users[:n]
```

### Parámetro Seed para reproducibilidad

Para garantizar reproducibilidad, empleamos el parámetro `seed`, que permite obtener los mismos resultados en ejecuciones posteriores. Esto resulta útil para testing, depuración y presentación de resultados consistentes.

**Ejemplo de uso:**
```python
# Sin seed → datos aleatorios cada vez
users = extract_users(100)

# Con seed → mismos usuarios en cada ejecución
users = extract_users(100, seed="proyecto_etl")
```

**Estructura del endpoint:**
```
https://randomuser.me/api/?results=500&page=1&seed=abc123
```

### Modelo de datos User

Cada respuesta devuelve un objeto JSON con información como nombre, género, país, correo y edad. Estos datos se transforman internamente en objetos `User` mediante el método `from_api()`.

**Código 5.2. Definición del modelo User y conversión desde JSON**

```python
@dataclass
class User:
    """Modelo que representa un usuario obtenido de la API RandomUser."""
    gender: str
    first_name: str
    last_name: str
    country: str
    age: int
    email: str
    
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

De este modo, la información se mantiene estructurada y lista para su posterior limpieza y transformación.

---

## 5.2. Transformación (Transform)

En esta etapa realizamos tareas de limpieza, validación, enriquecimiento y análisis de los datos obtenidos.

### 5.2.1. Limpieza y validación

Eliminamos los registros con datos incompletos o inconsistentes aplicando las siguientes reglas:
- ✅ El campo `email` no puede estar vacío
- ✅ La `age` debe ser mayor que 0
- ✅ El `country` no puede ser nulo

**Código 5.3. Función de limpieza de usuarios**

```python
def clean_users(self, users: List[User]) -> List[User]:
    """Limpia usuarios eliminando registros incompletos o inválidos."""
    cleaned = [u for u in users if u.email and u.age > 0 and u.country]
    logger.info(f"Limpieza completada: {len(cleaned)} usuarios válidos de {len(users)} totales.")
    return cleaned
```

### 5.2.2. Cálculo de estadísticas básicas

Dado que el proyecto no utiliza librerías de análisis de datos, las estadísticas se implementaron manualmente. Entre las funciones desarrolladas se incluyen:

#### Media aritmética

**Código 5.4. Implementación manual de la media**

```python
def _mean(data: list) -> float:
    return sum(data) / len(data) if data else 0.0
```

#### Mediana

**Código 5.5. Cálculo de la mediana sin librerías externas**

```python
def _median(data: list) -> float:
    n = len(data)
    if n == 0:
        return 0.0
    sorted_data = sorted(data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid-1] + sorted_data[mid]) / 2
    return sorted_data[mid]
```

#### Desviación estándar poblacional

**Código 5.6. Desviación estándar manual**

```python
def _pstdev(data: list) -> float:
    n = len(data)
    if n == 0:
        return 0.0
    mu = _mean(data)
    return (sum((x - mu) ** 2 for x in data) / n) ** 0.5
```

Además de estas estadísticas, calculamos distribución por género y el top 10 de países más frecuentes.

### 5.2.3. Enriquecimiento de datos

Con el fin de ampliar la información, integramos datos externos de la API RestCountries (https://restcountries.com/). Para cada país presente en los usuarios, obtuvimos dos atributos adicionales:
- **Región** (por ejemplo: Europa, Asia, América)
- **Población total** del país

**Código 5.7. Enriquecimiento con RestCountries API**

```python
def enrich_with_country_data(self):
    """Agrega información externa usando RestCountries API."""
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
```

### 5.2.4. Detección de valores atípicos

Para identificar posibles outliers en la edad, aplicamos el método **IQR (Interquartile Range)**, calculando los límites inferior y superior mediante los percentiles 25 (Q1) y 75 (Q3). Los usuarios con edades fuera de ese rango se marcaron como atípicos.

**Código 5.8. Detección de outliers con IQR**

```python
def detect_outliers(self):
    """Detecta valores atípicos usando el método IQR."""
    ages = [u.age for u in self.users]
    if not ages:
        logger.warning("No hay datos para detectar outliers.")
        return
        
    q1 = self._percentiles(ages, 25)
    q3 = self._percentiles(ages, 75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    
    for u in self.users:
        u.is_outlier = u.age < lower or u.age > upper
    
    n_outliers = sum(u.is_outlier for u in self.users)
    logger.info(f"Detectados {n_outliers} outliers de edad (método IQR).")
```

### 5.2.5. Agrupación por rangos de edad

Cada usuario se clasificó en un grupo de edad según el siguiente esquema:

- **<18**: Menores
- **18-30**: Jóvenes adultos
- **31-45**: Adultos
- **46-60**: Maduros
- **61-80**: Seniors
- **80+**: Longevos

**Código 5.9. Clasificación en grupos de edad**

```python
def enrich_data(self):
    """Crea nuevas columnas: grupos de edad y dominio de email."""
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
```

Este campo adicional (`age_group`) permitió realizar análisis estadísticos más detallados por categoría.

---

## 5.3. Carga (Load)

En la fase final, los datos transformados se almacenaron en dos formatos complementarios: un archivo CSV y una base de datos SQLite.

### 5.3.1. Exportación a CSV

El archivo `data/usuarios.csv` contiene todos los registros en formato UTF-8, con encabezados y separación por comas.

**Código 5.10. Guardado de datos en formato CSV**

```python
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
```

Este formato facilita la importación directa en herramientas como Excel, Python o R.

### 5.3.2. Inserción en SQLite

Además, creamos una base de datos local `data/usuarios.db` con la tabla `users` definida de la siguiente forma:

**Código 5.11. Definición del esquema de la base de datos**

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

Los registros se insertaron por lotes, garantizando un proceso eficiente y seguro.

**Código 5.12. Inserción de datos en SQLite**

```python
def load(self, data: List[Dict[str, Any]], output_dir: str) -> None:
    if not data:
        logger.warning("No hay datos para exportar en SQL.")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    db_path = os.path.join(output_dir, self.db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
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
    
    for u in data:
        cursor.execute("""
            INSERT INTO users (first_name, last_name, gender, country, age, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            u.get("first_name"),
            u.get("last_name"),
            u.get("gender"),
            u.get("country"),
            u.get("age"),
            u.get("email"),
        ))
    
    conn.commit()
    conn.close()
    logger.info(f"Datos insertados correctamente en {db_path}")
```

De este modo, los datos pueden consultarse mediante SQL o exportarse nuevamente según las necesidades del análisis.

### 5.3.3. Visualización de resultados

Finalmente, generamos cinco gráficos de análisis estadístico que se guardaron automáticamente en la carpeta `plots/`:

1. **Distribución de edades** - Histograma con KDE
2. **Distribución por género** - Gráfico de barras
3. **Top países** - Top 10 países con más usuarios
4. **Edad por país** - Boxplot de distribución
5. **Matriz de correlación** - Correlaciones entre variables numéricas

**Código 5.13. Generación de visualizaciones**

```python
def plot_age_distribution(self, users: list[User]) -> None:
    if not users:
        print("No hay datos para generar gráfico de distribución de edades.")
        return
    df = pd.DataFrame([u.__dict__ for u in users])
    plt.figure(figsize=(8, 5))
    sns.histplot(df["age"], bins=15, kde=True, color="#1f77b4")
    plt.title("Distribución de Edades")
    plt.xlabel("Edad")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    filepath = os.path.join(self.output_dir, "distribucion_edades.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado en: {filepath}")
    plt.show()
```

Cada gráfico se guarda con resolución de 300 DPI y se muestra también en pantalla para verificación inmediata.

---

## Resumen del flujo completo

El proceso ETL implementado sigue esta secuencia:

**1. EXTRACT** 
   - Descarga de usuarios desde RandomUser API (paginación y seed opcional)
   - Conversión de JSON a objetos User

**2. CLEAN**
   - Validación de campos obligatorios (email, edad, país)
   - Eliminación de registros inválidos

**3. TRANSFORM BÁSICO**
   - Cálculo de estadísticas descriptivas (manual, sin pandas/numpy)
   - Media, mediana, desviación estándar
   - Distribución por género y países

**4. TRANSFORM AVANZADO**
   - Enriquecimiento con datos de RestCountries API
   - Detección de outliers (método IQR)
   - Agrupación por rango de edad

**5. LOAD**
   - Exportación a archivo CSV
   - Inserción en base de datos SQLite

**6. VISUALIZE**
   - Generación de cinco gráficos en formato PNG para análisis visual

En conjunto, este flujo constituye un proceso ETL completo y reproducible, desarrollado íntegramente con herramientas estándar de Python y sin dependencias de análisis de datos externas, garantizando claridad, eficiencia y trazabilidad en cada etapa del procesamiento.

---

## Consideraciones técnicas

- **Timeout de conexión**: 30 segundos por defecto para evitar interrupciones
- **Manejo de errores**: Validaciones en cada fase para robustez
- **Logging**: Sistema de logs centralizado para seguimiento del proceso
- **Modularidad**: Separación clara de responsabilidades por capas
- **Multiplataforma**: Compatible con Windows, Linux y macOS

