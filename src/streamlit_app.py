import streamlit as st

# Add custom CSS for an enhanced sidebar
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        padding: 2rem 1rem;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] .css-1vq4p4l h1 {
        color: white;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Navigation options */
    [data-testid="stSidebar"] .stRadio > div {
        margin-top: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #94A3B8 !important;
        font-size: 15px;
        padding: 0.5rem 0.8rem;
        border-radius: 6px;
        transition: all 0.2s ease;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + div + label {
        color: white !important;
        font-weight: 600;
        background-color: #1E3A8A;
    }
    
    /* Hover effect for navigation items */
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(30, 58, 138, 0.5);
        color: white !important;
    }
    
    /* Logo styling */
    .sidebar-logo {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    /* Footer styling */
    .sidebar-footer {
        position: absolute;
        bottom: 20px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 12px;
        color: #64748B;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Update your streamlit_app.py file
import career_pivot_page
import internships_salary_page
import skills_learning_hub

# Create a more visually appealing sidebar
with st.sidebar:
    # Logo and app name
    st.markdown("""
    <div class="sidebar-logo">
        <span style="font-size:28px; margin-right:10px;">🚀</span>
        <span style="color:white; font-size:22px; font-weight:600;">FuturePaths</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color:#94A3B8; font-size:14px; margin-bottom:20px; font-weight:400;'>Career Guidance Platform</h3>", unsafe_allow_html=True)
    
    # Navigation with icons
    st.markdown("### Navigation")
    
    PAGES = {
        "🔄 Career Pivot Suggestions": career_pivot_page,
        "💰 Internships & Salary Insights": internships_salary_page,
        "🧠 Skills & Learning Hub": skills_learning_hub,
    }
    
    selection = st.radio("", list(PAGES.keys()), label_visibility="collapsed")
    
    # Additional sidebar content
    st.markdown("<hr style='margin:2rem 0; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    # User profile section (mock)
    st.markdown("""
    <div style="background-color:#1E293B; padding:15px; border-radius:8px; margin-top:20px;">
        <div style="display:flex; align-items:center; margin-bottom:10px;">
            <div style="width:40px; height:40px; border-radius:50%; background-color:#3B82F6; display:flex; justify-content:center; align-items:center; margin-right:10px;">
                <span style="color:white; font-weight:bold;">U</span>
            </div>
            <div>
                <p style="color:white; margin:0; font-weight:500;">User Profile</p>
                <p style="color:#94A3B8; margin:0; font-size:12px;">Student</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="sidebar-footer">
        <p>© 2025 FuturePaths</p>
        <p style="margin-top:5px;">Advanced Topics in ML</p>
    </div>
    """, unsafe_allow_html=True)

# Display the selected page
page = PAGES[selection]
page.run()
