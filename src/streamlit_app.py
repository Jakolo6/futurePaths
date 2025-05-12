import streamlit as st

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title="FuturePaths", page_icon="🚀", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] {
    background-color: #0F172A;
    padding: 2rem 1rem;
    border-right: 1px solid rgba(255,255,255,0.05);
    display: flex;
    flex-direction: column;
    height: 100vh;              /* fill full height so footer can stick */
  }
  .sidebar-logo {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  .sidebar-logo span:last-child {
    color: white;
    font-size: 22px;
    font-weight: 600;
  }
  .nav-button {
    width: 100%;
    background-color: transparent;
    color: #94A3B8;
    border: none;
    text-align: left;
    padding: 0.6rem 0.8rem;
    margin-bottom: 0.3rem;
    border-radius: 6px;
    font-size: 15px;
    transition: background-color 0.2s, color 0.2s;
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  .nav-button:hover {
    background-color: rgba(30,58,138,0.5);
    color: white !important;
  }
  .nav-button.selected {
    background-color: #1E3A8A;
    color: white !important;
    font-weight: 600;
  }
  .sidebar-footer {
    margin-top: auto;           /* push footer to bottom */
    text-align: center;
    font-size: 12px;
    color: #64748B;
    padding-top: 1rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Page modules ──────────────────────────────────────────────────────────────
import career_pivot_page
import internships_salary_page
import skills_learning_hub
import resume_upload_and_predict_page

# ── Pages dictionary ─────────────────────────────────────────────────────────
PAGES = {
    "Career Pivot Suggestions": ("🔄", career_pivot_page),
    "Resume Analysis & Pathfinding": ("📄", resume_upload_and_predict_page),
    "Internships & Salary Insights": ("💰", internships_salary_page),
    "Skills & Learning Hub": ("🧠", skills_learning_hub),
}

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo + title
    st.markdown(
      '<div class="sidebar-logo">'
      '  <span style="font-size:28px; margin-right:8px;">🚀</span>'
      '  <span>FuturePaths</span>'
      '</div>',
      unsafe_allow_html=True
    )
    st.markdown(
      "<p style='color:#94A3B8; margin-bottom:1rem;'>Career Guidance Platform</p>",
      unsafe_allow_html=True
    )

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = list(PAGES.keys())[0]

    # Render buttons
    for idx, (name, (icon, module)) in enumerate(PAGES.items()):
        selected = (st.session_state.page == name)
        label = f"{icon}  {name}"
        if st.button(label, key=name):
            st.session_state.page = name
        extra = " selected" if selected else ""
        # Apply the CSS class to the correct button
        st.write(
          f"<script>"
          f"document.querySelectorAll('.stButton button')[{idx}].className = 'nav-button{extra}';"
          f"</script>",
          unsafe_allow_html=True
        )

    # Footer
    st.markdown(
      "<div class='sidebar-footer'>© 2025 FuturePaths<br>Advanced Topics in ML</div>",
      unsafe_allow_html=True
    )

# ── Main content ─────────────────────────────────────────────────────────────
page_module = PAGES[st.session_state.page][1]
if hasattr(page_module, "run") and callable(page_module.run):
    page_module.run()
else:
    st.error(f"Page '{st.session_state.page}' has no run() function.")
