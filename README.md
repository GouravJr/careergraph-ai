# CareerGraph AI

**AI-powered QR portfolio and recruiter-job matching platform for students and early-career AI engineers.**

CareerGraph AI turns a normal student portfolio into an intelligent recruiter experience. Instead of only sharing a LinkedIn or GitHub link, recruiters can open a QR-based profile, select or paste a target role, and instantly see which projects prove candidate-role fit.

## Live Demo

- Live App: https://careergraph-ai-gourav.streamlit.app/
- GitHub Repository: https://github.com/GouravJr/careergraph-ai

---

## Why I Built This

At career fairs, hackathons, university events, and networking sessions, students usually share only a LinkedIn or GitHub link.

That creates a problem:

- Recruiters meet many students and profiles are easy to forget.
- GitHub projects are often hard to evaluate quickly.
- Students do not know which project impressed which recruiter.
- Follow-up after networking events is usually unstructured.

CareerGraph AI solves this by turning a personal QR code into an interactive recruiter-facing portfolio.

---

## What CareerGraph AI Does

Recruiters and reviewers can:

- Open my QR-based AI portfolio
- View my AI/ML profile and project evidence
- Select a target role such as GenAI Working Student, RAG Engineer Intern, AI/ML Intern, or Data Scientist Intern
- Paste a real job description and get a project-based fit analysis
- See matched skills, possible gaps, and strongest matching projects
- Leave recruiter interest through a lead form

I can use the private dashboard to:

- Track recruiter leads
- See role interest
- Identify top matched projects
- Export leads as CSV
- Prepare follow-up messages

---

## Key Features

### Recruiter View

A clean profile page with:

- Personal AI/ML summary
- Target roles
- Skills snapshot
- GitHub and LinkedIn links
- QR code generation
- Role-based project matching
- Recruiter interest form

### Reviewer Snapshot

A 30-second executive overview for recruiters, TUM reviewers, and industry partners.

It explains:

- Problem
- Solution
- Impact
- Core product features
- Technical architecture
- Project evidence matrix
- Roadmap

### JD Match Mode

Recruiters can paste a job description and receive:

- Overall fit score
- Matched skills
- Possible skill gaps
- Top matching projects
- Recruiter-ready fit summary
- Suggested follow-up message

### Private Lead Dashboard

The dashboard includes:

- Password protection
- Recruiter lead tracking
- Role-interest breakdown
- Company overview
- Follow-up message suggestions
- CSV export

---

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- QR code generation
- JSON-based profile and project data
- Rule-based role matching
- Job-description matching logic
- GitHub deployment workflow
- Streamlit Community Cloud

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
│   ├── jd_matcher.py
│   └── ai_summary.py
│
├── assets/
│   └── screenshots/
│
└── docs/
    ├── architecture.md
    └── project_plan.md