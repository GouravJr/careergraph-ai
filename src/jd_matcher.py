import re


CANONICAL_SKILLS = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "Data Science",
    "LangChain", "LangGraph", "RAG", "LLM", "GenAI", "FAISS",
    "Vector Database", "Embeddings", "OCR", "Tesseract", "FastAPI",
    "Streamlit", "Docker", "Git", "CI/CD", "MLflow", "PyTorch",
    "TensorFlow", "Scikit-learn", "Pandas", "NumPy", "Power BI",
    "Tableau", "Data Pipelines", "APIs", "Backend", "Cloud",
    "GCP", "Azure", "AWS", "Kubernetes", "PostgreSQL", "React"
]


def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def skill_in_text(skill, text):
    return skill.lower() in text


def collect_candidate_skills(profile, projects):
    skills = set(profile.get("skills", []))

    for project in projects:
        for skill in project.get("skills", []):
            skills.add(skill)

    return sorted(skills)


def build_project_text(project):
    return normalize_text(
        " ".join([
            project.get("title", ""),
            project.get("category", ""),
            project.get("description", ""),
            " ".join(project.get("skills", [])),
            " ".join(project.get("proof_points", []))
        ])
    )


def rank_projects_for_jd(projects, job_description):
    jd_text = normalize_text(job_description)
    ranked = []

    for project in projects:
        project_text = build_project_text(project)

        matched_terms = []

        for skill in CANONICAL_SKILLS:
            if skill_in_text(skill, jd_text) and skill_in_text(skill, project_text):
                matched_terms.append(skill)

        for word in jd_text.split():
            if len(word) > 4 and word in project_text and word not in matched_terms:
                matched_terms.append(word)

        score = min(100, len(set(matched_terms)) * 12)

        ranked.append({
            "project": project,
            "score": score,
            "matched_terms": sorted(set(matched_terms))
        })

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked


def analyze_job_description(profile, projects, job_title, company, job_description):
    jd_text = normalize_text(" ".join([job_title, company, job_description]))

    candidate_skills = collect_candidate_skills(profile, projects)
    candidate_skills_lower = [skill.lower() for skill in candidate_skills]

    jd_required_skills = [
        skill for skill in CANONICAL_SKILLS
        if skill_in_text(skill, jd_text)
    ]

    matched_skills = [
        skill for skill in jd_required_skills
        if skill.lower() in candidate_skills_lower
    ]

    gap_skills = [
        skill for skill in jd_required_skills
        if skill.lower() not in candidate_skills_lower
    ]

    ranked_projects = rank_projects_for_jd(projects, job_description)

    skill_score = int((len(matched_skills) / max(len(jd_required_skills), 1)) * 100)
    project_score = ranked_projects[0]["score"] if ranked_projects else 0

    fit_score = int((0.65 * skill_score) + (0.35 * project_score))
    fit_score = min(100, fit_score)

    return {
        "fit_score": fit_score,
        "matched_skills": matched_skills,
        "gap_skills": gap_skills,
        "ranked_projects": ranked_projects[:3]
    }


def generate_fit_summary(profile, job_title, company, analysis):
    name = profile.get("name", "The candidate")
    top_projects = analysis.get("ranked_projects", [])

    if top_projects:
        best_project = top_projects[0]["project"]["title"]
    else:
        best_project = "the candidate's AI/ML project portfolio"

    matched = analysis.get("matched_skills", [])
    gaps = analysis.get("gap_skills", [])

    matched_text = ", ".join(matched[:8]) if matched else "relevant AI/ML and software engineering skills"
    gap_text = ", ".join(gaps[:4]) if gaps else "no major obvious skill gap from the provided description"

    return (
        f"{name} appears to be a strong candidate for the {job_title} role at {company}. "
        f"The strongest evidence comes from {best_project}, supported by matched skills such as {matched_text}. "
        f"The profile is especially relevant for applied AI, RAG, document intelligence, Python-based development, "
        f"and deployment-oriented AI systems. Potential areas to strengthen for this specific role: {gap_text}."
    )


def generate_follow_up_message(profile, job_title, company, analysis):
    name = profile.get("name", "Gourav")
    top_projects = analysis.get("ranked_projects", [])

    if top_projects:
        best_project = top_projects[0]["project"]["title"]
    else:
        best_project = "my AI/ML project portfolio"

    return (
        f"Hi, thank you for checking my CareerGraph AI profile. "
        f"I noticed that the {job_title} role at {company} matches my background in AI/ML engineering. "
        f"My strongest related project is {best_project}, where I worked on practical AI systems, "
        f"project-based implementation, and recruiter-relevant technical proof points. "
        f"I would be happy to discuss how my experience and projects could fit this opportunity.\n\n"
        f"Best regards,\n{name}"
    )