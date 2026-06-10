import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from models import User, Project, Task
from utils import (
    load_users,
    save_users,
    load_projects,
    save_projects,
    load_tasks,
    save_tasks,
)

# Created a simple Typer app for our school project CLI
app = typer.Typer(help="🎓 Student Project Management CLI Tool")
console = Console()

@app.command("add-user")
def add_user(
    name: str = typer.Option(..., "--name", "-n", help="Name of the new user"),
    email: str = typer.Option(..., "--email", "-e", help="Email of the new user"),
):
    """
    Add a new user to the local system database.
    """
    try:
        users = load_users()
        # Check if the user email is already in our list
        if any(u.email.lower() == email.strip().lower() for u in users):
            console.print(f"[bold red]Error:[/] A user with email '{email}' already exists!")
            raise typer.Exit(code=1)

        user = User(name=name, email=email)
        users.append(user)
        save_users(users)
        console.print(f"[bold green]Success:[/] Added user '{user.name}' <{user.email}> successfully.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/] {e}")
        raise typer.Exit(code=1)

@app.command("list-users")
def list_users():
    """
    Show all registered users in a clean table format.
    """
    users = load_users()
    if not users:
        console.print("[yellow]No users registered yet. Run 'add-user' to add one.[/]")
        return

    table = Table(title="Registered Users List", show_header=True, header_style="bold blue")
    table.add_column("Full Name", style="cyan")
    table.add_column("Email Address", style="green")

    for u in users:
        table.add_row(u.name, u.email)

    console.print(table)

@app.command("add-project")
def add_project(
    user_email: str = typer.Option(..., "--user", "-u", help="Email of the user owning this project"),
    title: str = typer.Option(..., "--title", "-t", help="Title of the project"),
    description: str = typer.Option(..., "--desc", "-d", help="Short description of the project"),
    due_date: str = typer.Option(..., "--due", help="Due date (format: YYYY-MM-DD)"),
):
    """
    Create a project and link it to an existing user's email.
    """
    users = load_users()
    if not any(u.email.lower() == user_email.strip().lower() for u in users):
        console.print(f"[bold red]Error:[/] User '{user_email}' doesn't exist in our system.")
        raise typer.Exit(code=1)

    try:
        projects = load_projects()
        project = Project(
            title=title,
            description=description,
            due_date=due_date,
            user_email=user_email.strip().lower()
        )
        projects.append(project)
        save_projects(projects)
        console.print(Panel(
            f"[bold green]Project Created![/]\n"
            f"ID: {project.id}\n"
            f"Title: {project.title}\n"
            f"Assigned To: {project.user_email}\n"
            f"Due Date: {project.due_date}",
            title="Project Information",
            expand=False
        ))
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/] {e}")
        raise typer.Exit(code=1)

@app.command("list-projects")
def list_projects(
    user_email: Optional[str] = typer.Option(None, "--user", "-u", help="Filter by user email")
):
    """
    List all projects or filter them for a specific user email.
    """
    projects = load_projects()
    if user_email:
        projects = [p for p in projects if p.user_email.lower() == user_email.strip().lower()]

    if not projects:
        console.print("[yellow]No projects found.[/]")
        return

    table = Table(title="Projects Database", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="bold green")
    table.add_column("Description")
    table.add_column("Owner Email", style="magenta")
    table.add_column("Due Date")
    table.add_column("Status")

    for p in projects:
        table.add_row(str(p.id), p.title, p.description, p.user_email, p.due_date, p.status)

    console.print(table)

@app.command("update-project-status")
def update_project_status(
    project_id: int = typer.Option(..., "--project-id", "-p", help="ID of the project"),
    status: str = typer.Option(..., "--status", "-s", help="New status: Active, Completed, On Hold"),
):
    """
    Update the status of an existing project.
    """
    projects = load_projects()
    target_project = None
    for p in projects:
        if p.id == project_id:
            target_project = p
            break

    if not target_project:
        console.print(f"[bold red]Error:[/] Project with ID {project_id} not found.")
        raise typer.Exit(code=1)

    try:
        target_project.status = status
        save_projects(projects)
        console.print(f"[bold green]Success:[/] Updated status of Project #{project_id} to '{target_project.status}'.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/] {e}")
        raise typer.Exit(code=1)

@app.command("add-task")
def add_task(
    project_id: int = typer.Option(..., "--project-id", "-p", help="ID of the project"),
    title: str = typer.Option(..., "--title", "-t", help="Title of the task"),
    assigned_to: str = typer.Option(..., "--assigned", "-a", help="Email of the assigned user"),
):
    """
    Add a task to a project and assign it to a user.
    """
    projects = load_projects()
    if not any(p.id == project_id for p in projects):
        console.print(f"[bold red]Error:[/] Project ID {project_id} not found.")
        raise typer.Exit(code=1)

    users = load_users()
    if not any(u.email.lower() == assigned_to.strip().lower() for u in users):
        console.print(f"[bold red]Error:[/] User with email '{assigned_to}' does not exist.")
        raise typer.Exit(code=1)

    try:
        tasks = load_tasks()
        task = Task(
            title=title,
            project_id=project_id,
            assigned_to=assigned_to.strip().lower()
        )
        tasks.append(task)
        save_tasks(tasks)
        console.print(f"[bold green]Success:[/] Task '{task.title}' (ID: {task.id}) added to Project #{project_id}.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/] {e}")
        raise typer.Exit(code=1)

@app.command("add-contributor")
def add_contributor(
    task_id: int = typer.Option(..., "--task-id", "-t", help="ID of the task"),
    email: str = typer.Option(..., "--email", "-e", help="Email of the contributor"),
):
    """
    Add a contributor email to a task (demonstrates many-to-many relationship).
    """
    tasks = load_tasks()
    target_task = None
    for t in tasks:
        if t.id == task_id:
            target_task = t
            break

    if not target_task:
        console.print(f"[bold red]Error:[/] Task with ID {task_id} not found.")
        raise typer.Exit(code=1)

    users = load_users()
    if not any(u.email.lower() == email.strip().lower() for u in users):
        console.print(f"[bold red]Error:[/] User '{email}' not found in registered database.")
        raise typer.Exit(code=1)

    try:
        target_task.add_contributor(email)
        save_tasks(tasks)
        console.print(f"[bold green]Success:[/] Added '{email}' as a contributor to Task #{task_id}.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/] {e}")
        raise typer.Exit(code=1)

@app.command("complete-task")
def complete_task(
    task_id: int = typer.Option(..., "--task-id", "-t", help="ID of the task to complete")
):
    """
    Mark a task as completed.
    """
    tasks = load_tasks()
    target_task = None
    for t in tasks:
        if t.id == task_id:
            target_task = t
            break

    if not target_task:
        console.print(f"[bold red]Error:[/] Task with ID {task_id} not found.")
        raise typer.Exit(code=1)

    target_task.status = "Completed"
    save_tasks(tasks)
    console.print(f"[bold green]Success:[/] Task #{task_id} marked as Completed.")

@app.command("list-tasks")
def list_tasks(
    project_id: Optional[int] = typer.Option(None, "--project-id", "-p", help="Filter tasks by project ID")
):
    """
    List all tasks or filter them by a specific project ID.
    """
    tasks = load_tasks()
    if project_id is not None:
        tasks = [t for t in tasks if t.project_id == project_id]

    if not tasks:
        console.print("[yellow]No tasks match your selection.[/]")
        return

    table = Table(title="Task Board Database", show_header=True, header_style="bold green")
    table.add_column("Task ID", style="dim")
    table.add_column("Proj ID", style="dim")
    table.add_column("Task Title", style="bold cyan")
    table.add_column("Assignee", style="magenta")
    table.add_column("Contributors")
    table.add_column("Status")

    for t in tasks:
        contribs = ", ".join(t.contributors) if t.contributors else "None"
        table.add_row(str(t.id), str(t.project_id), t.title, t.assigned_to, contribs, t.status)

    console.print(table)

if __name__ == "__main__":
    app()
