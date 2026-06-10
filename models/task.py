class Task:
    """Task class representing a specific action item within a project."""
    _id_counter = 0

    def __init__(self, title: str, project_id: int, assigned_to: str, task_id: int = None, status: str = "Pending", contributors: list = None):
        if task_id is None:
            Task._id_counter += 1
            self.id = Task._id_counter
        else:
            self.id = task_id
            if task_id > Task._id_counter:
                Task._id_counter = task_id

        self.title = title
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.status = status
        self.contributors = contributors if contributors is not None else []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty")
        self._title = value.strip()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        valid_statuses = ["Pending", "In Progress", "Completed"]
        val = value.strip().title() if value else ""
        if val not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        self._status = val

    @property
    def assigned_to(self) -> str:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str):
        if not value or "@" not in value or "." not in value:
            raise ValueError("Assigned user must be a valid email format")
        self._assigned_to = value.strip()

    @classmethod
    def reset_counter(cls, start: int = 0):
        """Resets the ID counter to a start value."""
        cls._id_counter = start

    def add_contributor(self, email: str):
        """Adds a user's email as a contributor to this task (many-to-many relationship)."""
        email = email.strip()
        if "@" not in email or "." not in email:
            raise ValueError("Contributor email must be in a valid format")
        if email not in self.contributors:
            self.contributors.append(email)

    def remove_contributor(self, email: str):
        """Removes a contributor email from the task."""
        email = email.strip()
        if email in self.contributors:
            self.contributors.remove(email)

    def to_dict(self) -> dict:
        """Converts task object to dictionary for JSON persistence."""
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "contributors": self.contributors
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Creates a Task instance from a dictionary."""
        return cls(
            title=data["title"],
            project_id=data["project_id"],
            assigned_to=data["assigned_to"],
            task_id=data.get("id"),
            status=data.get("status", "Pending"),
            contributors=data.get("contributors", [])
        )

    def __str__(self) -> str:
        contribs_str = f", Contributors: {', '.join(self.contributors)}" if self.contributors else ""
        return f"Task #{self.id}: {self.title} [Status: {self.status}, Assigned to: {self.assigned_to}{contribs_str}]"

    def __repr__(self) -> str:
        return (f"Task(id={self.id}, title={self.title!r}, project_id={self.project_id}, "
                f"assigned_to={self.assigned_to!r}, status={self.status!r}, contributors={self.contributors!r})")
