import uuid
import streamlit as st
from datetime import datetime

# Task Schema:
# {
#    "id": str,
#    "title": str,
#    "description": str,
#    "assignee": str,
#    "status": str (Todo, In Progress, Done),
#    "priority": str (Low, Medium, High, AI Suggested),
#    "created_at": str
# }

def initialize_tasks():
    """Ensure the tasks list exists in session state."""
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = []

def get_tasks():
    initialize_tasks()
    return st.session_state["tasks"]

def add_task(title: str, description: str, assignee: str, status: str = "Todo", priority: str = "Medium") -> dict:
    initialize_tasks()
    new_task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "assignee": assignee,
        "status": status,
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state["tasks"].append(new_task)
    return new_task

def update_task(task_id: str, updates: dict):
    initialize_tasks()
    for task in st.session_state["tasks"]:
        if task["id"] == task_id:
            task.update(updates)
            return True
    return False

def delete_task(task_id: str):
    initialize_tasks()
    st.session_state["tasks"] = [t for t in st.session_state["tasks"] if t["id"] != task_id]

def clear_tasks():
    st.session_state["tasks"] = []
