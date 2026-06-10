import pytest
from models import Person, User, Project, Task

def test_person_model():
    p = Person("John Doe", "john@example.com")
    assert p.name == "John Doe"
    assert p.email == "john@example.com"
    
    # Test setters
    p.name = "Jane Doe"
    assert p.name == "Jane Doe"
    
    p.email = "jane@example.com"
    assert p.email == "jane@example.com"

    with pytest.raises(ValueError, match="Name cannot be empty"):
        p.name = ""

    with pytest.raises(ValueError, match="Invalid email format"):
        p.email = "invalid-email"

def test_user_model():
    u = User("Alice Smith", "alice@example.com")
    assert isinstance(u, Person)
    assert u.name == "Alice Smith"
    assert u.email == "alice@example.com"
    
    u_dict = u.to_dict()
    assert u_dict == {"name": "Alice Smith", "email": "alice@example.com"}
    
    u2 = User.from_dict(u_dict)
    assert u2.name == "Alice Smith"
    assert u2.email == "alice@example.com"

def test_project_model():
    Project.reset_counter(0)
    p = Project("Web App", "Develop React dashboard", "2026-12-31", "alice@example.com")
    assert p.id == 1
    assert p.title == "Web App"
    assert p.description == "Develop React dashboard"
    assert p.due_date == "2026-12-31"
    assert p.status == "Active"

    # Test setter validation
    with pytest.raises(ValueError, match="Project title cannot be empty"):
        p.title = " "

    with pytest.raises(ValueError, match="Due date must be in YYYY-MM-DD format"):
        p.due_date = "12/31/2026"

    with pytest.raises(ValueError, match="Status must be one of"):
        p.status = "Completed soon"

    p.status = "Completed"
    assert p.status == "Completed"

def test_task_model():
    Task.reset_counter(0)
    t = Task("Write core logic", 1, "alice@example.com")
    assert t.id == 1
    assert t.title == "Write core logic"
    assert t.project_id == 1
    assert t.assigned_to == "alice@example.com"
    assert t.status == "Pending"
    assert t.contributors == []

    # Test contributors
    t.add_contributor("bob@example.com")
    assert t.contributors == ["bob@example.com"]
    
    # Adding duplicate
    t.add_contributor("bob@example.com")
    assert len(t.contributors) == 1

    t.remove_contributor("bob@example.com")
    assert t.contributors == []
