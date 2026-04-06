from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Subtask:
    """Modelo que representa una subtarea dentro de una lista de tareas."""
    id: Optional[int] = None
    task_list_id: Optional[int] = None
    title: str = ""
    is_completed: bool = False
    created_at: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "task_list_id": self.task_list_id,
            "title": self.title,
            "is_completed": self.is_completed,
            "created_at": self.created_at
        }

    @staticmethod
    def from_row(row):
        return Subtask(
            id=row["id"],
            task_list_id=row["task_list_id"],
            title=row["title"],
            is_completed=bool(row["is_completed"]),
            created_at=row["created_at"]
        )


@dataclass
class TaskList:
    """Modelo que representa una lista de tareas con subtareas."""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    created_at: Optional[str] = None
    subtasks: list = field(default_factory=list)

    @property
    def progress(self):
        """Calcula el porcentaje de subtareas completadas."""
        if not self.subtasks:
            return 0
        completed = sum(1 for s in self.subtasks if s.is_completed)
        return round((completed / len(self.subtasks)) * 100)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "subtasks": [s.to_dict() for s in self.subtasks],
            "progress": self.progress
        }

    @staticmethod
    def from_row(row):
        return TaskList(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            created_at=row["created_at"]
        )
