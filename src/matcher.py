def calculate_match_score(project, role_keywords):
    project_text = " ".join([
        project.get("title", ""),
        project.get("category", ""),
        project.get("description", ""),
        " ".join(project.get("skills", [])),
        " ".join(project.get("proof_points", []))
    ]).lower()

    matched_keywords = []

    for keyword in role_keywords:
        if keyword.lower() in project_text:
            matched_keywords.append(keyword)

    score = int((len(matched_keywords) / max(len(role_keywords), 1)) * 100)

    return score, matched_keywords


def rank_projects_for_role(projects, selected_role):
    role_keywords = selected_role.get("keywords", [])
    ranked = []

    for project in projects:
        score, matched_keywords = calculate_match_score(project, role_keywords)
        ranked.append({
            "project": project,
            "score": score,
            "matched_keywords": matched_keywords
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked