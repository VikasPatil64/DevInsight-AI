# -------------------------------
# PHASE 1 DEVELOPER SCORING ENGINE
# -------------------------------

def recency_score(days_since_update):
    """
    Convert days since last activity → score (0–100)
    """

    if days_since_update <= 30:
        return 100
    elif days_since_update <= 90:
        return 80
    elif days_since_update <= 180:
        return 60
    elif days_since_update <= 365:
        return 40
    else:
        return 20


def impact_score(avg_stars, avg_forks):
    """
    Combine stars + forks → impact score
    """

    # Weighted raw impact
    impact_raw = (avg_stars * 0.6) + (avg_forks * 0.4)

    # Convert raw → bucket score
    if impact_raw >= 20:
        return 100
    elif impact_raw >= 10:
        return 80
    elif impact_raw >= 5:
        return 60
    elif impact_raw >= 1:
        return 40
    else:
        return 20


def volume_score(repo_count):
    """
    Repo count → experience score
    """

    if repo_count >= 50:
        return 100
    elif repo_count >= 30:
        return 80
    elif repo_count >= 15:
        return 60
    elif repo_count >= 5:
        return 40
    else:
        return 20


# -------------------------------
# FINAL COMBINED SCORE
# -------------------------------

def calculate_developer_score(profile_data, analytics_data):

    # Extract needed values
    repo_count = profile_data.get("public_repos", 0)

    avg_stars = analytics_data.get("average_stars", 0)
    avg_forks = analytics_data.get("average_forks", 0)

    days_since_update = analytics_data.get("days_since_last_update", 9999)

    # Individual Scores
    rec_score = recency_score(days_since_update)
    imp_score = impact_score(avg_stars, avg_forks)
    vol_score = volume_score(repo_count)

    # Final Weighted Score (Phase 1)
    final_score = (
        rec_score * 0.30 +
        imp_score * 0.25 +
        vol_score * 0.10
    )

    final_score = round(final_score)

    # Category Label
    if final_score >= 85:
        category = "Elite Developer"
    elif final_score >= 70:
        category = "Strong Developer"
    elif final_score >= 50:
        category = "Growing Developer"
    else:
        category = "Beginner Developer"

    return final_score, category