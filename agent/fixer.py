from pathlib import Path
import difflib


def fix_issue(issue: dict, base_path: str, apply: bool = True):
    file_path = Path(base_path) / issue["file"]

    if not file_path.exists():
        return "File not found"

    original = file_path.read_text()

    # Apply simple fixes
    if "0.0.0.0/0" in original:
        fixed = original.replace("0.0.0.0/0", "10.0.0.0/16")
    elif '"*"' in original:
        fixed = original.replace('"*"', '"ec2:Describe*"')
    else:
        return "No automatic fix available"

    # Generate diff
    diff = difflib.unified_diff(
        original.splitlines(),
        fixed.splitlines(),
        fromfile="before",
        tofile="after",
        lineterm=""
    )

    diff_output = "\n".join(diff)

    # Show diff ALWAYS
    print("\n--- Diff Preview ---")
    print(diff_output)

    # Apply change if allowed
    if apply:
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        backup_path.write_text(original)

        # Apply fix
        file_path.write_text(fixed)

        return f"Applied fix to {issue['file']} (backup saved as {backup_path.name})"
    else:
        return f"Would fix {issue['file']}"
