# 🔧 Guía de Scripts y Pipelines

Esta guía explica todos los scripts de ejecución disponibles en el proyecto y cómo utilizarlos.

---

## 📋 Índice

1. [Pipeline Principal](#pipeline-principal)
2. [Scripts Individuales](#scripts-individuales)
3. [Estructura de Ejecución](#estructura-de-ejecución)
4. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🚀 Pipeline Principal

### `PIPELINE.bat` / `PIPELINE.sh`

**Ubicación:** Raíz del proyecto  
**Descripción:** Pipeline completo que ejecuta las 3 fases del proyecto en secuencia.

**¿Qué hace?**
1. ✅ **Ejecuta el ETL** - Extrae, transforma y carga datos de usuarios
2. ✅ **Verifica resultados** - Comprueba CSV, SQLite y gráficos
3. ✅ **Inicia Dashboard** - Abre el dashboard interactivo en el navegador

**Uso:**
```bash
# Windows
PIPELINE.bat

# Linux/Mac
chmod +x PIPELINE.sh
./PIPELINE.sh
```

**Características:**
- Configura automáticamente PYTHONPATH
- Muestra progreso en tiempo real
- Abre el dashboard en `http://localhost:8000`
- Manejo de errores: se detiene si alguna fase falla
- Encoding UTF-8 configurado para caracteres especiales

---

## 🛠️ Scripts Individuales

### 1. `scripts_project/run_etl.bat` / `run_etl.sh`

**Descripción:** Ejecuta solo el proceso ETL (sin verificaciones ni dashboard).

**¿Qué hace?**
- Extrae usuarios de la API RandomUser
- Limpia y valida los datos
- Calcula estadísticas básicas y avanzadas
- Genera campos derivados (grupos de edad, outliers, etc.)
- Enriquece con datos de RestCountries API
- Guarda resultados en CSV y SQLite
- Genera 5 gráficos estadísticos
- Crea `stats.json` para el dashboard

**Archivos generados:**
- `data/usuarios.csv` - Datos en formato CSV
- `data/usuarios.db` - Base de datos SQLite
- `data/stats.json` - Estadísticas para el dashboard
- `plots/*.png` - 5 gráficos PNG

**Uso:**
```bash
# Windows
scripts_project\run_etl.bat

# Linux/Mac
chmod +x scripts_project/run_etl.sh
./scripts_project/run_etl.sh
```

---

### 2. `scripts_project/run_etl_with_tests.py`

**Descripción:** Ejecuta el ETL y luego verifica todos los resultados.

**¿Qué hace?**
1. **Ejecuta el ETL** (a menos que uses `--skip-etl`)
2. **Verifica archivo CSV:**
   - Comprueba que existe
   - Cuenta total de líneas
   - Verifica formato
3. **Verifica base de datos SQLite:**
   - Lista tablas
   - Muestra estructura de columnas
   - Cuenta registros
   - Distribución por género
   - Top 5 países
   - Estadísticas de edad
   - Consultas complejas (rangos de edad)
   - Integridad de datos (emails, edades, países)
4. **Verifica gráficos:**
   - Comprueba existencia de los 5 PNG
   - Muestra tamaño de archivos

**Modo `--skip-etl`:**
Omite la ejecución del ETL y solo realiza verificaciones.

**Uso:**
```bash
# Pipeline completo (ETL + verificaciones)
python scripts_project\run_etl_with_tests.py

# Solo verificaciones (saltar ETL)
python scripts_project\run_etl_with_tests.py --skip-etl

# Forma corta
python scripts_project\run_etl_with_tests.py -s
```

**Resultado esperado:**
```
✓ Proceso ETL completado exitosamente
✓ Archivo CSV verificado
✓ Tabla users encontrada
✓ Total de usuarios: 100
✓ 5 gráficos generados
✓ PIPELINE COMPLETADO EXITOSAMENTE
```

---

### 3. `scripts_project/serve_dashboard.py`

**Descripción:** Inicia un servidor HTTP local para visualizar el dashboard HTML.

**¿Qué hace?**
- Configura servidor HTTP en puerto 8000
- Sirve archivos estáticos (HTML, PNG, JSON)
- Habilita CORS para recursos locales
- Abre automáticamente el navegador
- Muestra logs de peticiones

**Uso:**
```bash
python scripts_project\serve_dashboard.py
```

**URLs disponibles:**
- Dashboard: `http://localhost:8000/dashboard/dashboard.html`
- Gráficos: `http://localhost:8000/plots/*.png`
- Stats: `http://localhost:8000/data/stats.json`

**Detener el servidor:** `Ctrl+C`

---

### 4. `scripts_project/VIEW_DASHBOARD.bat` / `VIEW_DASHBOARD.sh`

**Descripción:** Script simple para abrir solo el dashboard.

**¿Qué hace?**
- Llama a `serve_dashboard.py`
- Abre el dashboard en el navegador
- Espera hasta que presiones una tecla

**Uso:**
```bash
# Windows
scripts_project\VIEW_DASHBOARD.bat

# Linux/Mac
chmod +x scripts_project/VIEW_DASHBOARD.sh
./scripts_project/VIEW_DASHBOARD.sh
```

---

### 5. `scripts_project/run_pipeline.bat` / `run_pipeline.sh`

**Descripción:** Pipeline antiguo (ahora usar `PIPELINE.bat` en la raíz).

**Nota:** Estos scripts están en `scripts_project/` pero la versión recomendada está en la raíz como `PIPELINE.bat` y `PIPELINE.sh`.

---

## 📊 Estructura de Ejecución

### Flujo Completo (PIPELINE.bat)

```
PIPELINE.bat
    │
    ├─→ [1/3] ETL
    │   ├─→ python -m src.main
    │   ├─→ Extrae datos de API
    │   ├─→ Transforma datos
    │   ├─→ Guarda CSV + SQLite
    │   ├─→ Genera gráficos
    │   └─→ Crea stats.json
    │
    ├─→ [2/3] Verificaciones
    │   ├─→ run_etl_with_tests.py --skip-etl
    │   ├─→ Verifica CSV
    │   ├─→ Verifica SQLite
    │   └─→ Verifica gráficos
    │
    └─→ [3/3] Dashboard
        ├─→ serve_dashboard.py
        ├─→ Inicia servidor HTTP:8000
        ├─→ Abre navegador
        └─→ Dashboard interactivo
```

### Ejecución Individual

```
┌─────────────────────────────────────┐
│  Ejecutar SOLO ETL                  │
│  run_etl.bat / run_etl.sh           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Ejecutar ETL + Verificaciones      │
│  run_etl_with_tests.py              │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Verificar SIN ejecutar ETL         │
│  run_etl_with_tests.py --skip-etl   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Ver SOLO Dashboard                 │
│  VIEW_DASHBOARD.bat / .sh           │
└─────────────────────────────────────┘
```

---

## 📖 Ejemplos de Uso

### Escenario 1: Ejecutar Todo por Primera Vez

```bash
# Ejecutar el pipeline completo
PIPELINE.bat

# Resultado:
# - Datos extraídos y procesados
# - Archivos generados (CSV, DB, PNG)
# - Verificaciones completadas
# - Dashboard abierto en el navegador
```

### Escenario 2: Solo Ver los Resultados (ya ejecutado ETL)

```bash
# Si ya ejecutaste el ETL antes
scripts_project\VIEW_DASHBOARD.bat

# Abre solo el dashboard con los datos existentes
```

### Escenario 3: Verificar Datos Existentes

```bash
# Verificar que los datos estén correctos
python scripts_project\run_etl_with_tests.py --skip-etl

# Muestra estadísticas detalladas sin ejecutar ETL
```

### Escenario 4: Ejecutar ETL con Más Usuarios

Modificar `src/main.py`:
```python
# Cambiar de 100 a 1000 usuarios
controller.run(n_users=1000)
```

Luego ejecutar:
```bash
PIPELINE.bat
```

### Escenario 5: Uso en CI/CD o Automatización

```bash
# Pipeline silencioso sin dashboard
python -m src.main
python scripts_project\run_etl_with_tests.py --skip-etl

# Si todo OK, continúa con el siguiente paso
# Si falla, termina con código de error
```

---

## 🔍 Detalles Técnicos

### Configuración de PYTHONPATH

Todos los scripts configuran automáticamente `PYTHONPATH` para que Python encuentre los módulos del proyecto:

**Windows:**
```batch
set PYTHONPATH=%cd%
```

**Linux/Mac:**
```bash
export PYTHONPATH=$(pwd)
```

### Encoding UTF-8

El pipeline principal configura UTF-8 para mostrar correctamente caracteres especiales:

```batch
chcp 65001 >nul  # Windows
```

```python
# En run_etl_with_tests.py
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
```

### Manejo de Errores

Todos los scripts verifican códigos de salida:

```batch
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: El proceso fallo
    exit /b 1
)
```

---

## ❓ Troubleshooting

### Problema: "ModuleNotFoundError"

**Solución:** Asegúrate de ejecutar desde la raíz del proyecto:
```bash
cd /ruta/al/etl_randomuser
PIPELINE.bat
```

### Problema: Dashboard no se abre

**Solución:** Abre manualmente:
```
http://localhost:8000/dashboard/dashboard.html
```

### Problema: "Puerto 8000 ya en uso"

**Solución:** Cambiar puerto en `serve_dashboard.py`:
```python
PORT = 8001  # Cambiar puerto
```

### Problema: "No se encuentran los gráficos"

**Solución:** Asegúrate de ejecutar el ETL primero:
```bash
scripts_project\run_etl.bat
```

---

## 📚 Scripts Relacionados

- **[README.md](README.md)** - Documentación general del proyecto
- **[EXPLICACION_ETL.md](EXPLICACION_ETL.md)** - Detalles del proceso ETL
- **[MEMORIA_ETL_UNIVERSITARIA.md](MEMORIA_ETL_UNIVERSITARIA.md)** - Documentación académica

---

**⭐ Recomendación:** Usa `PIPELINE.bat` o `PIPELINE.sh` para la experiencia completa.

