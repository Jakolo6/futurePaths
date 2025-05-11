import streamlit as st
import numpy as np
import random

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
        Explore common career transitions and discover adjacent roles that match your skills.
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
                        Explore roles and transitions within the <strong>{cluster}</strong> cluster
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display roles in this cluster
            st.markdown("""
            <p style="color:white; margin:20px 0 15px 0; font-size:16px; font-weight:500;">Select a role to see common career transitions:</p>
            """, unsafe_allow_html=True)
            
            # Role selection
            selected_role = st.selectbox(
                "Choose a role:",
                sorted(roles),
                key="selected_role"
            )
            
            if selected_role:
                transitions = CAREER_TRANSITIONS.get(selected_role, [])
                
                if transitions:
                    st.markdown(f"""
                    <div style="margin-top:30px;">
                        <h3 style="color:white; margin:0 0 20px 0; font-size:18px; font-weight:600;">Common transitions from {selected_role}:</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a visual representation of transitions
                    st.markdown("""
                    <div style="position:relative; height:400px; margin:20px 0;">
                    """, unsafe_allow_html=True)
                    
                    # Central role
                    st.markdown(f"""
                    <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%);
                                width:150px; height:150px; background-color:#3B82F6; border-radius:50%;
                                display:flex; justify-content:center; align-items:center; z-index:2;
                                box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);">
                        <div style="text-align:center; padding:10px;">
                            <p style="color:white; font-weight:600; font-size:16px; margin:0;">{selected_role}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Transition roles
                    angles = [i * (360 / len(transitions)) for i in range(len(transitions))]
                    radius = 180  # Distance from center
                    
                    for i, (transition, angle) in enumerate(zip(transitions, angles)):
                        # Convert angle to radians and calculate position
                        angle_rad = np.radians(angle)
                        x = 50 + radius * np.cos(angle_rad)  # 50% is center
                        y = 50 + radius * np.sin(angle_rad)  # 50% is center
                        
                        # Determine if this role is in the same cluster
                        is_same_cluster = any(transition in cluster_roles for cluster_name, cluster_roles in CAREER_CLUSTERS.items() if selected_role in cluster_roles)
                        bg_color = "#8B5CF6" if is_same_cluster else "#22C55E"
                        
                        # Draw connecting line
                        line_x1 = 50  # Center x
                        line_y1 = 50  # Center y
                        line_x2 = x
                        line_y2 = y
                        
                        # Calculate points for the line to connect to the circles
                        central_radius = 75  # Half of central circle width
                        outer_radius = 50   # Half of outer circle width
                        
                        # Adjust line start and end points to connect to the circle edges
                        line_length = np.sqrt((line_x2 - line_x1)**2 + (line_y2 - line_y1)**2)
                        line_x1_adj = line_x1 + (line_x2 - line_x1) * central_radius / line_length
                        line_y1_adj = line_y1 + (line_y2 - line_y1) * central_radius / line_length
                        line_x2_adj = line_x2 - (line_x2 - line_x1) * outer_radius / line_length
                        line_y2_adj = line_y2 - (line_y2 - line_y1) * outer_radius / line_length
                        
                        st.markdown(f"""
                        <div style="position:absolute; top:{y}%; left:{x}%; transform:translate(-50%, -50%);
                                    width:100px; height:100px; background-color:{bg_color}; border-radius:50%;
                                    display:flex; justify-content:center; align-items:center; z-index:1;
                                    box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);">
                            <div style="text-align:center; padding:10px;">
                                <p style="color:white; font-weight:500; font-size:14px; margin:0;">{transition}</p>
                            </div>
                        </div>
                        
                        <svg style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:0;">
                            <line x1="{line_x1_adj}%" y1="{line_y1_adj}%" x2="{line_x2_adj}%" y2="{line_y2_adj}%" 
                                  style="stroke:rgba(255,255,255,0.3); stroke-width:2;" />
                        </svg>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Legend
                    st.markdown("""
                    <div style="display:flex; justify-content:center; gap:30px; margin-top:20px;">
                        <div style="display:flex; align-items:center;">
                            <div style="width:15px; height:15px; background-color:#8B5CF6; border-radius:50%; margin-right:8px;"></div>
                            <span style="color:white; font-size:14px;">Same cluster</span>
                        </div>
                        <div style="display:flex; align-items:center;">
                            <div style="width:15px; height:15px; background-color:#22C55E; border-radius:50%; margin-right:8px;"></div>
                            <span style="color:white; font-size:14px;">Different cluster</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Skill overlap information
                    st.markdown("""
                    <div style="margin-top:40px;">
                        <h3 style="color:white; margin:0 0 20px 0; font-size:18px; font-weight:600;">Skill overlap with adjacent roles:</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display skill overlap cards
                    st.markdown("""
                    <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:20px;">
                    """, unsafe_allow_html=True)
                    
                    for transition in transitions:
                        # Calculate mock skill overlap percentage
                        overlap = random.randint(60, 90)
                        
                        # Determine overlap color
                        if overlap >= 80:
                            overlap_color = "#22C55E"  # Green for high overlap
                        elif overlap >= 70:
                            overlap_color = "#F59E0B"  # Amber for medium overlap
                        else:
                            overlap_color = "#3B82F6"  # Blue for lower overlap
                        
                        # Get common skills
                        current_skills = JOB_TOOLS.get(selected_role, [])
                        transition_skills = JOB_TOOLS.get(transition, [])
                        
                        # Find common skills (simplified approach)
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
                        
                        # Limit to 3 skills for display
                        common_skills = common_skills[:3]
                        
                        st.markdown(f"""
                        <div style="background-color:#1E293B; padding:16px; border-radius:10px; 
                                    border:1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                                <h4 style="color:white; margin:0; font-size:16px; font-weight:600;">{transition}</h4>
                                <div style="background-color:rgba({overlap_color.replace('#', '')}, 0.1); padding:4px 8px; 
                                            border-radius:4px; border:1px solid {overlap_color};">
                                    <span style="color:{overlap_color}; font-size:12px; font-weight:500;">{overlap}% overlap</span>
                                </div>
                            </div>
                            <div>
                                <p style="color:#94A3B8; font-size:14px; margin:0 0 10px 0;">Common skills:</p>
                                <div style="display:flex; flex-wrap:wrap; gap:8px;">
                        """, unsafe_allow_html=True)
                        
                        # Display common skills
                        for skill in common_skills:
                            st.markdown(f"""
                            <div style="background-color:rgba(59, 130, 246, 0.1); padding:4px 8px; 
                                        border-radius:4px; border:1px solid rgba(59, 130, 246, 0.3);">
                                <span style="color:white; font-size:12px;">{skill}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info(f"No common transitions defined for {selected_role}. Try another role.")
        else:
            st.info(f"No roles defined for the {cluster} cluster. Try another cluster.")
