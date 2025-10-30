from dataclasses import dataclass

@dataclass
class User:
    """Modelo que representa un usuario obtenido de la API RandomUser."""
    gender: str
    first_name: str
    last_name: str
    country: str
    age: int
    email: str

    @staticmethod
    def from_api(data: dict) -> "User":
        """Convierte el JSON de la API en una instancia de User."""
        return User(
            gender=data.get("gender", ""),
            first_name=data.get("name", {}).get("first", ""),
            last_name=data.get("name", {}).get("last", ""),
            country=data.get("location", {}).get("country", ""),
            age=data.get("dob", {}).get("age", 0),
            email=data.get("email", "")
        )
