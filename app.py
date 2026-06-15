import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.matcher import rank_projects_for_role
from src.database import init_db, add_lead, get_all_leads


BASE_DIR = Path(__file__).parent


def load_json(path):
    with open(BASE_DIR / path, "r", encoding="utf-8") as file:
        return json.load(file)


profile = load_json("data/profile.json")
projects = load_json("data/projects.json")
roles = load_json("data/roles.json")

init_db()

st.set_page_config(
    page_title="CareerGraph AI | Gourav Srinivasalu",
    page_icon="🚀",
    layout="wide"
)

page = st.sidebar.radio(
    "Navigation",
    ["Recruiter View", "My Lead Dashboard"]
)


def recruiter_view():
    st.title("CareerGraph AI")
    st.subheader("AI-Powered QR Portfolio & Recruiter Matching Platform")

    st.markdown(
        """
        Recruiters can scan my QR profile, select a target role, and instantly see
        which of my projects prove my fit.
        """
    )

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
        role_names
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
            placeholder="Example: We are hiring for a GenAI Working Student role..."
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
                    top_project=top_project
                )
                st.success("Thank you. Your interest has been saved.")


def dashboard_view():
    st.title("My Lead Dashboard")
    st.subheader("Track recruiter interest from QR scans and portfolio visits")

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
        "Created At"
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
                key=f"followup_{row['ID']}"
            )


if page == "Recruiter View":
    recruiter_view()
else:
    dashboard_view()