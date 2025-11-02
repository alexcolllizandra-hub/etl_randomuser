# Implementación del Proceso ETL

## 5.1. Extracción (Extract)

### Descripción de la API RandomUser

**RandomUser API** es una API REST gratuita que genera usuarios aleatorios ficticios para proyectos de desarrollo y testing.

**Características principales:**
- ✅ Sin autenticación requerida
- ✅ Datos realistas pero ficticios
- ✅ Parametrizable: número de resultados, paginación, seed
- ✅ Documentación: https://randomuser.me/documentation

### Results y Paginación

**Paginación automática:**
- El sistema descarga lotes de 500 usuarios por página
- Calcula automáticamente cuántas páginas necesita según `n`
- Ejemplo: 100 usuarios = 1 página, 1000 usuarios = 2 páginas, 3500 usuarios = 7 páginas

**Código de paginación:**
```python
batch_size = 500
pages = n // batch_size + (1 if n % batch_size else 0)

for i in range(1, pages + 1):
    url = f"https://randomuser.me/api/?results={batch_size}&page={i}"
    # ... descarga de datos
```

### Seed (Semilla) - Reproducibilidad

**¿Qué es el Seed?**
- Un parámetro de texto que garantiza reproducibilidad
- **Sin seed**: cada ejecución devuelve usuarios completamente diferentes
- **Con seed**: siempre devuelve la misma secuencia de usuarios

**Beneficios:**
- 🔬 **Testing**: Mismo dataset para pruebas
- 📊 **Investigación**: Resultados reproducibles
- 🐛 **Debugging**: Mismo dato para reproducir errores
- 📈 **Presentaciones**: Ejemplos consistentes

**Ejemplo de uso:**
```python
# Sin seed - aleatorio cada vez
users = extract_users(100)  

# Con seed - siempre mismo resultado
users = extract_users(100, seed="proyecto_etl")
```

**Implementación:**
```python
def extract_users(self, n: int = 1000, seed: str = None) -> List[User]:
    for i in range(1, pages + 1):
        url = f"https://randomuser.me/api/?results={batch_size}&page={i}"
        if seed:
            url += f"&seed={seed}"  # Agrega parámetro seed a la URL
```

### Ejemplo de Endpoint y Datos

**Endpoint:**
```
https://randomuser.me/api/?results=500&page=1&seed=abc123
```

**Respuesta JSON:**
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

**Procesamiento:**
```python
data = response.json().get("results", [])
users = [User.from_api(u) for u in data]
# Convierte JSON → objetos User estructurados
```

---

## 5.2. Transformación (Transform)

### Limpieza de Datos

**Validaciones aplicadas:**
1. ✅ Email no vacío
2. ✅ Edad > 0 (datos válidos)
3. ✅ País no vacío

**Código:**
```python
def clean_users(self, users: List[User]) -> List[User]:
    cleaned = [u for u in users if u.email and u.age > 0 and u.country]
    return cleaned
```

**Resultado:** Elimina registros incompletos o inválidos

### Cálculo de Estadísticas sin Pandas

**Implementación manual de estadísticas:**

#### Media Aritmética
```python
def _mean(data: list) -> float:
    return sum(data) / len(data) if data else 0.0
```

#### Mediana
```python
def _median(data: list) -> float:
    sorted_data = sorted(data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid-1] + sorted_data[mid]) / 2
    return sorted_data[mid]
```

#### Desviación Estándar Poblacional
```python
def _pstdev(data: list) -> float:
    mu = _mean(data)
    return (sum((x - mu) ** 2 for x in data) / n) ** 0.5
```

**Estadísticas calculadas:**
- Media, Mediana, Desviación estándar
- Mínimo, Máximo
- Distribución de género
- Top 10 países

### Enriquecimiento con RestCountries API

**¿Qué hace?**
Agrega información demográfica y geográfica externa a cada usuario.

**API usada:** https://restcountries.com/
- Obtiene región y población por país
- Campos añadidos: `region`, `population`

**Flujo:**
1. Obtiene países únicos de los usuarios
2. Consulta RestCountries por cada país
3. Enriquece cada usuario con datos del país

**Código:**
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

### Detección de Outliers (Método IQR)

**Método IQR (Interquartile Range):**
- Q1: percentil 25
- Q3: percentil 75
- IQR = Q3 - Q1
- Límites: Q1 - 1.5×IQR y Q3 + 1.5×IQR

**Implementación manual:**
```python
def detect_outliers(self):
    q1 = self._percentiles(ages, 25)
    q3 = self._percentiles(ages, 75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    
    for u in self.users:
        u.is_outlier = u.age < lower or u.age > upper
```

### Agrupación por Edad

**Rangos definidos:**
- `<18`: Menores
- `18-30`: Jóvenes adultos
- `31-45`: Adultos
- `46-60`: Maduros
- `61-80`: Seniors
- `80+`: Longevos

**Campo agregado:** `age_group`

---

## 5.3. Carga (Load)

### Almacenamiento en CSV

**Archivo:** `data/usuarios.csv`

**Implementación:**
```python
with open(filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
```

**Formato:** Comma-Separated Values estándar UTF-8

### Almacenamiento en SQLite

**Base de datos:** `data/usuarios.db`

**Estructura de la tabla:**
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

**Insertado por lotes:**
```python
for u in data:
    cursor.execute(
        "INSERT INTO users (first_name, last_name, gender, country, age, email) VALUES (?, ?, ?, ?, ?, ?)",
        (u.get("first_name"), u.get("last_name"), u.get("gender"), 
         u.get("country"), u.get("age"), u.get("email"))
    )
conn.commit()
```

### Ejemplo de Registros

**CSV:**
```csv
first_name,last_name,gender,country,age,email
John,Doe,male,Spain,35,john.doe@example.com
Jane,Smith,female,United States,28,jane.smith@example.com
```

**SQLite:** Mismas columnas, consultable con SQL

**Ventajas:**
- 📊 CSV: Fácil importar a Excel, Python, R
- 💾 SQLite: Queries SQL complejas, relaciones
- 🔄 Doble respaldo: dos formatos para análisis

---

## Resumen del Flujo Completo

```
1. EXTRACT
   ↓ API RandomUser (paginación + seed opcional)
   ↓ JSON → objetos User
   
2. CLEAN
   ↓ Validación (email, age, country)
   ↓ Eliminar inválidos
   
3. TRANSFORM BÁSICO
   ↓ Estadísticas descriptivas (manual)
   ↓ Media, mediana, std dev
   
4. TRANSFORM AVANZADO
   ↓ Enriquecimiento (RestCountries API)
   ↓ Detección outliers (IQR)
   ↓ Agrupación por edad
   ↓ Estadísticas avanzadas
   
5. LOAD
   ↓ Guardar CSV
   ↓ Guardar SQLite
   
6. VISUALIZE
   ↓ 5 gráficos generados
   ↓ Guardados como PNG
```

**Total:** ETL completo sin pandas/numpy, 100% implementado manualmente con Python estándar.

