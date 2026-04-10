import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def explain_issue(issue: dict):
    prompt = f"""
You are a cloud security expert.

Explain the following issue clearly and ONLY about cloud security.

Issue: {issue['issue']}
Risk: {issue['risk']}
Fix: {issue['fix']}

Respond ONLY in this format:

Problem:
Why it matters:
Fix:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[Fallback] Could not reach AI: {str(e)}"
