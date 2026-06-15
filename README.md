# CareerGraph AI

**AI-powered QR portfolio and recruiter matching platform for students and early-career AI engineers.**

CareerGraph AI is a personal portfolio intelligence system that helps recruiters understand my profile faster. Instead of only sharing a normal LinkedIn or GitHub link, recruiters can scan a QR code, select the role they are hiring for, and instantly see which of my projects best prove my fit.

The project combines a personal AI/ML portfolio, role-based project matching, recruiter lead capture, and a private dashboard for follow-up tracking.

---

## Problem

At hackathons, career fairs, university events, and networking sessions, students usually share only a LinkedIn profile or GitHub link.

This creates three problems:

1. Recruiters need time to understand which projects are relevant.
2. Good student profiles are forgotten after short conversations.
3. Students have no structured way to track recruiter interest and follow up.

CareerGraph AI solves this by turning a personal QR code into an intelligent recruiter-facing portfolio.

---

## Solution

Recruiters can:

* Open my QR-based portfolio
* Select a target role such as GenAI Working Student, RAG Engineer Intern, AI/ML Intern, or Data Scientist Intern
* See my best matching projects for that role
* View project proof points, skills, and GitHub links
* Leave their contact details and message

I can then use the private dashboard to:

* Track recruiter leads
* See which roles companies are interested in
* Identify the strongest matched project per lead
* Generate follow-up messages

---

## Key Features

### Recruiter View

* Personal AI/ML profile
* Skills snapshot
* Target roles
* Role-based project matching
* Project proof points
* GitHub project links
* Recruiter interest form

### Lead Dashboard

* Stores recruiter leads locally
* Shows total leads
* Tracks unique companies
* Displays most interested role
* Shows role-interest breakdown
* Generates follow-up message drafts

### Project Matching

The current version uses keyword-based matching between role requirements and project descriptions. It ranks projects based on matched skills, project categories, and proof points.

Future versions will use semantic embeddings for deeper project-role matching.

---

## Tech Stack

* Python
* Streamlit
* SQLite
* Pandas
* Plotly
* JSON-based profile/project data
* QR code generation planned
* LLM-based fit summary planned

---

## Current Projects Included

### Agentic Multi-Document Analysis System

Autonomous AI agent for multi-document analysis using LangGraph, LangChain, OCR, FAISS, FastAPI, Streamlit, and Docker.

### OCR-Based RAG Assistant for German and English Documents

RAG + OCR pipeline for document question answering and structured extraction from German and English documents.

### Music-Driven Cityscape Visualization

Real-time audio-reactive visual computing project using Python, Pygame, NumPy, and SciPy.

### UXRVT: Unity XR Visualization Toolkit

Unity-based toolkit for immersive 3D data visualization in XR environments.

### EEG Sleep Scoring using Ensemble Learning and CNN-LSTM

Biomedical ML project for EEG-based sleep stage classification.

### Plant Disease Detection using Transfer Learning

Computer vision project using CNNs and transfer learning for plant disease classification.

---

## Project Structure

```text
careergraph-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── profile.json
│   ├── projects.json
│   └── roles.json
│
├── db/
│   └── leads.db
│
├── src/
│   ├── matcher.py
│   ├── database.py
│   ├── qr_generator.py
│   └── ai_summary.py
│
├── assets/
│   └── screenshots/
│
└── docs/
    ├── architecture.md
    └── project_plan.md
```

---

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/GouravJr/careergraph-ai.git
cd careergraph-ai
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

For Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

---

## Roadmap

### Version 1

* Personal recruiter-facing portfolio
* Role-based project matching
* Recruiter lead form
* Private dashboard

### Version 2

* QR code generation
* Public deployment
* Profile visit tracking
* Export leads as CSV

### Version 3

* Semantic project-role matching using embeddings
* AI-generated recruiter fit summaries
* Personalized follow-up email drafts
* Company/job-description based matching

### Version 4

* Authentication for private dashboard
* Cloud database
* Analytics dashboard
* Multi-user version for students and university career events

---

## Why This Project Matters

CareerGraph AI is not just a portfolio website. It is a small AI product built around a real career problem:

**How can students make their projects easier to understand, remember, and match to industry roles?**

The project demonstrates:

* AI product thinking
* Practical Python development
* Streamlit application building
* Data modeling with JSON and SQLite
* Recruiter/user-focused design
* Role-based project recommendation logic
* End-to-end portfolio packaging

---

## Author

**Gourav Srinivasalu**
AI/ML Engineering Student | Ex-IBM | Agentic AI, RAG & Document Intelligence

* LinkedIn: https://www.linkedin.com/in/gourav-srinivasalu/
* GitHub: https://github.com/GouravJr
