def detect_public_s3(tf_content: str):
    if 'aws_s3_bucket' in tf_content and (
        'acl = "public-read"' in tf_content or
        'acl = "public-read-write"' in tf_content
    ):
        return {
            "issue": "S3 bucket is publicly accessible",
            "risk": "HIGH",
            "fix": "Set ACL to private and use bucket policies for controlled access"
        }
    return None
