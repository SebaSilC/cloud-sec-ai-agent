from pathlib import Path
import json
from typing import TypedDict, List
from rich.console import Console
from rich.table import Table

from rules.security_groups import detect_open_sg
from rules.iam import detect_wildcard_iam
from rules.s3 import detect_public_s3
from rules.secrets import detect_hardcoded_secrets

console = Console()


class Issue(TypedDict):
    issue: str
    risk: str
    fix: str
    file: str


def run_scan(path: str):
    issues: List[Issue] = []
    path = Path(path)

    if not path.exists():
        console.print(f"[red]Path not found:[/red] {path}")
        return

    for file in path.glob("*.tf"):
        try:
            content = file.read_text()
        except Exception as e:
            console.print(f"[red]Error reading {file}:[/red] {e}")
            continue

        file_issues: List[Issue] = []

        # Security Group check
        sg_issue = detect_open_sg(content)
        if sg_issue:
            file_issues.append(sg_issue)

        # IAM check
        iam_issue = detect_wildcard_iam(content)
        if iam_issue:
            file_issues.append(iam_issue)

        # S3 check
        s3_issue = detect_public_s3(content)
        if s3_issue:
            file_issues.append(s3_issue)

        # Secrets check
        secret_issue = detect_hardcoded_secrets(content)
        if secret_issue:
            file_issues.append(secret_issue)

        # Add file context
        for issue in file_issues:
            issue["file"] = file.name
            issues.append(issue)

    if not issues:
        console.print("[green]✔ No issues found[/green]")
        return

    table = Table(title="Security Scan Results")

    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Severity", style="bold")
    table.add_column("Issue")
    table.add_column("File")
    table.add_column("Fix")

    for i, issue in enumerate(issues, 1):
        severity_color = {
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "green"
        }.get(issue["risk"], "white")

        table.add_row(
            str(i),
            f"[{severity_color}]{issue['risk']}[/{severity_color}]",
            issue["issue"],
            issue["file"],
            issue["fix"]
        )

    console.print(table)

    # Severity summary
    summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for issue in issues:
        level = issue["risk"]
        if level in summary:
            summary[level] += 1

    console.print("\n[bold]Summary:[/bold]")
    console.print(
        f"[red]HIGH: {summary['HIGH']}[/red] | "
        f"[yellow]MEDIUM: {summary['MEDIUM']}[/yellow] | "
        f"[green]LOW: {summary['LOW']}[/green]"
    )

    # Save scan results
    log_path = Path("logs/last_scan.json")
    log_path.parent.mkdir(exist_ok=True)

    with open(log_path, "w") as f:
        json.dump(issues, f, indent=2)
