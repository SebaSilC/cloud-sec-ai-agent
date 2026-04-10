import typer
import json
from rich.console import Console
from rich.panel import Panel

from agent.controller import run_scan
from agent.fixer import fix_issue
from ai.llm import explain_issue

app = typer.Typer()
console = Console()


@app.command()
def scan(path: str):
    """Scan Terraform files"""
    run_scan(path)


@app.command()
def explain(issue_id: int):
    """Explain an issue using AI"""
    with open("logs/last_scan.json", "r") as f:
        issues = json.load(f)

    if issue_id < 1 or issue_id > len(issues):
        console.print("[red]Invalid issue ID[/red]")
        return

    issue = issues[issue_id - 1]

    explanation = explain_issue(issue)

    console.print(Panel.fit(
        explanation,
        title=f"[bold red]Issue {issue_id}: {issue['issue']}[/bold red]",
        border_style="red"
    ))


@app.command()
def fix(issue_id: int, path: str, dry_run: bool = False):
    """Apply fix for an issue (supports dry-run)"""

    with open("logs/last_scan.json", "r") as f:
        issues = json.load(f)

    if issue_id < 1 or issue_id > len(issues):
        console.print("[red]Invalid issue ID[/red]")
        return

    issue = issues[issue_id - 1]

    console.print(f"\n[bold]Issue:[/bold] {issue['issue']}")
    console.print(f"[bold]Suggested fix:[/bold] {issue['fix']}")

    # Only ask confirmation if NOT dry-run
    if not dry_run:
        confirm = input("\nApply fix? (y/n): ")
        if confirm.lower() != "y":
            console.print("[yellow]Cancelled.[/yellow]")
            return

    if dry_run:
        console.print("[yellow]DRY-RUN: No changes will be applied[/yellow]")
        result = fix_issue(issue, path, apply=False)
    else:
        result = fix_issue(issue, path, apply=True)

    console.print(f"[green]{result}[/green]")


if __name__ == "__main__":
    app()
