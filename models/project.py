from datetime import datetime

class Project:
    """Project class representing a project managed by a user."""
    _id_counter = 0

    def __init__(self, title: str, description: str, due_date: str, user_email: str, project_id: int = None, status: str = "Active"):
        if project_id is None:
            Project._id_counter += 1
            self.id = Project._id_counter
        else:
            self.id = project_id
            if project_id > Project._id_counter:
                Project._id_counter = project_id

        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.user_email = user_email

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty")
        self._title = value.strip()

    @property
    def due_date(self) -> str:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        # Validate YYYY-MM-DD format
        try:
            datetime.strptime(value.strip(), "%Y-%m-%d")
            self._due_date = value.strip()
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        valid_statuses = ["Active", "Completed", "On Hold"]
        val = value.strip().title() if value else ""
        if val not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        self._status = val

    @classmethod
    def reset_counter(cls, start: int = 0):
        """Resets the ID counter to a start value."""
        cls._id_counter = start

    def to_dict(self) -> dict:
        """Converts project object to dictionary for JSON persistence."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "user_email": self.user_email
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Creates a Project instance from a dictionary."""
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            user_email=data["user_email"],
            project_id=data.get("id"),
            status=data.get("status", "Active")
        )

    def __str__(self) -> str:
        return f"Project #{self.id}: {self.title} [Status: {self.status}, Due: {self.due_date}]"

    def __repr__(self) -> str:
        return (f"Project(id={self.id}, title={self.title!r}, "
                f"description={self.description!r}, due_date={self.due_date!r}, "
                f"status={self.status!r}, user_email={self.user_email!r})")
