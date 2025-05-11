import streamlit as st
import random
import numpy as np

# Required tools/software by role (from your salary page)
JOB_TOOLS = {
    "Data Analyst": ["Excel", "SQL", "Tableau/Power BI", "Python/R"],
    "Data Scientist": ["Python", "R", "SQL", "TensorFlow/PyTorch", "Jupyter"],
    "UX Designer": ["Figma", "Sketch", "Adobe XD", "InVision", "Zeplin"],
    "Marketing Manager": ["Google Analytics", "HubSpot", "SEO tools", "Social media platforms"],
    "Product Manager": ["Jira", "Confluence", "Figma", "Google Analytics"],
    "Software Engineer": ["Git", "Docker", "CI/CD tools", "Cloud platforms"],
    "Frontend Developer": ["HTML/CSS", "JavaScript", "React/Angular/Vue", "Git"],
    "Backend Developer": ["Node.js/Python/Java", "SQL/NoSQL", "API tools", "Docker"],
    "Full Stack Developer": ["JavaScript", "HTML/CSS", "Backend languages", "Databases", "Git"],
    "DevOps Engineer": ["Docker", "Kubernetes", "AWS/Azure/GCP", "CI/CD pipelines", "Terraform"],
    "Machine Learning Engineer": ["Python", "TensorFlow/PyTorch", "Scikit-learn", "Jupyter", "Git"],
    "Business Analyst": ["Excel", "SQL", "Tableau/Power BI", "Jira"],
    "Project Manager": ["MS Project", "Jira", "Asana", "Slack", "Confluence"],
    "Content Writer": ["CMS platforms", "SEO tools", "Grammarly", "Google Analytics"],
    "Graphic Designer": ["Adobe Creative Suite", "Figma", "Sketch", "Canva"],
}

def classify_transition(num_skills_to_develop):
    if num_skills_to_develop == 0:
        return "Easy Transition", "#22C55E"  # Green
    elif num_skills_to_develop == 1:
        return "Moderate Transition", "#F59E0B"  # Orange
    else:
        return "Challenging Transition", "#EF4444"  # Red

def display_career_path_map():
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                padding:16px; border-radius:10px; margin:20px 0 15px 0; 
                display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <span style="font-size:24px; margin-right:10px;">🗺️</span>
        <h3 style="color:white; margin:0; font-weight:600;">Career Path Map</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#94A3B8; margin-bottom:20px;">
        Explore potential career transitions and discover roles that match your skills.
    </p>
    """, unsafe_allow_html=True)
    
    # Career clusters with related roles
    CAREER_CLUSTERS = {
        "Data & Analytics": [
            "Data Analyst", 
            "Data Scientist", 
            "Business Analyst", 
            "Data Engineer", 
            "Machine Learning Engineer",
            "Business Intelligence Analyst"
        ],
        "Software Development": [
            "Software Engineer", 
            "Frontend Developer", 
            "Backend Developer", 
            "Full Stack Developer", 
            "DevOps Engineer",
            "Mobile Developer"
        ],
        "Design": [
            "UX Designer", 
            "UI Designer", 
            "Graphic Designer", 
            "Product Designer",
            "Visual Designer",
            "Interaction Designer"
        ],
        "Product & Project Management": [
            "Product Manager", 
            "Project Manager", 
            "Program Manager", 
            "Scrum Master",
            "Product Owner",
            "Business Analyst"
        ],
        "Marketing & Content": [
            "Marketing Manager", 
            "Content Writer", 
            "SEO Specialist", 
            "Social Media Manager",
            "Content Strategist",
            "Digital Marketing Specialist"
        ]
    }
    
    # Career transitions - showing which roles commonly transition to others
    CAREER_TRANSITIONS = {
        "Data Analyst": ["Data Scientist", "Business Analyst", "Data Engineer", "Business Intelligence Analyst"],
        "Data Scientist": ["Machine Learning Engineer", "Data Engineer", "AI Researcher", "Data Analyst"],
        "Business Analyst": ["Product Manager", "Data Analyst", "Project Manager", "Business Intelligence Analyst"],
        "Software Engineer": ["DevOps Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer"],
        "Frontend Developer": ["Full Stack Developer", "UX Designer", "UI Designer", "Software Engineer"],
        "Backend Developer": ["Full Stack Developer", "DevOps Engineer", "Software Engineer", "Data Engineer"],
        "UX Designer": ["Product Designer", "UI Designer", "Product Manager", "Frontend Developer"],
        "Product Manager": ["Program Manager", "UX Designer", "Marketing Manager", "Business Analyst"],
        "Marketing Manager": ["Product Manager", "Content Strategist", "Digital Marketing Specialist", "Social Media Manager"],
        "Content Writer": ["Content Strategist", "SEO Specialist", "Social Media Manager", "Marketing Manager"]
    }
    
    # Add generic transitions for other roles
    for job_title in ["Full Stack Developer", "DevOps Engineer", "Machine Learning Engineer", "Project Manager", "Graphic Designer"]:
        if job_title not in CAREER_TRANSITIONS:
            if job_title == "Full Stack Developer":
                CAREER_TRANSITIONS[job_title] = ["Frontend Developer", "Backend Developer", "Software Engineer", "DevOps Engineer"]
            elif job_title == "DevOps Engineer":
                CAREER_TRANSITIONS[job_title] = ["Site Reliability Engineer", "Cloud Engineer", "Backend Developer", "System Administrator"]
            elif job_title == "Machine Learning Engineer":
                CAREER_TRANSITIONS[job_title] = ["Data Scientist", "AI Engineer", "Software Engineer", "Research Scientist"]
            elif job_title == "Project Manager":
                CAREER_TRANSITIONS[job_title] = ["Program Manager", "Product Manager", "Scrum Master", "Business Analyst"]
            elif job_title == "Graphic Designer":
                CAREER_TRANSITIONS[job_title] = ["UI Designer", "UX Designer", "Visual Designer", "Web Designer"]
    
    # Cluster selection
    cluster = st.selectbox(
        "Select a career cluster:",
        sorted(list(CAREER_CLUSTERS.keys())),
        key="career_cluster"
    )
    
    if cluster:
        roles = CAREER_CLUSTERS.get(cluster, [])
        
        if roles:
            st.markdown(f"""
            <div style="background-color:rgba(59, 130, 246, 0.1); padding:12px; border-radius:8px; 
                        margin:16px 0; border-left:3px solid #3B82F6;">
                <div style="display:flex; align-items:center;">
                    <span style="font-size:18px; margin-right:10px;">🔍</span>
                    <p style="color:white; margin:0; font-size:14px;">
                        Explore potential career transitions within the <strong>{cluster}</strong> cluster
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Role selection
            selected_role = st.selectbox(
                "Choose your current role:",
                sorted(roles),
                key="selected_role"
            )
            
            if selected_role:
                transitions = CAREER_TRANSITIONS.get(selected_role, [])
                
                if transitions:
                    # Get up to 3 transitions
                    display_transitions = transitions[:3]
                    
                    # Calculate skill overlaps and skills to develop
                    common_skills_list = []
                    skills_to_develop_list = []
                    
                    for transition in display_transitions:
                        # Get skills for both roles
                        current_skills = JOB_TOOLS.get(selected_role, [])
                        transition_skills = JOB_TOOLS.get(transition, [])
                        
                        # Find common skills
                        common_skills = []
                        for skill in current_skills:
                            skill_name = skill.split('/')[0] if '/' in skill else skill
                            for t_skill in transition_skills:
                                t_skill_name = t_skill.split('/')[0] if '/' in t_skill else t_skill
                                if skill_name == t_skill_name or skill_name in t_skill or t_skill_name in skill:
                                    common_skills.append(skill)
                                    break
                        
                        # If no common skills found, create some mock ones
                        if not common_skills:
                            if "Developer" in selected_role and "Developer" in transition:
                                common_skills = ["Programming fundamentals", "Git", "Problem-solving"]
                            elif "Data" in selected_role and "Data" in transition:
                                common_skills = ["SQL", "Data analysis", "Statistics"]
                            elif "Designer" in selected_role and "Designer" in transition:
                                common_skills = ["Design principles", "User-centered design", "Visual communication"]
                            else:
                                common_skills = ["Communication", "Project management", "Industry knowledge"]
                        
                        common_skills_list.append(common_skills[:3])  # Limit to 3 skills for display
                        
                        # Find skills to develop
                        skills_to_develop = []
                        for skill in transition_skills:
                            is_common = False
                            skill_name = skill.split('/')[0] if '/' in skill else skill
                            
                            for common in common_skills:
                                common_name = common.split('/')[0] if '/' in common else common
                                if skill_name == common_name or skill_name in common or common_name in skill:
                                    is_common = True
                                    break
                            
                            if not is_common:
                                skills_to_develop.append(skill)
                        
                        skills_to_develop_list.append(skills_to_develop[:3])  # Limit to 3 skills for display
                    
                    # Display the current role in a centered box
                    st.markdown(f"""
                    <div style="display:flex; justify-content:center; margin:30px 0;">
                        <div style="background-color:#3B82F6; color:white; padding:15px 25px; 
                                    border-radius:10px; text-align:center; font-weight:600; 
                                    box-shadow:0 4px 6px rgba(0,0,0,0.1); min-width:180px;">
                            {selected_role}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create columns for the transitions
                    cols = st.columns(len(display_transitions))
                    
                    # Display each transition in its own column
                    for i, (col, transition, common_skills, skills_to_develop) in enumerate(zip(cols, display_transitions, common_skills_list, skills_to_develop_list)):
                        # Classify transition based on number of skills to develop
                        transition_type, color = classify_transition(len(skills_to_develop))
                        
                        with col:
                            # Transition box
                            st.markdown(f"""
                            <div style="background-color:{color}; color:white; padding:12px 20px; 
                                        border-radius:8px; text-align:center; font-weight:500; 
                                        box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:15px; position:relative;">
                                {transition}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Transition difficulty
                            st.markdown(f"""
                            <div style="background-color:#1E293B; padding:12px; border-radius:8px; 
                                        border:1px solid rgba(255,255,255,0.05); margin-bottom:10px;">
                                <div style="display:flex; align-items:center; margin-bottom:5px;">
                                    <div style="width:12px; height:12px; background-color:{color}; 
                                                border-radius:50%; margin-right:8px;"></div>
                                    <span style="color:white; font-weight:500; font-size:14px;">{transition_type}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Common skills
                            st.markdown("""
                            <div style="background-color:#1E293B; padding:12px; border-radius:8px; 
                                        border:1px solid rgba(255,255,255,0.05); margin-bottom:10px;">
                                <p style="color:#94A3B8; font-size:14px; margin:0 0 8px 0;">Common Skills:</p>
                            """, unsafe_allow_html=True)
                            
                            for skill in common_skills:
                                st.markdown(f"""
                                <div style="background-color:rgba(59, 130, 246, 0.1); padding:6px 10px; 
                                            border-radius:6px; border:1px solid rgba(59, 130, 246, 0.3);
                                            margin-bottom:5px;">
                                    <span style="color:white; font-size:13px;">{skill}</span>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            # Skills to develop
                            if skills_to_develop:
                                st.markdown("""
                                <div style="background-color:#1E293B; padding:12px; border-radius:8px; 
                                            border:1px solid rgba(255,255,255,0.05); margin-bottom:10px;">
                                    <p style="color:#94A3B8; font-size:14px; margin:0 0 8px 0;">Skills to Develop:</p>
                                """, unsafe_allow_html=True)
                                
                                for skill in skills_to_develop:
                                    st.markdown(f"""
                                    <div style="background-color:rgba(251, 113, 133, 0.1); padding:6px 10px; 
                                                border-radius:6px; border:1px solid rgba(251, 113, 133, 0.3);
                                                margin-bottom:5px;">
                                        <span style="color:white; font-size:13px;">{skill}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info(f"No common transitions defined for {selected_role}. Try another role.")
        else:
            st.info(f"No roles defined for the {cluster} cluster. Try another cluster.")
