# 🧑‍💻 Proyecto ETL RandomUser

Proceso ETL (Extracción, Transformación y Carga) completo desarrollado en Python sin usar pandas/numpy.

---

## ⚡ Ejecución Ultra-Rápida

**UN SOLO COMANDO PARA TODO:**

```bash
# Windows
PIPELINE.bat

# Linux/Mac/Debian (VM)
chmod +x PIPELINE.sh
./PIPELINE.sh
```

**¿Qué hace este comando?**
1. ✅ **Ejecuta el ETL** → Extrae, transforma y carga datos
2. ✅ **Verifica SQLite** → Comprueba que todo esté correcto
3. ✅ **Abre Dashboard** → Visualiza los 8 gráficos en tu navegador

**Eso es todo. Un solo comando y tienes todo funcionando.**

---

## 📁 Estructura del Proyecto

```
etl_randomuser/
│
├── src/                      # Código fuente principal
│   ├── main.py              # Punto de entrada
│   ├── controller/          # Controlador ETL
│   ├── services/            # Lógica de negocio
│   ├── loaders/             # Carga de datos
│   ├── models/              # Modelos de datos
│   └── utils/               # Utilidades
│
├── scripts_project/         # Scripts de ejecución
│   ├── run_etl_with_tests.py
│   ├── serve_dashboard.py
│   ├── run_etl.bat/sh
│   └── VIEW_DASHBOARD.bat/sh
│
├── dashboard/               # Dashboard HTML interactivo
│   └── dashboard.html
│
├── docs/                    # Documentación
│   ├── README.md
│   ├── GUIA_SCRIPTS.md
│   ├── MEJORAS_IMPLEMENTADAS.md
│   ├── EXPLICACION_ETL.md
│   ├── MEMORIA_ETL_UNIVERSITARIA.md
│   └── GUIA_VIRTUALIZACION.md
│
├── data/                    # Datos generados
│   ├── usuarios.csv
│   ├── usuarios.db
│   └── stats.json
│
├── plots/                   # Gráficos generados
│
├── PIPELINE.bat/.sh         # Pipeline completo ⭐
└── requirements.txt         # Dependencias
```

---

## 📚 Documentación

- **[README Completo](docs/README.md)** - Documentación detallada del proyecto
- **[Guía de Scripts](docs/GUIA_SCRIPTS.md)** ⭐ - Todos los scripts y pipelines explicados
- **[Mejoras Implementadas](docs/MEJORAS_IMPLEMENTADAS.md)** ⭐ - Transformaciones y visualizaciones avanzadas
- **[Explicación ETL](docs/EXPLICACION_ETL.md)** - Detalles técnicos del proceso ETL
- **[Memoria Universitaria](docs/MEMORIA_ETL_UNIVERSITARIA.md)** - Documento académico completo
- **[Guía Virtualización](docs/GUIA_VIRTUALIZACION.md)** - Setup con VM

---

## 🎯 Características

- ✅ **ETL completo**: Extract, Transform, Load
- ✅ **Sin pandas/numpy**: Cálculos manuales
- ✅ **Doble almacenamiento**: CSV + SQLite
- ✅ **8 visualizaciones** automáticas (3 nuevas añadidas)
- ✅ **Estadísticas avanzadas**: CV, IQR, min/max, cuartiles
- ✅ **Transformaciones ampliadas**: categorías, preferencias, outliers
- ✅ **Dashboard interactivo** HTML
- ✅ **Verificaciones automáticas**
- ✅ **100% reproducible** con seeds

---

## 🛠️ Instalación

```bash
# Clonar repositorio
git clone https://github.com/alexcolllizandra-hub/etl_randomuser.git
cd etl_randomuser

# Instalar dependencias
   pip install -r requirements.txt
   ```

---

## 🔧 Scripts Adicionales

Si necesitas ejecutar partes del proceso por separado:

**Solo ETL:**
```bash
python -m src.main
```

**Solo Dashboard (si ya ejecutaste ETL antes):**
```bash
# Windows
scripts_project\VIEW_DASHBOARD.bat

# Linux/Mac
chmod +x scripts_project/VIEW_DASHBOARD.sh && ./scripts_project/VIEW_DASHBOARD.sh
```

**Solo verificaciones:**
```bash
python scripts_project\run_etl_with_tests.py --skip-etl
```

---

## 📈 Resultados

Tras ejecutar el pipeline:
- `data/usuarios.csv` - Datos en formato CSV
- `data/usuarios.db` - Base de datos SQLite
- `plots/*.png` - 8 gráficos estadísticos
- Dashboard interactivo en http://localhost:8000

**8 Gráficos generados:**
1. Distribución de Edades (histograma)
2. Distribución por Género (barras)
3. Top 10 Países (barras horizontales)
4. Edad por País (boxplots)
5. Matriz de Correlación (heatmap)
6. 📊 Distribución por Regiones (barras - NUEVO)
7. 📊 Grupos de Edad (pie chart - NUEVO)
8. 📊 Género por País (barras apiladas - NUEVO)

---

## 🔗 Enlaces

- API RandomUser: https://randomuser.me/
- RestCountries API: https://restcountries.com/

---

## 📝 Licencia

Proyecto académico - Uso libre para fines educativos

---

## 🎯 Para Usuarios de VM (Debian 12)

**1. Clonar repositorio:**
```bash
git clone https://github.com/alexcolllizandra-hub/etl_randomuser.git
cd etl_randomuser
```

**2. Instalar dependencias:**
```bash
pip3 install -r requirements.txt
```

**3. Ejecutar (TODO EN UNO):**
```bash
chmod +x PIPELINE.sh
./PIPELINE.sh
```

El dashboard se abrirá automáticamente en tu navegador. Si no se abre, visita: `http://localhost:8000/dashboard/dashboard.html`

---

**⭐ RECOMENDACIÓN: Usa `PIPELINE.bat` o `PIPELINE.sh` - Es el camino más simple**

