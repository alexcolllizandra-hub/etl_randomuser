import sqlite3
import os
from typing import List, Dict, Any
from src.loaders.base_loader import BaseLoader
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class SQLLoader(BaseLoader):
    """Carga los datos en una base de datos SQLite."""

    def __init__(self, db_name: str = "users.db") -> None:
        self.db_name = db_name

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
