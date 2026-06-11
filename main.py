# -------------------------------
# IMPORTS
# -------------------------------

from fastapi.responses import StreamingResponse
from app.pdf_generator import generate_developer_report
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import builtins
# GitHub API helpers
from app.github_api import get_user_profile, get_user_repos
from app.llm_insight import generate_llm_insight
# Analytics + Scoring
from app.analysis import analyze_repositories
from app.scoring import calculate_developer_score


# -------------------------------
# APP SETUP
# -------------------------------

app = FastAPI()

# Static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")


# -------------------------------
# HOME ROUTE (Landing Page)
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------
# API ROUTE (JSON)
# -------------------------------

@app.get("/analyze/{username}")
def analyze_user(username: str):
    profile = get_user_profile(username)
    repos = get_user_repos(username)

    if profile is None:
        return {"error": "User not found"}

    analytics = analyze_repositories(repos)
    score, category = calculate_developer_score(profile, analytics)

    return {
        "username": username,
        "public_repos": profile["public_repos"],
        "followers": profile["followers"],
        "following": profile["following"],
        "avatar_url": profile["avatar_url"],
        "name": profile.get("name", username),
        "bio": profile.get("bio", "No bio available"),
        "created_at": profile["created_at"],
        "repo_count_fetched": len(repos),
        "analytics": analytics,
        "developer_score": score,
        "developer_category": category
    }


# -------------------------------
# API ENDPOINT FOR COMPARE FEATURE
# -------------------------------

@app.get("/api/analyze/{username}")
def api_analyze_user(username: str):
    """API endpoint for compare feature - returns JSON only"""
    profile = get_user_profile(username)
    repos = get_user_repos(username)

    if profile is None:
        return {"error": "User not found"}

    analytics = analyze_repositories(repos)
    score, category = calculate_developer_score(profile, analytics)
    
    language_labels = list(analytics.get("language_count", {}).keys())
    language_values = list(analytics.get("language_count", {}).values())

    return {
        "username": username,
        "name": profile.get("name", username),
        "avatar_url": profile["avatar_url"],
        "public_repos": profile["public_repos"],
        "followers": profile["followers"],
        "following": profile["following"],
        "developer_score": score,
        "developer_category": category,
        "analytics": {
            "average_stars": analytics.get("average_stars", 0),
            "average_forks": analytics.get("average_forks", 0),
            "most_used_language": analytics.get("most_used_language", "N/A"),
            "total_languages": analytics.get("total_languages", 0),
            "days_since_last_update": analytics.get("days_since_last_update", 0),
            "top_repo_name": analytics.get("top_repo_name", "N/A")
        }
    }


# -------------------------------
# DOWNLOAD PDF ROUTE
# -------------------------------

@app.get("/download/{username}")
async def download_pdf(username: str):
    """Download developer report as PDF"""
    profile = get_user_profile(username)
    if profile is None:
        return {"error": "User not found"}
    
    repos = get_user_repos(username)
    analytics = analyze_repositories(repos)
    score, category = calculate_developer_score(profile, analytics)
    
    try:
        ai_insight = generate_llm_insight(profile, analytics)
        if ai_insight in ["AI insight generation failed.", "AI service temporarily unavailable"]:
            ai_insight = "AI insights temporarily unavailable"
    except:
        ai_insight = "AI insights not available"
    
    pdf_buffer = generate_developer_report(
        username=username,
        profile=profile,
        analytics=analytics,
        score=score,
        category=category,
        ai_insight=ai_insight
    )
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=devinsight_{username}.pdf"}
    )


# -------------------------------
# COMPARE PAGE ROUTE
# -------------------------------

@app.get("/compare", response_class=HTMLResponse)
def compare_page(request: Request):
    return templates.TemplateResponse("compare.html", {"request": request})


# -------------------------------
# DASHBOARD ROUTE (MAIN FEATURE)
# -------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, username: str):
    profile = get_user_profile(username)
    repos = get_user_repos(username)

    top_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:6]

    if profile is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "User not found"})

    analytics = analyze_repositories(repos)
    developer_score, category = calculate_developer_score(profile, analytics)
    
    language_labels = list(analytics["language_count"].keys())
    language_values = list(analytics["language_count"].values())

    sorted_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)
    top_star_repos = sorted_repos[:5]

    repo_labels = [repo["name"] for repo in top_star_repos]
    repo_stars = [repo["stargazers_count"] for repo in top_star_repos]
    
    ai_insight = generate_llm_insight(profile, analytics)
    if ai_insight in ["AI insight generation failed.", "AI service temporarily unavailable"]:
        ai_insight = "⚠️ AI analysis currently unavailable. Core insights are still shown below."
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "public_repos": profile["public_repos"],
            "followers": profile["followers"],
            "following": profile["following"],
            "avatar_url": profile["avatar_url"],
            "name": profile.get("name", username),
            "bio": profile.get("bio", "No bio available"),
            "created_at": profile["created_at"],
            "analytics": analytics,
            "developer_score": developer_score,
            "category": category, 
            "top_repos": top_repos,
            "language_labels": language_labels,
            "language_values": language_values,
            "repo_labels": repo_labels,
            "repo_stars": repo_stars,
            "ai_insight": ai_insight
        }
    )