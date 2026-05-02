import streamlit as st
from modules.task_manager import get_tasks, add_task, update_task, delete_task, initialize_tasks
from modules.ui_components import display_task_card
from modules.ai_features import prioritize_tasks, generate_daily_standup, chat_with_team_bot, summarize_meeting_notes, get_dashboard_insight, assess_risk_level, generate_risk_report, get_risk_metrics, generate_task_description
from modules.llm_client import call_llm

st.set_page_config(page_title="TeamSync AI", page_icon="🚀", layout="wide")

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; padding-bottom: 0 !important; max-width: 1100px !important; }
[data-testid="stSidebar"] { background: #0f1117 !important; min-width: 240px !important; max-width: 240px !important; }
[data-testid="stSidebar"] > div { background: #0f1117 !important; }
[data-testid="stSidebar"] * { color: #9ca3af !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 2px !important; display: flex; flex-direction: column; }
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] { padding: 8px 12px !important; border-radius: 7px !important; font-size: 13px !important; font-weight: 500 !important; cursor: pointer; transition: background 0.15s; }
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover { background: rgba(255,255,255,0.07) !important; }
[data-testid="stSidebar"] [aria-checked="true"] { background: rgba(99,102,241,0.18) !important; color: #a5b4fc !important; }
[data-testid="stSidebar"] [aria-checked="true"] p { color: #a5b4fc !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; margin: 8px 0 !important; }
.stButton > button { border-radius: 8px !important; font-size: 13px !important; font-weight: 600 !important; }
div[data-testid="stHorizontalBlock"] { gap: 12px !important; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
initialize_tasks()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("TeamSync AI")
st.markdown("Team Collaboration Tool powered by Google Cloud & Gemini")

# Sidebar Navigation
st.sidebar.markdown("""
<div style="padding:16px 12px 12px;">
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="width:34px;height:34px;background:#4f46e5;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;color:white;font-size:14px;flex-shrink:0;">TS</div>
    <div>
      <div style="font-size:14px;font-weight:700;color:#f3f4f6;line-height:1.2;">TeamSync AI</div>
      <div style="font-size:10px;color:#6b7280;margin-top:1px;">Powered by Google Gemini</div>
    </div>
  </div>
</div>
<hr style="border:none;border-top:0.5px solid rgba(255,255,255,0.08);margin:0 12px 8px;"/>
<div style="padding:2px 16px 4px;font-size:9px;font-weight:700;color:#374151;letter-spacing:1.5px;text-transform:uppercase;">Workspace</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["Dashboard", "Task Board", "AI Standup & Priority", "Team Chat", "Meeting Notes", "Risk Analyzer"],
    label_visibility="collapsed"
)

st.sidebar.markdown("""
<hr style="border:none;border-top:0.5px solid rgba(255,255,255,0.08);margin:8px 12px;"/>
<div style="padding:2px 16px 4px;font-size:9px;font-weight:700;color:#374151;letter-spacing:1.5px;text-transform:uppercase;">AI Features</div>
""", unsafe_allow_html=True)

# push user to bottom
st.sidebar.markdown("<div style='height:200px'></div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<hr style="border:none;border-top:0.5px solid rgba(255,255,255,0.08);margin:0 12px 10px;"/>
<div style="padding:0 12px 16px;display:flex;align-items:center;gap:9px;">
  <div style="width:28px;height:28px;background:#4f46e5;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;flex-shrink:0;">S</div>
  <div>
    <div style="font-size:12px;font-weight:600;color:#d1d5db;">Sushmita</div>
    <div style="font-size:10px;color:#6b7280;">Project Lead</div>
  </div>
</div>
""", unsafe_allow_html=True)

def render_dashboard():
    tasks = get_tasks()
    total = len(tasks)
    in_progress_count = len([t for t in tasks if t['status'] == 'In Progress'])
    done_count = len([t for t in tasks if t['status'] == 'Done'])
    todo_tasks = [t for t in tasks if t['status'] == 'Todo']
    wip_tasks = [t for t in tasks if t['status'] == 'In Progress']
    done_tasks = [t for t in tasks if t['status'] == 'Done']

    # AI Insight
    if total > 0:
        task_str = "\n".join([f"- {t['title']} | {t['status']} | {t['priority']} | {t['assignee']}" for t in tasks])
        insight = call_llm(
            f"Tasks:\n{task_str}",
            "Give ONE specific actionable insight about workload, risks or priorities in under 25 words. No preamble."
        )
    else:
        insight = "Add your first task to get AI-powered project insights."

    # Risk level
    high_count = len([t for t in tasks if t.get('priority') == 'High'])
    if total == 0:
        risk_label, risk_color = "None", "#6b7280"
    elif high_count >= 3:
        risk_label, risk_color = "High &#128308;", "#dc2626"
    elif high_count >= 1:
        risk_label, risk_color = "Medium &#127937;", "#d97706"
    else:
        risk_label, risk_color = "Low &#128994;", "#16a34a"

    # --- Build all HTML parts as separate variables FIRST ---

    def make_badge(priority):
        if priority == 'High':
            return '<span style="background:#fef2f2;color:#991b1b;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">High</span>'
        elif priority == 'Medium':
            return '<span style="background:#fffbeb;color:#92400e;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">Medium</span>'
        else:
            return '<span style="background:#f0fdf4;color:#166534;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">Low</span>'

    def make_avatar(name):
        initial = name[0].upper() if name else "?"
        return (
            '<span style="display:inline-flex;align-items:center;justify-content:center;'
            'width:22px;height:22px;background:#4f46e5;border-radius:50%;'
            'color:white;font-size:10px;font-weight:700;">' + initial + '</span>'
        )

    def make_task_cards(task_list, muted=False):
        if not task_list:
            return '<div style="color:#9ca3af;font-size:12px;padding:8px 4px;">No tasks here</div>'
        parts = []
        for t in task_list:
            opacity = "opacity:0.6;" if muted else ""
            blocker = ""
            if t.get('priority') == 'High' and not muted:
                blocker = '<span style="background:#fff7ed;color:#9a3412;border:0.5px solid #fed7aa;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:600;margin-left:4px;">&#9888; Blocker</span>'
            badge_html = make_badge(t.get('priority', 'Medium'))
            avatar_html = make_avatar(t.get('assignee', '?'))
            assignee_name = t.get('assignee', 'Unassigned')
            title = t.get('title', '')
            card = (
                '<div style="background:white;border:0.5px solid #e5e7eb;border-radius:10px;'
                'padding:12px 14px;margin-bottom:8px;' + opacity + '">'
                '<div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:8px;line-height:1.4;">' + title + '</div>'
                '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">'
                + badge_html + blocker +
                '<span style="margin-left:auto;display:flex;align-items:center;gap:4px;font-size:11px;color:#6b7280;">'
                + avatar_html + ' ' + assignee_name + '</span>'
                '</div></div>'
            )
            parts.append(card)
        return "".join(parts)

    def make_workload_bars(task_list):
        if not task_list:
            return '<div style="color:#9ca3af;font-size:12px;">No assignees yet</div>'
        from collections import Counter
        workload = Counter(t.get('assignee', 'Unknown') for t in task_list)
        max_tasks = max(workload.values(), default=1)
        parts = []
        for name, count in sorted(workload.items(), key=lambda x: -x[1]):
            pct = int((count / max_tasks) * 100)
            if count >= 4:
                color, label = "#dc2626", "Overloaded"
            elif count >= 3:
                color, label = "#d97706", "Busy"
            else:
                color, label = "#16a34a", "Balanced"
            bar = (
                '<div style="margin-bottom:12px;">'
                '<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
                '<span style="font-size:12px;font-weight:500;color:#374151;">' + name + '</span>'
                '<span style="font-size:11px;font-weight:600;color:' + color + ';">' + str(count) + ' tasks &middot; ' + label + '</span>'
                '</div>'
                '<div style="background:#f3f4f6;border-radius:4px;height:6px;">'
                '<div style="background:' + color + ';height:6px;border-radius:4px;width:' + str(pct) + '%;"></div>'
                '</div></div>'
            )
            parts.append(bar)
        return "".join(parts)

    # Pre-build all section HTML
    todo_html = make_task_cards(todo_tasks)
    wip_html = make_task_cards(wip_tasks)
    done_html = make_task_cards(done_tasks, muted=True)
    workload_html = make_workload_bars(tasks)
    todo_count = str(len(todo_tasks))
    wip_count = str(len(wip_tasks))
    done_count_str = str(len(done_tasks))

    # Now build the final HTML using simple string concatenation (NO f-string for the full block)
    html = (
        '<div style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;">'

        # Header
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;padding-bottom:16px;border-bottom:0.5px solid #e5e7eb;">'
        '<div>'
        '<h2 style="font-size:22px;font-weight:700;color:#111827;margin:0;">Project Dashboard</h2>'
        '<p style="font-size:12px;color:#6b7280;margin:3px 0 0;">Real-time overview of your team workload and active risks</p>'
        '</div>'
        '<span style="background:rgba(99,102,241,0.08);color:#4f46e5;border:0.5px solid rgba(99,102,241,0.3);padding:5px 12px;border-radius:20px;font-size:11px;font-weight:700;">&#9679; AI Active</span>'
        '</div>'

        # AI Insight
        '<div style="background:rgba(99,102,241,0.06);border:0.5px solid rgba(99,102,241,0.22);border-radius:10px;padding:12px 16px;margin-bottom:20px;display:flex;align-items:flex-start;gap:12px;">'
        '<div style="width:28px;height:28px;background:rgba(99,102,241,0.15);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">&#10022;</div>'
        '<div style="font-size:12px;color:#374151;line-height:1.6;"><strong style="color:#4f46e5;">AI Insight:</strong> ' + insight + '</div>'
        '</div>'

        # Metrics
        '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px;">'
        '<div style="background:white;border:0.5px solid #e5e7eb;border-radius:10px;padding:16px 18px;">'
        '<div style="font-size:10px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:8px;">Total Tasks</div>'
        '<div style="font-size:28px;font-weight:700;color:#111827;">' + str(total) + '</div></div>'

        '<div style="background:white;border:0.5px solid #e5e7eb;border-radius:10px;padding:16px 18px;">'
        '<div style="font-size:10px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:8px;">In Progress</div>'
        '<div style="font-size:28px;font-weight:700;color:#d97706;">' + str(in_progress_count) + '</div></div>'

        '<div style="background:white;border:0.5px solid #e5e7eb;border-radius:10px;padding:16px 18px;">'
        '<div style="font-size:10px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:8px;">Completed</div>'
        '<div style="font-size:28px;font-weight:700;color:#16a34a;">' + str(done_count) + '</div></div>'

        '<div style="background:white;border:0.5px solid #e5e7eb;border-radius:10px;padding:16px 18px;">'
        '<div style="font-size:10px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:8px;">AI Risk Score</div>'
        '<div style="font-size:28px;font-weight:700;color:' + risk_color + ';">' + risk_label + '</div></div>'
        '</div>'

        # Kanban
        '<div style="font-size:14px;font-weight:700;color:#111827;margin-bottom:12px;">Kanban Board</div>'
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px;">'

        '<div style="background:#f9fafb;border-radius:10px;padding:12px;">'
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">'
        '<div style="display:flex;align-items:center;gap:6px;">'
        '<span style="width:8px;height:8px;background:#6b7280;border-radius:50%;display:inline-block;"></span>'
        '<span style="font-size:11px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;">To Do</span>'
        '</div>'
        '<span style="font-size:10px;background:white;color:#6b7280;padding:1px 7px;border-radius:8px;border:0.5px solid #e5e7eb;">' + todo_count + '</span>'
        '</div>' + todo_html + '</div>'

        '<div style="background:#f9fafb;border-radius:10px;padding:12px;">'
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">'
        '<div style="display:flex;align-items:center;gap:6px;">'
        '<span style="width:8px;height:8px;background:#f59e0b;border-radius:50%;display:inline-block;"></span>'
        '<span style="font-size:11px;font-weight:700;color:#92400e;text-transform:uppercase;letter-spacing:0.5px;">In Progress</span>'
        '</div>'
        '<span style="font-size:10px;background:white;color:#6b7280;padding:1px 7px;border-radius:8px;border:0.5px solid #e5e7eb;">' + wip_count + '</span>'
        '</div>' + wip_html + '</div>'
        '<div style="background:#f9fafb;border-radius:10px;padding:12px;">'
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">'
        '<div style="display:flex;align-items:center;gap:6px;">'
        '<span style="width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;"></span>'
        '<span style="font-size:11px;font-weight:700;color:#166534;text-transform:uppercase;letter-spacing:0.5px;">Done</span>'
        '</div>'
        '<span style="font-size:10px;background:white;color:#6b7280;padding:1px 7px;border-radius:8px;border:0.5px solid #e5e7eb;">' + done_count_str + '</span>'
        '</div>' + done_html + '</div>'
        '</div>'

        # Workload
        '<div style="background:white;border:0.5px solid #e5e7eb;border-radius:10px;padding:16px 18px;margin-bottom:16px;">'
        '<div style="font-size:13px;font-weight:700;color:#111827;margin-bottom:14px;">Team Workload</div>'
        + workload_html +
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

if page == "Dashboard":
    render_dashboard()

elif page == "Task Board":
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("## Task Board")
        st.caption("Manage your team's tasks and priorities")
    with col2:
        st.markdown("<div style='text-align:right;padding-top:8px;'><span style='background:rgba(99,102,241,0.1);color:#6366f1;border:0.5px solid rgba(99,102,241,0.25);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;'>● AI Active</span></div>", unsafe_allow_html=True)
    st.divider()
    
    # Task Creation Form
    with st.expander("➕ Create New Task", expanded=False):
        title = st.text_input("Task Title", key="task_title_input")
        
        if st.button("✦ Auto-generate description"):
            if title:
                with st.spinner("Generating..."):
                    st.session_state["task_desc_input"] = generate_task_description(title)
                    st.session_state["desc_is_ai"] = True
            else:
                st.warning("Please enter a Task Title first.")
                
        desc_val = st.session_state.get("task_desc_input", "")
        description = st.text_area("Description", value=desc_val, key="task_desc_input")
        
        if st.session_state.get("desc_is_ai", False):
            st.caption("✦ AI-generated — edit as needed")
            
        assignee = st.text_input("Assignee", key="task_assignee_input")
        col1, col2 = st.columns(2)
        with col1:
            status = st.selectbox("Initial Status", ["Todo", "In Progress", "Done"], key="task_status_input")
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High"], key="task_priority_input")
            
        if st.button("Add Task", type="primary"):
            if title and assignee:
                add_task(title, description, assignee, status, priority)
                st.success("Task added successfully!")
                # Reset inputs by clearing keys
                for key in ["task_title_input", "task_desc_input", "task_assignee_input", "desc_is_ai"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            else:
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

elif page == "AI Standup & Priority":
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("## AI Team Insights")
        st.caption("Generate daily standups and get smart task prioritization")
    with col2:
        st.markdown("<div style='text-align:right;padding-top:8px;'><span style='background:rgba(99,102,241,0.1);color:#6366f1;border:0.5px solid rgba(99,102,241,0.25);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;'>● AI Active</span></div>", unsafe_allow_html=True)
    st.divider()
    tasks = get_tasks()
    
    tab1, tab2 = st.tabs(["Daily Standup", "Smart Prioritization"])
    
    with tab1:
        st.markdown("Generate a daily standup summary based on current tasks.")
        if st.button("Generate Standup Summary", type="primary"):
            if tasks:
                with st.spinner("AI is analyzing the board..."):
                    summary = generate_daily_standup(tasks)
                st.markdown("### Standup Report")
                st.write(summary)
            else:
                st.warning("Add some tasks to the board first!")
                
    with tab2:
        st.markdown("Ask the AI to review current tasks and suggest priority adjustments.")
        if st.button("Suggest Priorities", type="primary"):
            if tasks:
                with st.spinner("AI is evaluating priorities..."):
                    suggestions = prioritize_tasks(tasks)
                st.markdown("### AI Priority Suggestions")
                st.write(suggestions)
            else:
                st.warning("Add some tasks to the board first!")

elif page == "Team Chat":
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("## TeamSync Assistant")
        st.caption("Ask questions about the project, tasks, or team status")
    with col2:
        st.markdown("<div style='text-align:right;padding-top:8px;'><span style='background:rgba(99,102,241,0.1);color:#6366f1;border:0.5px solid rgba(99,102,241,0.25);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;'>● AI Active</span></div>", unsafe_allow_html=True)
    st.divider()
    
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

elif page == "Meeting Notes":
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("## Meeting Notes Summarizer")
        st.caption("Paste your meeting transcript below to generate a concise summary and action items")
    with col2:
        st.markdown("<div style='text-align:right;padding-top:8px;'><span style='background:rgba(99,102,241,0.1);color:#6366f1;border:0.5px solid rgba(99,102,241,0.25);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;'>● AI Active</span></div>", unsafe_allow_html=True)
    st.divider()
    
    transcript = st.text_area("Meeting Transcript", height=300, placeholder="Paste transcript here...")
    
    if st.button("✨ Summarize", type="primary"):
        if transcript:
            with st.spinner("AI is summarizing the meeting..."):
                summary = summarize_meeting_notes(transcript)
            st.markdown("### Meeting Summary")
            st.write(summary)
        else:
            st.warning("Please paste a transcript first!")

elif page == "Risk Analyzer":
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("## Risk Analyzer")
        st.caption("Analyze task workloads and identify project risks proactively")
    with col2:
        st.markdown("<div style='text-align:right;padding-top:8px;'><span style='background:rgba(99,102,241,0.1);color:#6366f1;border:0.5px solid rgba(99,102,241,0.25);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;'>● AI Active</span></div>", unsafe_allow_html=True)
    st.divider()
    tasks = get_tasks()
    
    if not tasks:
        st.info("No tasks available to analyze.")
    else:
        with st.spinner("Compiling risk report and metrics..."):
            metrics = get_risk_metrics(tasks)
            report = generate_risk_report(tasks)
            
        st.markdown("### Risk Metrics")
        m1, m2, m3 = st.columns(3)
        m1.metric("Tasks at Risk", metrics["at_risk"])
        m2.metric("Overloaded Team Members", metrics["overloaded"])
        m3.metric("Suggested Priority Changes", metrics["priority_changes"])
        
        st.markdown("<hr style='border:0.5px solid rgba(128,128,128,0.2);margin:16px 0;'/>", unsafe_allow_html=True)
        st.markdown("### Executive Risk Report")
        st.markdown(report)
        
        st.download_button(
            label="Download Risk Report (.txt)",
            data=report,
            file_name="project_risk_report.txt",
            mime="text/plain"
        )
