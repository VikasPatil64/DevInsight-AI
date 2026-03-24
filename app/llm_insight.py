from urllib import response

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
           "model": "google/gemma-7b-it:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
        },
    )
    
# ✅ ADD THIS CHECK HERE
    if response.status_code != 200:
        print("API ERROR:", response.text)
        return "AI service temporarily unavailable"
        
    try:
        data = response.json()
        print("STATUS:", response.status_code)
        print("RESPONSE:", data)
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("ERROR:", e)
        print("RAW RESPONSE:", response.text)
        return "AI insight generation failed."