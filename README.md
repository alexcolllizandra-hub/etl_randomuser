# 🚀 Proyecto ETL RandomUser

Proceso ETL (Extract, Transform, Load) en Python usando la API pública [RandomUser](https://randomuser.me/api/):

- **Extract:** Obtiene usuarios aleatorios de la API.
- **Transform:** Normaliza y limpia los datos.
- **Load:** Guarda en CSV y SQLite.

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

## ⚡ Uso Rápido

Instala dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta el ETL:

```bash
python src/main.py
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

## ✨ Notas

- El directorio `data/` contiene los resultados del proceso.
- La API RandomUser no requiere registro.
- 100% Python puro, modular y fácil de ampliar.

---

