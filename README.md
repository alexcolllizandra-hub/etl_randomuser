# 🚀 Proyecto ETL RandomUser

Proceso ETL (Extract, Transform, Load) en Python usando la API pública [RandomUser](https://randomuser.me/api/):

- **Extract:** Obtiene usuarios aleatorios de la API.
- **Transform:** Normaliza y limpia los datos.
- **Load:** Guarda en CSV y SQLite.

---

## 📥 Guía

Repositorio: [alexcolllizandra-hub/etl_randomuser](https://github.com/alexcolllizandra-hub/etl_randomuser.git)

### 1. Clona el repositorio

```bash
git clone https://github.com/alexcolllizandra-hub/etl_randomuser.git
cd etl_randomuser
```

### 2. Ábrelo en PyCharm

- Ve a PyCharm → `Open` → selecciona la carpeta `etl_randomuser`.
- Acepta crear el entorno virtual si te lo pregunta (recomendado).

### 3. Instala las dependencias

- Abre una terminal (en PyCharm o en la carpeta del proyecto):

```bash
pip install -r requirements.txt
```

### 4. Ejecuta el ETL

```bash
python src/main.py
```

---

## 📦 Estructura del proyecto

```
etl_project/
├── src/
│   ├── main.py
│   ├── etl_service.py
│   ├── user_model.py
│   └── loader/
│       ├── base_loader.py
│       ├── csv_loader.py
│       └── sql_loader.py
├── data/
├── requirements.txt
└── README.md
```

---

## 📂 Salida esperada

- `data/users.csv` → Datos en CSV
- `data/users.db`  → SQLite DB

Con mensajes tipo:
```
🔹 Extrayendo usuarios...
🔹 Transformando datos...
🔹 Guardando resultados...
✅ Datos guardados en data/users.csv
✅ Datos insertados correctamente en la base de datos.
✅ Proceso ETL completado con éxito.
```

---

## ✨ Notas y recomendaciones

- El directorio `data/` contiene los resultados del proceso.
- La API RandomUser no requiere registro.
- Puedes usar cualquier editor: VSCode, PyCharm, etc.
- Puedes modificar las rutas de salida si lo necesitas.
- 100% Python puro, modular y fácil de ampliar.

---

Hecho con ❤️ y Python.
