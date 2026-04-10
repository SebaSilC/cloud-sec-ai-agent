def detect_wildcard_iam(tf_content: str):
    if "*:*" in tf_content or '"*"' in tf_content:
        return {
            "issue": "Overly permissive IAM policy (* or *:*)",
            "risk": "HIGH",
            "fix": "Restrict actions and resources to least privilege"
        }
    return None
