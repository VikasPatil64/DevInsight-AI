# -------------------------------
# IMPORTS
# -------------------------------

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

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -------------------------------
# OPTIONAL API ROUTE (JSON)
# Keep if you want API testing
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
# DASHBOARD ROUTE (MAIN FEATURE)
# -------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, username: str):

    profile = get_user_profile(username)
    repos = get_user_repos(username)
    profile = get_user_profile(username)
    # top repos 
    top_repos = sorted(
        repos, 
        key = lambda x: x["stargazers_count"],
        reverse = True
        
    )[:6] # Get top 6 repos

    # If user not found → return landing page again
    if profile is None:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "User not found"
            }
        )

    # Run analytics
    analytics = analyze_repositories(repos)

    # Run scoring
    developer_score, category = calculate_developer_score(profile, analytics)
    # Language distribution
    language_labels = builtins.list(analytics["language_count"].keys())
    language_values = builtins.list(analytics["language_count"].values())

    # Top 5 repos by stars
    sorted_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)
    top_star_repos = sorted_repos[:5]

    repo_labels = [repo["name"] for repo in top_star_repos]
    repo_stars = [repo["stargazers_count"] for repo in top_star_repos]
    ai_insight = generate_llm_insight(profile, analytics)
    # Render dashboard page
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