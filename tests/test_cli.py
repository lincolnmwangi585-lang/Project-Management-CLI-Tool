import pytest
from typer.testing import CliRunner
import utils.persistence as persistence
from main import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_persistence_paths(tmp_path, monkeypatch):
    """Fixture to automatically redirect data storage to a temp directory for tests."""
    temp_data_dir = tmp_path / "data"
    temp_data_dir.mkdir()
    
    monkeypatch.setattr(persistence, "DATA_DIR", str(temp_data_dir))
    monkeypatch.setattr(persistence, "USERS_FILE", str(temp_data_dir / "users.json"))
    monkeypatch.setattr(persistence, "PROJECTS_FILE", str(temp_data_dir / "projects.json"))
    monkeypatch.setattr(persistence, "TASKS_FILE", str(temp_data_dir / "tasks.json"))

def test_add_user_success():
    result = runner.invoke(app, ["add-user", "--name", "Alex Jones", "--email", "alex@example.com"])
    assert result.exit_code == 0
    assert "Success: Added user 'Alex Jones' <alex@example.com> successfully." in result.output

    # Duplicate user check
    result_dup = runner.invoke(app, ["add-user", "--name", "Alex Dup", "--email", "alex@example.com"])
    assert result_dup.exit_code == 1
    assert "Error: A user with email 'alex@example.com' already exists!" in result_dup.output

def test_list_users():
    runner.invoke(app, ["add-user", "--name", "Alex Jones", "--email", "alex@example.com"])
    result = runner.invoke(app, ["list-users"])
    assert result.exit_code == 0
    assert "Alex Jones" in result.output
    assert "alex@example.com" in result.output

def test_add_project_and_list():
    # Attempt to add project for non-existing user
    result_fail = runner.invoke(app, [
        "add-project", "--user", "nobody@example.com", "--title", "CLI Tool", "--desc", "Test", "--due", "2026-12-31"
    ])
    assert result_fail.exit_code == 1
    assert "Error: User 'nobody@example.com' doesn't exist in our system." in result_fail.output

    # Register user first
    runner.invoke(app, ["add-user", "--name", "Alex", "--email", "alex@example.com"])
    
    # Success project creation
    result = runner.invoke(app, [
        "add-project", "--user", "alex@example.com", "--title", "CLI Tool", "--desc", "My project desc", "--due", "2026-12-31"
    ])
    assert result.exit_code == 0
    assert "Project Created!" in result.output

    # List projects
    result_list = runner.invoke(app, ["list-projects"])
    assert result_list.exit_code == 0
    assert "CLI Tool" in result_list.output
    assert "My project desc" in result_list.output

def test_add_task_and_complete():
    # Register user & project
    runner.invoke(app, ["add-user", "--name", "Alex", "--email", "alex@example.com"])
    runner.invoke(app, ["add-project", "--user", "alex@example.com", "--title", "CLI Tool", "--desc", "My project desc", "--due", "2026-12-31"])

    # Add task
    result_task = runner.invoke(app, [
        "add-task", "--project-id", "1", "--title", "Write code", "--assigned", "alex@example.com"
    ])
    assert result_task.exit_code == 0
    assert "Success: Task 'Write code' (ID: 1) added to Project #1." in result_task.output

    # Add contributor (many-to-many)
    # Register second user first
    runner.invoke(app, ["add-user", "--name", "Bob", "--email", "bob@example.com"])
    result_contrib = runner.invoke(app, [
        "add-contributor", "--task-id", "1", "--email", "bob@example.com"
    ])
    assert result_contrib.exit_code == 0
    assert "Success: Added 'bob@example.com' as a contributor to Task #1." in result_contrib.output

    # Complete task
    result_complete = runner.invoke(app, ["complete-task", "--task-id", "1"])
    assert result_complete.exit_code == 0
    assert "Success: Task #1 marked as Completed." in result_complete.output
