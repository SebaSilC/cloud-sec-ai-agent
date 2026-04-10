def detect_open_sg(tf_content: str):
    if "0.0.0.0/0" in tf_content:
        return {
            "issue": "Open Security Group (0.0.0.0/0)",
            "risk": "HIGH",
            "fix": "Restrict CIDR to a trusted IP range"
        }
    return None
