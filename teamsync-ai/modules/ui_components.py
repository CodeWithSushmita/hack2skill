import streamlit as st

def render_status_badge(status: str):
    """Returns markdown for a colored status badge."""
    colors = {
        "Todo": "lightgrey",
        "In Progress": "#FFD700", # Gold
        "Done": "#32CD32" # LimeGreen
    }
    color = colors.get(status, "lightgrey")
    return f'<span style="background-color: {color}; color: black; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold;">{status}</span>'

def render_priority_badge(priority: str):
    """Returns markdown for a priority badge."""
    colors = {
        "High": "#FF6347", # Tomato
        "Medium": "#FFA500", # Orange
        "Low": "#87CEEB", # SkyBlue
        "AI Suggested": "#9370DB" # MediumPurple
    }
    color = colors.get(priority, "lightgrey")
    return f'<span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold;">{priority}</span>'

def display_task_card(task: dict, update_callback, delete_callback):
    """Renders a single task as a card using Streamlit columns and containers."""
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {task['title']}")
            st.write(task["description"])
            st.markdown(f"**Assignee:** {task['assignee']}")
            
            # Badges
            status_html = render_status_badge(task["status"])
            priority_html = render_priority_badge(task["priority"])
            st.markdown(f"**Status:** {status_html} | **Priority:** {priority_html}", unsafe_allow_html=True)
            
            st.caption(f"Created at: {task['created_at']}")
            
        with col2:
            st.markdown("#### Actions")
            new_status = st.selectbox("Update Status", ["Todo", "In Progress", "Done"], index=["Todo", "In Progress", "Done"].index(task["status"]), key=f"status_{task['id']}")
            if new_status != task["status"]:
                update_callback(task["id"], {"status": new_status})
                st.rerun()
                
            if st.button("Delete Task", key=f"delete_{task['id']}", type="primary"):
                delete_callback(task["id"])
                st.rerun()
