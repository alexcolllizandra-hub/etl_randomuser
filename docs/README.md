# 🧑‍💻 Proyecto ETL RandomUser

## 🚦 ¿Qué es este proyecto?

Este repositorio despliega paso a paso un **proceso ETL** (Extracción, Transformación y Carga) utilizando Python y la API pública [RandomUser](https://randomuser.me/api/). Es 100% didáctico, ideal para practicar cómo crear pipelines ETL modernos, generando análisis y visualizaciones a partir de datos reales de usuarios internacionales.

---

## ❌ ¿Por qué NO se usan pandas, numpy ni statistics?

En este proyecto **NO se utilizan librerías avanzadas de análisis de datos como `pandas`, `numpy` ni siquiera la estándar `statistics`** para los cálculos matemáticos. Todos los cálculos y transformaciones (media, mediana, desviación estándar, percentiles) **se realizan "a mano", usando solo código Python básico**.

**¿Por qué este enfoque?**
- **Didáctico**: Obliga a entender realmente cada paso de la lógica ETL, ideal si eres principiante.
- **Transparencia total**: Puedes ver cómo se calcula cada estadística y transformar los datos línea a línea.
- **Portabilidad**: El código es portable y entendible incluso si alguna librería avanzada no está disponible.

**Ejemplo de cálculo manual en este proyecto:**
```python
# Cálculo manual de la media:
def _mean(data):
    return sum(data) / len(data) if data else 0.0
# Mediana, desviación estándar, percentiles... también están hechos así.
```

Puedes abrir los archivos `src/services/etl_service.py` y `src/services/transformer_service.py` para ver todos los cálculos hechos a "mano".

---

## 💡 ¿Qué hace exactamente este ETL?

- **Extract (Extracción):** Descarga cientos o miles de perfiles aleatorios (ficticios) usando la API RandomUser. Soporta hasta 5000 usuarios en una sola petición HTTP.
- **Transform (Transformación):**
  - Limpia los datos: filtra y elimina usuarios incompletos o incorrectos (sin email, sin país, edad inválida).
  - Calcula estadísticas básicas:** media/mediana/desviación estándar de la edad, distribución de género y país.
  - Aplica transformaciones avanzadas: 
    - Agrupa edades manualmente en rangos.
    - Detecta outliers sin ninguna librería de data science (utiliza el método estadístico IQR directamente implementado).
    - Enriquecimiento: consulta a otra API pública (RestCountries) para añadir información extra del país (población y región).
- **Load (Carga):**
  - Almacena el resultado como CSV y como base de datos SQLite, usando módulos propios muy sencillos.
- **Visualización:**
  - Genera gráficos automáticos (edades, géneros, países top, etc.) usando sólo `matplotlib` y `seaborn` (librerías populares para graficar en Python).

---

## 🧩 Explicación detallada de cada módulo y capa

**Todo el flujo está dividido en módulos fáciles de seguir.** Aquí tienes para principiantes cómo se "comunican":

- **main.py**: Es el "director de orquesta", ejecuta los pasos del proceso llamando a un "controlador".
- **controller/etl_controller.py**: Organiza y coordina todo el flujo ETL, de principio a fin. Su función clave es `run()`:
  1. Llama a la **extracción** (ETLService)
  2. Llama a la **limpieza** (ETLService)
  3. Obtiene estadísticas básicas (ETLService)
  4. Aplica transformaciones avanzadas (TransformerService)
  5. Llama a los cargadores (**loaders**) para guardar los datos en CSV y SQLite
  6. Ejecuta el módulo de **visualizaciones**
- **services/etl_service.py**: Hace la extracción (descarga desde la API), limpieza y estadísticas básicas (todo a mano).
- **services/transformer_service.py**: Aplica transformaciones más complejas (enriquecimiento, outlier, agrupaciones, percentiles) manualmente.
- **services/visualization_service.py**: Usa los datos para crear gráficos (distribución de edad, género, países...)
- **models/user_model.py**: Define cómo es cada usuario en Python (estructura de datos, usando un "dataclass").
- **loaders/csv_loader.py**/**sql_loader.py**: Guardan la información en archivos de la carpeta `data/`, cada uno en su formato.
- **utils/logger.py**: Solo para mejorar lo que ves por consola, para que entiendas en qué paso está el proceso.

---

### Ejemplo paso a paso (flujo de datos entre capas)

1. **main.py** → llama a `ETLController.run()`
2. **Extracción:**
   - Se descargan usuarios [ETLService.extract_users()]
3. **Limpieza:**
   - Se eliminan usuarios sin datos clave [ETLService.clean_users()]
4. **Transformación básica:**
   - Se calculan estadísticas manualmente (media, mediana, etc.) sin pandas/numPy/statistics
5. **Transformación avanzada:**
   - Se asignan grupos de edad manualmente, se detectan "outliers", se enriquece con datos externos usando otra API. Todo sin librerías externas de análisis.
6. **Carga:**
   - Los datos limpios y enriquecidos se escriben a disco en archivos CSV y base de datos SQLite (cada usuario es un registro)
7. **Visualización:**
   - Se generan los gráficos usando los datos ya preparados.

**En cada paso puedes seguir los datos y ver exactamente qué ocurre y cómo se implementa.**

---

## 🏁 Guía rápida para empezar desde cero

### Clona el repositorio

Puedes usar cualquier terminal, por ejemplo:

**En Windows:**
- Presiona `Win + R`, escribe `cmd` o `powershell` y presiona `Enter`
- O haz clic derecho en la carpeta y elige "Abrir Terminal aquí"

**En Mac/Linux:**
- Abre Terminal desde el menú de aplicaciones

Clona este proyecto ejecutando:
```bash
git clone https://github.com/alexcolllizandra-hub/etl_randomuser.git
cd etl_randomuser
```

---

### ⚙️ Instala Python y dependencias

1. **Asegúrate de tener Python 3.9 o superior instalado.**
   - Ve a [python.org](https://www.python.org/) si necesitas instalarlo.

2. **(Opcional, recomendable) Crea un entorno virtual:**
   ```bash
   python -m venv venv
   # Activa el entorno virtual:
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

### 🚀 Ejecuta el pipeline ETL

Desde la terminal, estando en la raíz del proyecto:

**En Windows:**
```bash
.\run_etl.bat
```

**En Linux/Mac:**
```bash
chmod +x run_etl.sh
./run_etl.sh
```

**Alternativa (funciona en todos los sistemas):**
```bash
# Windows PowerShell:
$env:PYTHONPATH="."; python src\main.py

# Linux/Mac:
PYTHONPATH=$(pwd) python src/main.py
```

Por defecto, descarga y procesa 100 usuarios (puedes ajustar el número modificando `main.py` o el parámetro en `ETLController.run()`).

---

## 🗂️ Estructura del repositorio

```
etl_randomuser/
│
├── src/
│   ├── main.py               # Punto de entrada: ejecuta todo el pipeline ETL y visualizaciones
│   ├── controller/
│   │   └── etl_controller.py # Orquesta todas las fases ETL y visualización
│   ├── services/
│   │   ├── etl_service.py        # Lógica de extracción y limpieza
│   │   ├── transformer_service.py# Transformaciones avanzadas (enriquecimientos, outliers, etc.)
│   │   └── visualization_service.py # Generación de gráficos
│   ├── loaders/
│   │   ├── csv_loader.py     # Guarda los datos como CSV
│   │   └── sql_loader.py     # Guarda los datos como SQLite
│   ├── models/
│   │   └── user_model.py     # Estructura de los usuarios
│   └── utils/
│       └── logger.py         # Log amigable por consola y archivo
│
├── data/         # Aquí se almacenan los resultados: CSV, DB y stats.json
├── plots/        # Carpeta con los gráficos PNG generados
├── logs/         # (opcional) Aquí se ubican los logs detallados si los configuras
├── requirements.txt       # Dependencias Python necesarias
├── run_etl.bat           # Script de ejecución para Windows
├── run_etl.sh            # Script de ejecución para Linux/Mac
├── run_pipeline.bat      # Pipeline completo con verificaciones (Windows)
├── run_pipeline.sh       # Pipeline completo con verificaciones (Linux/Mac)
├── VIEW_DASHBOARD.bat    # Abre el dashboard HTML (Windows)
├── VIEW_DASHBOARD.sh     # Abre el dashboard HTML (Linux/Mac)
├── dashboard.html        # Dashboard interactivo HTML
├── serve_dashboard.py    # Servidor HTTP para el dashboard
└── README.md
```

---

## 📈 ¿Qué obtendrás? (outputs)

Tras ejecutar el proyecto, encontrarás:

- `data/usuarios.csv` → Archivo CSV con toda la información procesada.
- `data/usuarios.db`  → Base de datos SQLite para análisis con otros programas.
- `data/stats.json` → Estadísticas en formato JSON para el dashboard.
- `plots/` → Carpeta con 5 gráficos PNG generados automáticamente.
- **Gráficos** (se abren automáticamente al final): distribución de edad, géneros, top países, etc.
- **Dashboard HTML** interactivo para visualizar todos los resultados.

### 🎨 Visualizar el Dashboard

Para ver todos los gráficos y estadísticas en un dashboard interactivo:

**Windows:**
```bash
VIEW_DASHBOARD.bat
```

**Linux/Mac:**
```bash
chmod +x VIEW_DASHBOARD.sh
./VIEW_DASHBOARD.sh
```

O ejecuta manualmente:
```bash
python serve_dashboard.py
```

Esto abrirá un navegador en `http://localhost:8000/dashboard.html` con un dashboard visual mostrando todas las visualizaciones generadas.

Mensajes típicos por consola:
```
🚀 Iniciando proceso ETL de usuarios...

🔹 Extrayendo usuarios...
🔹 Transformando datos...
🔹 Guardando resultados...
✅ Datos guardados en data/usuarios.csv
✅ Datos insertados correctamente en la base de datos.
✅ Proceso ETL completado con éxito.
```

---

## 🖥️ Consejos útiles y notas

- **Data reproducible:** la API RandomUser NO requiere registro ni clave.
- **Editor recomendado:** Funciona con PyCharm, VSCode o cualquier editor Python.
- **Salida configurada:** Puedes cambiar el nombre/ruta de CSV y DB, y ampliar el modelo de usuario fácilmente.
- **Extiéndelo:** Puedes añadir más transformadores, salidas (parquet, Excel, etc.), o visualizaciones nuevas.
- **Proyecto 100% modular y limpio**, ideal para didáctica y entrevistas técnicas.

---

## ⚡ Preguntas frecuentes

**¿Puedo aumentar el número de usuarios?**
Sí, en `src/main.py` puedes modificar `n_users=100` y poner, por ejemplo, 500 o 1000.

**¿Qué hago si quiero analizar otros campos?**
Extiende `user_model.py` (añade nuevos atributos al dataclass) y ajusta las transformaciones pertinentes.

**¿Y si quiero guardar en otro formato?**
Añade un nuevo loader en la carpeta `loaders/`.

**Error "ModuleNotFoundError: No module named 'services'"?**
Si ejecutas desde PyCharm funciona pero desde terminal falla, es un problema de PYTHONPATH. Usa los scripts `run_etl.bat` (Windows) o `run_etl.sh` (Linux/Mac), o ejecuta manualmente con:
```bash
# Windows:
$env:PYTHONPATH="."; python src\main.py
# Linux/Mac:
PYTHONPATH=$(pwd) python src/main.py
```

---
