from models.person import Person

class User(Person):
    """User class representing a developer/administrator, inheriting from Person."""
    def __init__(self, name: str, email: str):
        super().__init__(name, email)

    def to_dict(self) -> dict:
        """Converts user object to dictionary for JSON persistence."""
        return {
            "name": self.name,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Creates a User instance from a dictionary."""
        return cls(name=data["name"], email=data["email"])

    def __str__(self) -> str:
        return f"User: {self.name} <{self.email}>"

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, email={self.email!r})"
