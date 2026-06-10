# Summative Lab: Python Project Management CLI Tool

**Course**: CSCI-301 / Software Engineering Methods  
**Lab Assignment**: Project Management Command-Line Tool  
**Status**: Completed and Submitted for Evaluation  

---

## 📝 Project Overview

This is my implementation for the Project Management CLI Tool Summative Lab. It is written in Python 3.12 and implements Object-Oriented Programming (OOP) principles, relational data mappings (one-to-many and many-to-many relationships), local storage persistence via JSON file I/O, and an interactive CLI with input validation.

### Core Architecture & OOP Features
- **Inheritance**: Defined a base class `Person` (holding `name` and `email` properties) from which `User` inherits.
- **Encapsulation**: Used property getters and setters (`@property` and `@setter`) in `Person`, `Project`, and `Task` to run clean data validation (e.g., preventing empty titles, verifying email shapes, and enforcing specific `YYYY-MM-DD` date formats).
- **Class Attributes**: Employed incremental counters on the `Project` and `Task` classes to automatically assign IDs and automatically restore counters correctly when reloading state from the database files.
- **Relational Integrity**:
  - **One-to-Many**: Users can own multiple Projects.
  - **One-to-Many**: Projects can contain multiple Tasks.
  - **Many-to-Many**: Tasks can have multiple User Emails registered as "contributors" (co-workers).

---

## 📂 Project Structure

```text
Project-Management-CLI-Tool/
├── data/                    # Storage directory for local JSON database files
│   ├── users.json
│   ├── projects.json
│   └── tasks.json
├── models/                  # Classes and object data definitions
│   ├── __init__.py
│   ├── person.py            # Parent class Person (Encapsulation and setters)
│   ├── user.py              # Child class User (Inheritance)
│   ├── project.py           # Project details and validation
│   └── task.py              # Task details, status, and contributors
├── utils/                   # File system utilities
│   ├── __init__.py
│   └── persistence.py       # JSON Load/Save handler with try/except
├── tests/                   # Automated unit testing suite
│   ├── test_cli.py
│   └── test_models.py
├── requirements.txt         # Student dependencies (typer, rich, pytest)
├── main.py                  # Main program entry point
└── README.md                # Project documentation
```

---

## 🚀 How to Set Up and Run

### 1. Requirements Setup
Install the external packages (`typer` for subcommands, `rich` for nice console tables, and `pytest` for running test suites) specified in the lab assignment:
```bash
pip install -r requirements.txt
```

### 2. User Subcommands
- **Create a User**:
  ```bash
  python3 main.py add-user --name "Alice Smith" --email "alice@example.com"
  python3 main.py add-user --name "Bob Johnson" --email "bob@example.com"
  ```
- **List Registered Users**:
  ```bash
  python3 main.py list-users
  ```

### 3. Project Subcommands
- **Add a Project** (Validates owner email and YYYY-MM-DD format):
  ```bash
  python3 main.py add-project --user "alice@example.com" --title "Math App" --desc "Calculus homework app" --due "2026-10-31"
  ```
- **List Projects** (Optionally filter by user email):
  ```bash
  python3 main.py list-projects
  python3 main.py list-projects --user "alice@example.com"
  ```
- **Update Status**:
  ```bash
  python3 main.py update-project-status --project-id 1 --status "Completed"
  ```

### 4. Task Subcommands
- **Add a Task to a Project**:
  ```bash
  python3 main.py add-task --project-id 1 --title "Write parser" --assigned "alice@example.com"
  ```
- **Add Collaborators** (Demonstrates many-to-many relationship):
  ```bash
  python3 main.py add-contributor --task-id 1 --email "bob@example.com"
  ```
- **List Tasks**:
  ```bash
  python3 main.py list-tasks --project-id 1
  ```
- **Complete a Task**:
  ```bash
  python3 main.py complete-task --task-id 1
  ```

---

## 🧪 Running Unit Tests

I wrote automated unit tests using `pytest` to test models, setter validation errors, and command runners. Run them with:
```bash
python3 -m pytest -v
```
All tests use temporary folder fixtures to make sure the program doesn't touch or corrupt actual user storage files in `data/`.
