import streamlit as st
from skills_hub_components.course_recommendations import display_course_recommendations
from skills_hub_components.skill_gap_analysis import display_skill_gap_analysis
from skills_hub_components.career_timeline import display_career_timeline
from skills_hub_components.career_path_map import display_career_path_map

def run():
    # Enhanced header with gradient background
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                padding:16px; border-radius:10px; margin-bottom:20px;">
        <div style="display:flex; align-items:center;">
            <span style="font-size:24px; margin-right:12px;">🧠</span>
            <div>
                <h1 style="color:white; margin:0; font-size:24px; font-weight:600;">Skills & Learning Hub</h1>
                <p style="color:#94A3B8; margin:4px 0 0 0; font-size:14px;">Develop the skills you need for your next career move</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Courses", "📊 Skill Gap Analysis", "⏳ Career Timeline", "🗺️ Career Path Map"])
    
    with tab1:
        display_course_recommendations()
    
    with tab2:
        display_skill_gap_analysis()
    
    with tab3:
        display_career_timeline()
    
    with tab4:
        display_career_path_map()
    
    # Footer
    st.markdown("""
    <div style="background-color:rgba(15, 23, 42, 0.3); padding:8px; border-radius:6px; margin-top:30px; text-align:center;">
        <p style="color:#64748B; font-size:11px; margin:0;">© 2025 FuturePaths | Career Guidance Platform</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
