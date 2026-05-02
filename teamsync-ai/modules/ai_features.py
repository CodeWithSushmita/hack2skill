import json
from .gemini_client import call_llm

def prioritize_tasks(tasks: list) -> str:
    """Uses LLM to suggest priorities for a list of tasks."""
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
    return call_llm(prompt)

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
    return call_llm(prompt)

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
    return call_llm(prompt)

def summarize_meeting_notes(transcript: str) -> str:
    """Summarizes a meeting transcript into key points and action items."""
    if not transcript.strip():
        return "No transcript provided."
        
    prompt = f"""
    You are an AI Meeting Assistant. Summarize the following meeting transcript.
    Extract the key discussion points, decisions made, and a clear list of action items (with assignees if mentioned).
    
    Transcript:
    {transcript}
    """
    return call_llm(prompt)

def get_dashboard_insight(tasks: list) -> str:
    """Generates a real-time insight about the current task board."""
    if not tasks:
        return "No active tasks. Add tasks to see AI insights."
    
    task_context = "\n".join([f"- [{t['status']}] {t['title']} (Priority: {t['priority']})" for t in tasks])
    prompt = f"""
    Given these tasks, give ONE specific actionable insight about workload, blockers, or priorities in under 30 words.
    
    Tasks:
    {task_context}
    """
    return call_llm(prompt)

def assess_risk_level(tasks: list) -> str:
    """Assesses the overall project risk based on tasks."""
    if not tasks:
        return "Low "
        
    task_context = "\n".join([f"- [{t['status']}] {t['title']} (Priority: {t['priority']})" for t in tasks])
    prompt = f"""
    You are an AI Risk Analyst. Based on the following tasks, assess the overall project risk level.
    Return ONLY ONE of these exact strings: "Low ", "Medium ", or "High ".
    Do not include any other text or explanation.
    
    Tasks:
    {task_context}
    """
    return call_llm(prompt).strip()

def generate_risk_report(tasks: list) -> str:
    """Generates a structured risk report."""
    if not tasks:
        return "No tasks to analyze."
        
    task_context = "\n".join([f"- {t['title']} (Assignee: {t['assignee']}, Status: {t['status']}, Priority: {t['priority']})" for t in tasks])
    prompt = f"""
    You are a senior project manager. Analyze these tasks and return a structured risk report with: 
     Critical Risks,  Warnings,  What's on track, and  Recommendations. 
    Be specific and actionable.
    
    Tasks:
    {task_context}
    """
    return call_llm(prompt)

def get_risk_metrics(tasks: list) -> dict:
    """Generates numerical risk metrics using LLM."""
    if not tasks:
        return {"at_risk": 0, "overloaded": 0, "priority_changes": 0}
        
    task_context = "\n".join([f"- {t['title']} (Assignee: {t['assignee']}, Status: {t['status']}, Priority: {t['priority']})" for t in tasks])
    prompt = f"""
    Analyze these tasks and return ONLY a valid JSON object with three integer keys:
    "at_risk": (number of tasks that are high risk or blocked),
    "overloaded": (number of team members assigned to too many tasks),
    "priority_changes": (number of tasks that need priority adjustment).
    
    Tasks:
    {task_context}
    """
    try:
        response = call_llm(prompt, "You are a data system. Output ONLY raw JSON, without markdown formatting or backticks.")
        cleaned = response.strip().replace("```json", "").replace("```", "")
        data = json.loads(cleaned)
        return {
            "at_risk": data.get("at_risk", 0), 
            "overloaded": data.get("overloaded", 0), 
            "priority_changes": data.get("priority_changes", 0)
        }
    except Exception as e:
        return {"at_risk": "?", "overloaded": "?", "priority_changes": "?"}

def generate_task_description(title: str) -> str:
    """Generates a smart task description based on the title."""
    prompt = f"""
    Write a clear, concise task description (2-3 sentences) for a software team task titled: '{title}'.
    Include what needs to be done, expected outcome, and any technical considerations.
    """
    return call_llm(prompt)
