class Person:
    """Base class representing a person with a name and email."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not value or "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        self._email = value.strip()

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, email={self.email!r})"
