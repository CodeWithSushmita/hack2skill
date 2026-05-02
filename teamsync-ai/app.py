import streamlit as st
from modules.task_manager import get_tasks, add_task, update_task, delete_task, initialize_tasks
from modules.ui_components import display_task_card
from modules.ai_features import prioritize_tasks, generate_daily_standup, chat_with_team_bot

st.set_page_config(page_title="TeamSync AI", page_icon="🚀", layout="wide")

# Initialize session state
initialize_tasks()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("🚀 TeamSync AI")
st.markdown("Team Collaboration Tool powered by Google Gemini")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["📋 Task Board", "🤖 AI Standup & Priority", "💬 AI Team Chat"])

if page == "📋 Task Board":
    st.header("Task Board")
    
    # Task Creation Form
    with st.expander("➕ Create New Task", expanded=False):
        with st.form("new_task_form", clear_on_submit=True):
            title = st.text_input("Task Title")
            description = st.text_area("Description")
            assignee = st.text_input("Assignee")
            col1, col2 = st.columns(2)
            with col1:
                status = st.selectbox("Initial Status", ["Todo", "In Progress", "Done"])
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                
            submitted = st.form_submit_button("Add Task")
            if submitted and title and assignee:
                add_task(title, description, assignee, status, priority)
                st.success("Task added successfully!")
                st.rerun()
            elif submitted:
                st.error("Title and Assignee are required.")

    st.divider()
    
    # Display Tasks
    tasks = get_tasks()
    if not tasks:
        st.info("No tasks available. Create one above!")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect("Filter by Status", ["Todo", "In Progress", "Done"], default=["Todo", "In Progress", "Done"])
        with col2:
            assignee_filter = st.text_input("Filter by Assignee")
            
        filtered_tasks = [t for t in tasks if t["status"] in status_filter]
        if assignee_filter:
            filtered_tasks = [t for t in filtered_tasks if assignee_filter.lower() in t["assignee"].lower()]
            
        for task in filtered_tasks:
            display_task_card(task, update_task, delete_task)

elif page == "🤖 AI Standup & Priority":
    st.header("AI Team Insights")
    tasks = get_tasks()
    
    tab1, tab2 = st.tabs(["Daily Standup", "Smart Prioritization"])
    
    with tab1:
        st.markdown("Generate a daily standup summary based on current tasks.")
        if st.button("Generate Standup Summary", type="primary"):
            if tasks:
                with st.spinner("Gemini is analyzing the board..."):
                    summary = generate_daily_standup(tasks)
                st.markdown("### Standup Report")
                st.write(summary)
            else:
                st.warning("Add some tasks to the board first!")
                
    with tab2:
        st.markdown("Ask Gemini to review current tasks and suggest priority adjustments.")
        if st.button("Suggest Priorities", type="primary"):
            if tasks:
                with st.spinner("Gemini is evaluating priorities..."):
                    suggestions = prioritize_tasks(tasks)
                st.markdown("### AI Priority Suggestions")
                st.write(suggestions)
            else:
                st.warning("Add some tasks to the board first!")

elif page == "💬 AI Team Chat":
    st.header("TeamSync Assistant")
    st.markdown("Ask questions about the project, tasks, or team status.")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat input
    if prompt := st.chat_input("Ask about the project..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Format chat history for context
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history[:-1]])
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_team_bot(get_tasks(), prompt, history_str)
                st.markdown(response)
                
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
