import requests
import os

OPENROUTER_API_KEY = "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"

def generate_llm_insight(profile, analytics):

    prompt = f"""
You are a professional software engineering mentor.

Analyze this developer profile:

Public Repositories: {profile["public_repos"]}
Followers: {profile["followers"]}
Average Stars: {analytics["average_stars"]}
Average Forks: {analytics["average_forks"]}
Days Since Last Activity: {analytics["days_since_last_update"]}
Most Used Language: {analytics["most_used_language"]}
Total Languages Used: {analytics["total_languages"]}

Generate:
1. Professional performance summary
2. Strengths
3. Weaknesses
4. Skill improvement suggestions

Be concise, professional, and structured.
Use bullet points.
Avoid unnecessary explanations.
Keep output under 150 words..
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
        },
    )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "AI insight generation failed."