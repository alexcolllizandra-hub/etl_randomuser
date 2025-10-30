# 🧑‍💻 Proyecto ETL RandomUser

## 🚦 ¿Qué es este proyecto?

Este repositorio despliega paso a paso un **proceso ETL** (Extracción, Transformación y Carga) utilizando Python y la API pública [RandomUser](https://randomuser.me/api/). Es 100% didáctico, ideal para practicar cómo crear pipelines ETL modernos, generando análisis y visualizaciones a partir de datos reales de usuarios internacionales.

---

## 💡 ¿Qué hace exactamente este ETL?

- **Extract (Extracción):** Descarga cientos o miles de perfiles aleatorios (ficticios) usando la API RandomUser.
- **Transform (Transformación):** Limpia, filtra y enriquece los datos (por ejemplo: calcula grupos de edad, detecta outliers, obtiene información del país desde otra API, etc.).
- **Load (Carga):** Almacena el resultado en CSV y en una base de datos SQLite para consumir con cualquier herramienta.
- **Visualización:** Genera gráficos automáticos (edades, géneros, países top, etc.) como complemento analítico.

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
```bash
python src/main.py
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
├── data/         # Aquí se almacenan los resultados: CSV y DB
├── logs/         # (opcional) Aquí se ubican los logs detallados si los configuras
├── requirements.txt # Dependencias Python necesarias
└── README.md
```

---

## 📈 ¿Qué obtendrás? (outputs)

Tras ejecutar el proyecto, encontrarás:

- `data/usuarios.csv` → Archivo CSV con toda la información procesada.
- `data/usuarios.db`  → Base de datos SQLite para análisis con otros programas.
- **Gráficos** (se abren automáticamente al final): distribución de edad, géneros, top países, etc.

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

---
