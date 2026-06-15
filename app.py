import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.matcher import rank_projects_for_role
from src.database import init_db, add_lead, get_all_leads
from src.qr_generator import generate_qr_png_bytes
from src.jd_matcher import (
    analyze_job_description,
    generate_fit_summary,
    generate_follow_up_message,
)


BASE_DIR = Path(__file__).parent


def load_json(path):
    with open(BASE_DIR / path, "r", encoding="utf-8") as file:
        return json.load(file)


profile = load_json("data/profile.json")
projects = load_json("data/projects.json")
roles = load_json("data/roles.json")

init_db()


def get_dashboard_password():
    """
    Reads dashboard password from Streamlit secrets if available.
    Falls back to a local development password.
    """
    try:
        return st.secrets.get("DASHBOARD_PASSWORD", "careergraph2026")
    except Exception:
        return "careergraph2026"


def require_dashboard_access():
    """
    Simple password gate for the private lead dashboard.
    """
    if st.session_state.get("dashboard_unlocked", False):
        with st.sidebar:
            if st.button("Lock dashboard"):
                st.session_state.dashboard_unlocked = False
                st.rerun()
        return True

    st.warning("Private dashboard. Enter password to view recruiter leads.")

    with st.form("dashboard_login"):
        password = st.text_input("Dashboard password", type="password")
        submitted = st.form_submit_button("Unlock dashboard")

        if submitted:
            if password == get_dashboard_password():
                st.session_state.dashboard_unlocked = True
                st.success("Dashboard unlocked.")
                st.rerun()
            else:
                st.error("Incorrect password.")

    st.info("For local development, use the demo password configured in the code or Streamlit secrets.")
    return False


st.set_page_config(
    page_title="CareerGraph AI | Gourav Srinivasalu",
    page_icon="🚀",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0rem;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #9CA3AF;
        margin-top: 0rem;
    }

    .impact-card {
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.16);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        min-height: 160px;
        color: #F8FAFC !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }

    .impact-card b {
        color: #FFFFFF !important;
        font-size: 1.05rem;
    }

    .impact-card p {
        color: #CBD5E1 !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


page = st.sidebar.radio(
    "Navigation",
    ["Recruiter View", "Reviewer Snapshot", "JD Match Mode", "My Lead Dashboard"],
)


def render_landing_header():
    st.markdown('<div class="main-title">CareerGraph AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">AI-powered QR portfolio and recruiter-job matching platform</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        CareerGraph AI turns a personal QR profile into an intelligent recruiter experience.
        Recruiters can scan, explore projects, select or paste a role, and instantly see
        which projects prove candidate-role fit.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Profile Mode", "QR-ready")

    with col2:
        st.metric("Project Matching", "Role-aware")

    with col3:
        st.metric("Recruiter Leads", "Trackable")

    with col4:
        st.metric("Fit Summary", "JD-based")


def recruiter_view():
    render_landing_header()

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.header(profile["name"])
        st.write(f"**{profile['headline']}**")
        st.write(profile["summary"])

        st.write("### Target Roles")
        st.write(", ".join(profile["target_roles"]))

    with right:
        st.write("### Links")
        st.link_button("LinkedIn", profile["linkedin"])
        st.link_button("GitHub", profile["github"])
        st.write(f"📍 {profile['location']}")
        st.write(f"📧 {profile['email']}")

        st.write("### QR Profile")

        qr_target = st.selectbox(
            "QR links to:",
            ["LinkedIn Profile", "GitHub Profile"],
            index=0,
        )

        if qr_target == "LinkedIn Profile":
            qr_url = profile["linkedin"]
        else:
            qr_url = profile["github"]

        qr_bytes = generate_qr_png_bytes(qr_url)

        st.image(qr_bytes, caption=f"Scan to open {qr_target}", width=180)

        st.download_button(
            label="Download QR Code",
            data=qr_bytes,
            file_name="gourav_profile_qr.png",
            mime="image/png",
        )

    st.divider()

    st.header("Why this profile is relevant")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="impact-card">
                <b>Applied AI Systems</b>
                <p>
                Built projects around RAG, OCR, document intelligence, and agentic AI.
                The focus is on practical AI workflows, not generic chatbot demos.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="impact-card">
                <b>Industry Data Experience</b>
                <p>
                IBM experience includes Python and SQL pipelines, ML models,
                reporting automation, dashboards, and measurable business impact.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="impact-card">
                <b>Recruiter-Friendly Proof</b>
                <p>
                Projects are mapped to target roles, matched skills, proof points,
                and GitHub repositories so recruiters can evaluate fit quickly.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.header("Skills Snapshot")

    skill_cols = st.columns(4)
    for index, skill in enumerate(profile["skills"]):
        with skill_cols[index % 4]:
            st.markdown(f"- {skill}")

    st.divider()

    st.header("Role-Based Project Match")

    role_names = [role["role"] for role in roles]
    selected_role_name = st.selectbox(
        "Select the role you are hiring for:",
        role_names,
    )

    selected_role = next(role for role in roles if role["role"] == selected_role_name)
    ranked_projects = rank_projects_for_role(projects, selected_role)

    top_project = ranked_projects[0]["project"]["title"] if ranked_projects else ""

    st.write(f"### Best projects for: {selected_role_name}")

    for item in ranked_projects:
        project = item["project"]
        score = item["score"]
        matched_keywords = item["matched_keywords"]

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(project["title"])
                st.caption(f"{project['period']} | {project['category']}")
                st.write(project["description"])

                st.write("**Proof points:**")
                for point in project["proof_points"]:
                    st.markdown(f"- {point}")

                st.write("**Skills:** " + ", ".join(project["skills"]))

                if project["github"]:
                    st.link_button("View GitHub Repository", project["github"])

            with col2:
                st.metric("Match Score", f"{score}%")
                if matched_keywords:
                    st.write("**Matched keywords:**")
                    for keyword in matched_keywords:
                        st.markdown(f"- {keyword}")

    st.divider()

    st.header("IBM Experience Highlights")

    for highlight in profile["experience_highlights"]:
        st.markdown(f"- {highlight}")

    st.divider()

    st.header("Interested in my profile?")

    st.write(
        "Leave your details here and I can follow up with a role-specific message."
    )

    with st.form("lead_form"):
        name = st.text_input("Your name *")
        email = st.text_input("Email or LinkedIn")
        company = st.text_input("Company / Organization")
        recruiter_message = st.text_area(
            "Message",
            placeholder="Example: We are hiring for a GenAI Working Student role...",
        )

        submitted = st.form_submit_button("Save recruiter interest")

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            else:
                add_lead(
                    name=name.strip(),
                    email=email.strip(),
                    company=company.strip(),
                    role_interest=selected_role_name,
                    recruiter_message=recruiter_message.strip(),
                    top_project=top_project,
                )
                st.success("Thank you. Your interest has been saved.")


def reviewer_snapshot():
    st.title("Reviewer Snapshot")
    st.subheader("30-second overview for recruiters, TUM reviewers, and industry partners")

    st.markdown(
        """
        **CareerGraph AI** is an AI-powered QR portfolio and recruiter-job matching platform.
        It turns a normal student profile into an intelligent, role-aware career interface.

        Instead of asking recruiters to manually inspect LinkedIn, GitHub, and project descriptions,
        the platform maps my projects to target roles, job descriptions, proof points, and recruiter follow-up actions.
        """
    )

    st.divider()

    st.header("Problem → Solution → Impact")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### Problem
            Recruiters meet many students at events, but profiles are hard to remember and compare.
            LinkedIn and GitHub alone do not clearly show which projects prove fit for a specific role.
            """
        )

    with col2:
        st.markdown(
            """
            ### Solution
            A QR-based AI portfolio where recruiters can select or paste a role and instantly see
            matched projects, skills, proof points, and follow-up suggestions.
            """
        )

    with col3:
        st.markdown(
            """
            ### Impact
            Faster candidate understanding, better follow-up after networking events,
            and a stronger bridge between student projects and industry hiring needs.
            """
        )

    st.divider()

    st.header("Core Product Features")

    feature_data = [
        {
            "Feature": "QR Portfolio",
            "What it does": "Turns a personal QR code into a recruiter-facing profile.",
            "Recruiter Value": "Fast access during events and networking.",
        },
        {
            "Feature": "Role-Based Project Match",
            "What it does": "Ranks projects based on target roles like GenAI, RAG, ML, and Data Science.",
            "Recruiter Value": "Shows relevant proof instead of generic project lists.",
        },
        {
            "Feature": "JD Match Mode",
            "What it does": "Analyzes pasted job descriptions against skills and project evidence.",
            "Recruiter Value": "Makes candidate-role fit easier to evaluate.",
        },
        {
            "Feature": "Lead Dashboard",
            "What it does": "Tracks recruiter interest, role selection, company, and follow-up context.",
            "Recruiter Value": "Shows product thinking around long-term networking.",
        },
        {
            "Feature": "Follow-Up Generator",
            "What it does": "Creates role-specific follow-up messages.",
            "Recruiter Value": "Converts profile views into real career conversations.",
        },
    ]

    st.dataframe(feature_data, use_container_width=True, hide_index=True)

    st.divider()

    st.header("Technical Architecture")

    st.markdown(
        """
        ```text
        Recruiter / Reviewer
                |
                v
        Streamlit Frontend
                |
                |-- Profile + Projects JSON
                |-- Role Matching Logic
                |-- JD Matching Logic
                |-- QR Generator
                |
                v
        SQLite Lead Database
                |
                v
        Lead Dashboard + Follow-Up Suggestions
        ```
        """
    )

    st.divider()

    st.header("Project Evidence Matrix")

    evidence_rows = []

    for project in projects:
        evidence_rows.append(
            {
                "Project": project["title"],
                "Category": project["category"],
                "Main Skills": ", ".join(project["skills"][:5]),
                "Recruiter Signal": project["proof_points"][0]
                if project["proof_points"]
                else "Project evidence available",
            }
        )

    st.dataframe(evidence_rows, use_container_width=True, hide_index=True)

    st.divider()

    st.header("Why this is stronger than a normal portfolio")

    st.markdown(
        """
        - It is **interactive**, not just a static webpage.
        - It connects **projects to job roles**, not just skills to keywords.
        - It includes **recruiter lead capture**, making networking measurable.
        - It has a **JD matching mode**, making it useful during real hiring conversations.
        - It demonstrates **AI product thinking**, not only coding ability.
        """
    )

    st.divider()

    st.header("Next Roadmap")

    roadmap = [
        "Deploy public Streamlit app and connect QR code to live demo.",
        "Add screenshots and demo GIFs to GitHub README.",
        "Add semantic embeddings for better project-job matching.",
        "Add password protection for private lead dashboard.",
        "Add export to CSV for recruiter leads.",
        "Add architecture diagram and product demo video.",
    ]

    for item in roadmap:
        st.markdown(f"- {item}")


def jd_match_mode():
    st.title("JD Match Mode")
    st.subheader("Paste a job description and see project-based candidate fit")

    st.markdown(
        """
        This mode is designed for recruiters and industry reviewers. It connects a job description
        to concrete project evidence, matched skills, possible gaps, and a recruiter-ready fit summary.
        """
    )

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        job_title = st.text_input("Job title", value="GenAI Working Student")
        company = st.text_input("Company", value="Example Company")

    with col2:
        st.info(
            "Tip: Paste a real working student, internship, or AI/ML job description. "
            "The system will rank projects based on evidence."
        )

    job_description = st.text_area(
        "Job description",
        height=220,
        placeholder=(
            "Paste a job description here. Example: We are looking for a working student "
            "with Python, LangChain, RAG, FastAPI, Docker, SQL, and experience building AI applications..."
        ),
    )

    if st.button("Analyze Fit"):
        if not job_description.strip():
            st.error("Please paste a job description first.")
            return

        analysis = analyze_job_description(
            profile=profile,
            projects=projects,
            job_title=job_title,
            company=company,
            job_description=job_description,
        )

        st.divider()

        st.header("Fit Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Overall Fit Score", f"{analysis['fit_score']}%")

        with c2:
            st.metric("Matched Skills", len(analysis["matched_skills"]))

        with c3:
            st.metric("Skill Gaps", len(analysis["gap_skills"]))

        st.write("### Matched Skills")
        if analysis["matched_skills"]:
            st.write(", ".join(analysis["matched_skills"]))
        else:
            st.warning("No direct skill matches found from the known skill list.")

        st.write("### Possible Skill Gaps")
        if analysis["gap_skills"]:
            st.write(", ".join(analysis["gap_skills"]))
        else:
            st.success("No major gap detected from the current skill list.")

        st.divider()

        st.header("Top Matching Projects")

        for item in analysis["ranked_projects"]:
            project = item["project"]

            with st.container(border=True):
                col_left, col_right = st.columns([3, 1])

                with col_left:
                    st.subheader(project["title"])
                    st.caption(project["category"])
                    st.write(project["description"])

                    if item["matched_terms"]:
                        st.write(
                            "**Evidence matched:** "
                            + ", ".join(item["matched_terms"][:12])
                        )

                    if project["github"]:
                        st.link_button("View GitHub Repository", project["github"])

                with col_right:
                    st.metric("Project Match", f"{item['score']}%")

        st.divider()

        st.header("Recruiter-Ready Fit Summary")

        fit_summary = generate_fit_summary(
            profile=profile,
            job_title=job_title,
            company=company,
            analysis=analysis,
        )

        st.text_area(
            "Fit summary",
            value=fit_summary,
            height=140,
        )

        st.header("Follow-up Message")

        follow_up = generate_follow_up_message(
            profile=profile,
            job_title=job_title,
            company=company,
            analysis=analysis,
        )

        st.text_area(
            "Suggested follow-up",
            value=follow_up,
            height=180,
        )


def dashboard_view():
    st.title("My Lead Dashboard")
    st.subheader("Track recruiter interest from QR scans and portfolio visits")

    if not require_dashboard_access():
        return

    leads = get_all_leads()

    if not leads:
        st.info("No recruiter leads saved yet.")
        return

    columns = [
        "ID",
        "Name",
        "Email / LinkedIn",
        "Company",
        "Role Interest",
        "Message",
        "Top Matched Project",
        "Created At",
    ]

    df = pd.DataFrame(leads, columns=columns)

    total_leads = len(df)
    unique_companies = df["Company"].replace("", pd.NA).dropna().nunique()
    most_common_role = df["Role Interest"].mode()[0] if not df.empty else "N/A"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Leads", total_leads)

    with col2:
        st.metric("Unique Companies", unique_companies)

    with col3:
        st.metric("Most Interested Role", most_common_role)

    st.divider()

    st.write("### Role Interest Breakdown")
    role_counts = df["Role Interest"].value_counts()
    st.bar_chart(role_counts)

    st.divider()

    st.write("### Recruiter Leads")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download leads as CSV",
        data=csv_data,
        file_name="careergraph_recruiter_leads.csv",
        mime="text/csv",
    )

    st.divider()

    st.write("### Follow-up Suggestions")

    for _, row in df.iterrows():
        with st.container(border=True):
            st.write(f"**{row['Name']}** — {row['Company']}")
            st.write(f"Interested role: **{row['Role Interest']}**")
            st.write(f"Top matched project: **{row['Top Matched Project']}**")

            follow_up = (
                f"Hi {row['Name']}, thank you for checking out my CareerGraph AI profile. "
                f"I noticed your interest in {row['Role Interest']} roles. "
                f"My strongest matching project is {row['Top Matched Project']}, where I worked with "
                f"AI/ML systems, practical implementation, and deployment-focused tooling. "
                f"I would be happy to discuss how my background could fit opportunities at {row['Company']}."
            )

            st.text_area(
                "Suggested follow-up message",
                value=follow_up,
                height=120,
                key=f"followup_{row['ID']}",
            )


if page == "Recruiter View":
    recruiter_view()
elif page == "Reviewer Snapshot":
    reviewer_snapshot()
elif page == "JD Match Mode":
    jd_match_mode()
else:
    dashboard_view()