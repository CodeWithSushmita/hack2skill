import json
from .gemini_client import generate_text

def prioritize_tasks(tasks: list) -> str:
    """Uses Gemini to suggest priorities for a list of tasks."""
    if not tasks:
        return "No tasks to prioritize."

    task_descriptions = "\n".join([f"- {t['title']}: {t['description']} (Assignee: {t['assignee']}, Status: {t['status']})" for t in tasks])
    prompt = f"""
    You are an AI Project Manager. Review the following team tasks and suggest the optimal priority (High, Medium, Low) for each based on standard software engineering principles.
    Provide a brief justification for each suggestion.

    Tasks:
    {task_descriptions}

    Output Format:
    - **Task Title**: Priority - Justification
    """
    return generate_text(prompt)

def generate_daily_standup(tasks: list) -> str:
    """Generates a daily standup summary from the current task list."""
    if not tasks:
        return "No tasks available to generate a standup."

    task_data = "\n".join([f"- {t['assignee']} is working on: '{t['title']}' ({t['status']})" for t in tasks])
    prompt = f"""
    You are an AI Scrum Master. Generate a daily standup summary based on the following tasks.
    Group the summary by team member, highlighting what is completed ('Done'), what is currently active ('In Progress'), and what is up next ('Todo').
    Keep it concise, professional, and encouraging.

    Task Data:
    {task_data}
    """
    return generate_text(prompt)

def chat_with_team_bot(tasks: list, user_message: str, chat_history: str = "") -> str:
    """Allows the user to chat with an AI assistant that knows about the project context."""
    task_context = "\n".join([f"[{t['status']}] {t['title']} (Assigned to: {t['assignee']})" for t in tasks])
    
    prompt = f"""
    You are a helpful AI Team Assistant for a project called TeamSync AI.
    You have access to the current project tasks. Answer the user's question based on the task context.

    Current Task Context:
    {task_context if tasks else "No tasks currently exist."}

    Chat History:
    {chat_history}

    User: {user_message}
    AI Assistant:
    """
    return generate_text(prompt)
