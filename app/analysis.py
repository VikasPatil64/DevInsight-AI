import pandas as pd
from datetime import datetime


def analyze_repositories(repo_data):

    if not repo_data:
        return None

    # Convert JSON → DataFrame
    df = pd.DataFrame(repo_data)

    # -------------------------------
    # LANGUAGE ANALYSIS (Already Exists)
    # -------------------------------

    language_df = df.dropna(subset=["language"])

    language_counts = language_df["language"].value_counts()
    
    most_used_language = (
        language_counts.idxmax()
        if not language_counts.empty
        else "Not Available"
    )

    total_languages = language_df["language"].nunique()
    

    # -------------------------------
    # STAR ANALYSIS (Already Exists)
    # -------------------------------

    avg_stars = df["stargazers_count"].mean()

    # -------------------------------
    # NEW → FORK ANALYSIS
    # -------------------------------

    avg_forks = df["forks_count"].mean()

    # -------------------------------
    # NEW → RECENCY ANALYSIS
    # -------------------------------

    # Convert updated_at → datetime
    df["updated_at"] = pd.to_datetime(df["updated_at"])

    # Find latest update date
    latest_update = df["updated_at"].max()

    # Today date
    today = pd.Timestamp.utcnow()

    # Days since last activity
    days_since_last_update = (today - latest_update).days

    # -------------------------------
    # TOP REPO (Keep Existing)
    # -------------------------------

    top_repo = df.loc[df["stargazers_count"].idxmax()]

    top_repo_name = top_repo["name"]
    top_repo_stars = top_repo["stargazers_count"]

    # -------------------------------
    # RETURN ALL ANALYTICS
    # -------------------------------

    return {
        "most_used_language": most_used_language,
        "total_languages": int(total_languages),

        "average_stars": round(float(avg_stars), 2),
        "average_forks": round(float(avg_forks), 2),

        "days_since_last_update": int(days_since_last_update),

        "top_repo_name": top_repo_name,
        "top_repo_stars": int(top_repo_stars),
        "language_count": language_counts.to_dict(),
    }