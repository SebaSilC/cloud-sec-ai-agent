
def detect_hardcoded_secrets(tf_content: str):
    keywords = ["password", "secret", "access_key", "secret_key"]

    for keyword in keywords:
        if keyword in tf_content.lower():
            return {
                "issue": "Potential hardcoded secret detected",
                "risk": "HIGH",
                "fix": "Use environment variables or a secrets manager instead of hardcoding"
            }
    return None
