# Proyecto ETL RandomUser

Este proyecto implementa un proceso ETL (Extract, Transform, Load) en Python.  
Usa la API pública [RandomUser](https://randomuser.me/api/) para obtener datos de usuarios,
procesarlos y guardarlos en formatos CSV y SQLite.

## Estructura
etl_project/
├── src/
│ ├── main.py
│ ├── etl_service.py
│ ├── user_model.py
│ └── loader/
│ ├── base_loader.py
│ ├── csv_loader.py
│ └── sql_loader.py
├── data/
├── requirements.txt
└── README.md

bash
Copiar código

## Instalación y uso
```bash
pip install -r requirements.txt
python src/main.py
Salida
data/users.csv → Datos de usuarios en CSV

data/users.db → Base de datos SQLite

yaml
Copiar código

---

## ✅ Resultat quan l’executes

```bash
🔹 Extrayendo usuarios...
🔹 Transformando datos...
🔹 Guardando resultados...
✅ Datos guardados en data/users.csv
✅ Datos insertados correctamente en la base de datos.
✅ Proceso ETL completado con éxito.
I a la carpeta data/ tindràs:

users.csv

users.db

