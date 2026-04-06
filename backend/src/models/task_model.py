from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Modelo que representa una tarea del sistema."""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    is_completed: bool = False
    created_at: Optional[str] = None

    def to_dict(self):
        """Convierte la tarea a un diccionario serializable."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
            "created_at": self.created_at
        }

    @staticmethod
    def from_row(row):
        """Crea una instancia de Task desde una fila de la base de datos."""
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            is_completed=bool(row["is_completed"]),
            created_at=row["created_at"]
        )
