import streamlit as st
import random
import numpy as np

# Updated JOB_TOOLS with proper skill overlaps between related roles
# Added missing roles: AI Engineer, AI Researcher, System Administrator, Research Scientist, Web Designer
JOB_TOOLS = {
    # Data & Analytics cluster
    "Data Analyst": ["SQL", "Excel", "Data visualization", "Statistical analysis", "Data cleaning"],
    "Data Scientist": ["Python", "SQL", "Statistical analysis", "Machine learning", "Data visualization"],
    "Data Engineer": ["SQL", "Python", "ETL processes", "Database design", "Data pipelines"],
    "Business Analyst": ["Excel", "SQL", "Data visualization", "Business requirements", "Process analysis"],
    "Machine Learning Engineer": ["Python", "Machine learning", "SQL", "Model deployment", "Deep learning"],
    "Business Intelligence Analyst": ["SQL", "Data visualization", "Excel", "Dashboard creation", "Data modeling"],
    "AI Engineer": ["Python", "Machine learning", "Deep learning", "Algorithm development", "Neural networks"],
    "AI Researcher": ["Python", "Deep learning", "Research methods", "Scientific writing", "Neural networks"],
    "Research Scientist": ["Python", "Research methods", "Statistical analysis", "Scientific writing", "Experimental design"],
    
    # Software Development cluster
    "Software Engineer": ["Programming languages", "Git", "Software design", "Testing", "Algorithms"],
    "Frontend Developer": ["JavaScript", "HTML/CSS", "Git", "React/Angular/Vue", "UI/UX principles"],
    "Backend Developer": ["Programming languages", "SQL/NoSQL", "API design", "Git", "Server management"],
    "Full Stack Developer": ["JavaScript", "HTML/CSS", "Programming languages", "SQL/NoSQL", "Git"],
    "DevOps Engineer": ["CI/CD pipelines", "Cloud platforms", "Infrastructure as code", "Containerization", "Monitoring"],
    "Cloud Engineer": ["Cloud platforms", "Infrastructure as code", "Networking", "Security", "Containerization"],
    "Site Reliability Engineer": ["Monitoring", "Automation", "Infrastructure as code", "Incident response", "Cloud platforms"],
    "Mobile Developer": ["Mobile frameworks", "Programming languages", "Git", "API integration", "UI design"],
    "System Administrator": ["Server management", "Networking", "Security", "Automation", "Troubleshooting"],
    
    # Design cluster
    "UX Designer": ["User research", "Wireframing", "Prototyping", "Design tools", "Information architecture"],
    "UI Designer": ["Visual design", "Design tools", "Prototyping", "Typography", "Color theory"],
    "Graphic Designer": ["Design tools", "Visual composition", "Typography", "Color theory", "Brand identity"],
    "Product Designer": ["Design tools", "User research", "Prototyping", "Visual design", "User flows"],
    "Visual Designer": ["Design tools", "Color theory", "Typography", "Visual composition", "Brand identity"],
    "Interaction Designer": ["Prototyping", "Design tools", "Motion design", "User flows", "Wireframing"],
    "Web Designer": ["HTML/CSS", "Design tools", "Responsive design", "Typography", "UI principles"],
    
    # Product & Project Management cluster
    "Product Manager": ["Product strategy", "User stories", "Stakeholder management", "Market analysis", "Roadmapping"],
    "Project Manager": ["Project planning", "Stakeholder management", "Risk management", "Agile methodologies", "Resource allocation"],
    "Program Manager": ["Portfolio management", "Stakeholder management", "Strategic planning", "Risk management", "Resource allocation"],
    "Scrum Master": ["Agile methodologies", "Team facilitation", "Sprint planning", "Impediment removal", "Stakeholder management"],
    "Product Owner": ["User stories", "Product backlog", "Stakeholder management", "Prioritization", "Product strategy"],
    
    # Marketing & Content cluster
    "Marketing Manager": ["Marketing strategy", "Analytics", "Campaign management", "Brand development", "Customer insights"],
    "Content Writer": ["Content creation", "SEO principles", "Research", "Editing", "Brand voice"],
    "SEO Specialist": ["SEO principles", "Analytics", "Content optimization", "Keyword research", "Technical SEO"],
    "Social Media Manager": ["Content creation", "Social media platforms", "Analytics", "Community management", "Campaign planning"],
    "Content Strategist": ["Content planning", "SEO principles", "Analytics", "Brand voice", "Audience research"],
    "Digital Marketing Specialist": ["Analytics", "SEO principles", "Campaign management", "Social media platforms", "Email marketing"]
}

# Updated classification function: 0-1 skills = easy, 2 skills = moderate, 3+ skills = challenging
def classify_transition(num_skills_to_develop):
    if num_skills_to_develop <= 1:
        return "Easy Transition", "#22C55E"  # Green
    elif num_skills_to_develop == 2:
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
            "Business Intelligence Analyst",
            "AI Engineer",
            "AI Researcher",
            "Research Scientist"
        ],
        "Software Development": [
            "Software Engineer", 
            "Frontend Developer", 
            "Backend Developer", 
            "Full Stack Developer", 
            "DevOps Engineer",
            "Mobile Developer",
            "System Administrator",
            "Cloud Engineer",
            "Site Reliability Engineer"
        ],
        "Design": [
            "UX Designer", 
            "UI Designer", 
            "Graphic Designer", 
            "Product Designer",
            "Visual Designer",
            "Interaction Designer",
            "Web Designer"
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
