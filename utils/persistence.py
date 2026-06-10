import os
import json
from models import User, Project, Task

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

def _ensure_data_dir():
    """Ensures that the data storage directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_users() -> list[User]:
    """Loads users from the JSON storage file."""
    _ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return [User.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError, PermissionError) as e:
        # Robust handling of malformed or unreadable data
        return []

def save_users(users: list[User]):
    """Saves users to the JSON storage file."""
    _ensure_data_dir()
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([user.to_dict() for user in users], f, indent=4)
    except PermissionError as e:
        raise IOError(f"Permission denied writing to users file: {e}")

def load_projects() -> list[Project]:
    """Loads projects from the JSON storage file and adjusts ID counter."""
    _ensure_data_dir()
    Project.reset_counter(0)
    if not os.path.exists(PROJECTS_FILE):
        return []
    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            projects = []
            for item in data:
                proj = Project.from_dict(item)
                projects.append(proj)
            return projects
    except (json.JSONDecodeError, KeyError, PermissionError):
        return []

def save_projects(projects: list[Project]):
    """Saves projects to the JSON storage file."""
    _ensure_data_dir()
    try:
        with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
            json.dump([proj.to_dict() for proj in projects], f, indent=4)
    except PermissionError as e:
        raise IOError(f"Permission denied writing to projects file: {e}")

def load_tasks() -> list[Task]:
    """Loads tasks from the JSON storage file and adjusts ID counter."""
    _ensure_data_dir()
    Task.reset_counter(0)
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            tasks = []
            for item in data:
                task = Task.from_dict(item)
                tasks.append(task)
            return tasks
    except (json.JSONDecodeError, KeyError, PermissionError):
        return []

def save_tasks(tasks: list[Task]):
    """Saves tasks to the JSON storage file."""
    _ensure_data_dir()
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=4)
    except PermissionError as e:
        raise IOError(f"Permission denied writing to tasks file: {e}")
