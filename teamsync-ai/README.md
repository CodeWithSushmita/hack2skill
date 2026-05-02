# TeamSync AI

A Team Collaboration Tool powered by Google Gemini API, designed to be deployable on Google Cloud Run.

## Features
- **Task Management**: Create, view, update, and delete tasks.
- **AI Task Prioritization**: Leverage Gemini to automatically suggest task priorities.
- **AI Daily Standup**: Generate daily summaries of tasks.
- **Team Chat**: Ask questions about tasks and project status directly to the AI.

## Setup

1. Copy `.env.example` to `.env` and fill in your Gemini API Key:
   ```bash
   cp .env.example .env
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run locally:
   ```bash
   streamlit run app.py
   ```

## Cloud Run Deployment URL
[Placeholder for Cloud Run URL]
