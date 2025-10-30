from abc import ABC, abstractmethod
from typing import Any

class BaseLoader(ABC):
    """Interfaz base para todas las clases de carga de datos."""

    @abstractmethod
    def load(self, data: Any, output_dir: str) -> None:
        """
        Carga los datos a un destino (archivo, base de datos, etc.)
        :param data: Datos a cargar.
        :param output_dir: Carpeta donde se guardarán los resultados.
        """
        pass
