# Cloud Security AI Agent

AI-powered CLI tool that scans, explains, and safely fixes insecure Terraform configurations in AWS environments.

---

## Architecture Design

![AI Agent Architecture](diagram.png)

--- 

## Real-World Problem

Modern cloud infrastructure is defined as code using tools like Terraform. However:
- Developers often use overly permissive defaults
- Security misconfigurations go unnoticed
- Fixing issues requires cloud and security expertise
- Manual reviews are slow, inconsistent, and error-prone

Common issues include:
- Security groups open to the internet (`0.0.0.0/0`)
- IAM policies granting full access (`"*"` or `*:*`)
- Lack of clear visibility into risk and impact

---

## Project Overview

This project implements a CLI-based DevOps assistant that:
- Scans Terraform code for security issues
- Explains issues in clear, simple terms
- Suggests and applies fixes safely
- Prevents unintended changes using dry-run mode
- Displays exact diffs before applying changes
- Creates backups to enable rollback

---

## Features

### Scan

Detects common cloud security misconfigurations:

- Open security groups (`0.0.0.0/0`)
- Overly permissive IAM policies (`"*"` or wildcard access)
- Publicly accessible S3 buckets
- Hardcoded secrets in Terraform files

```bash
python cli.py scan examples/insecure_terraform
```

---

### Explain (AI-powered)

Explains issues in simple terms:

```bash
python cli.py explain 1
```

Example output:

```bash
Problem:
Your IAM policy allows all actions (*)

Why it matters:
This can lead to privilege escalation and full account compromise

Fix:
Restrict permissions to least privilege
```

---

### Fix (Safe Remediation)

Applies fixes interactively with user confirmation:

```bash
python cli.py fix 1 examples/insecure_terraform
```

---

### Dry-Run Mode

Preview changes without modifying files:

```bash
python cli.py fix 1 examples/insecure_terraform --dry-run
```

---

### Diff Preview

Displays exact changes before applying:

```bash
- cidr_blocks = ["0.0.0.0/0"]
+ cidr_blocks = ["10.0.0.0/16"]
```

---

### Severity Summary

Displays a summary of detected issues by severity level:

```text
HIGH: 3 | MEDIUM: 1 | LOW: 0
```

---

### Backup and Restore

Creates a backup before applying changes:

```bash
main.tf -> main.tf.bak
```

This allows safe rollback if needed.

---

## Technology Stack
- Python
- Typer (CLI framework)
- Rich (terminal output)
- OpenAI API (AI explanations)
- Terraform (infrastructure as code)

---

## Design Decisions

- Safe by default: no automatic destructive changes
- Dry-run support: similar to Terraform plan/apply workflow
- Diff visibility: full transparency before execution
- Fallback handling: tool remains usable without AI API
- Modular rules: easy to extend with additional checks

---

## What This Solves

This tool addresses the gap between:
- Infrastructure deployment
- Security best practices

It provides:
- Immediate detection of security issues across network, IAM, storage, and secrets
- Clear explanations suitable for junior engineers
- Safe and controlled remediation workflows
- Risk visibility through severity classification
- Reduced likelihood of human error in infrastructure changes

---

## What I Learned

- Translating cloud security concepts into automation
- Designing safe infrastructure tooling
- Handling edge cases such as API failures and validation
- Building CLI tools with production-style usability

---

## Future Improvements

- CI/CD integration (GitHub Actions)
- Terraform plan parsing
- Policy-as-code integration (OPA)
- Multi-cloud support (Azure, GCP)

---

## Demo
python cli.py scan examples/insecure_terraform
python cli.py explain 1
python cli.py fix 1 examples/insecure_terraform --dry-run

The scan output includes:
- Detected issues across multiple security domains
- Severity classification
- Summary of overall risk levels

---

## Summary

Built a CLI-based AI assistant that analyzes, explains, and safely remediates insecure cloud infrastructure configurations.

---

## Author

Sebastian Silva C. - Cloud Engineer – Secure Infrastructure & Automation - Berlin, Germany
