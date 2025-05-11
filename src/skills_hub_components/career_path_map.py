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

def display_career_path_map():
    # Add CSS for tree diagram
    st.markdown("""
    <style>
        /* Tree diagram container */
        .tree-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 40px;
            position: relative;
        }
        
        /* Root node (current role) */
        .root-node {
            background-color: #3B82F6;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
            margin-bottom: 50px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            position: relative;
            z-index: 2;
            min-width: 180px;
        }
        
        /* Tree branches container */
        .branches-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 800px;
            position: relative;
        }
        
        /* Vertical line from root */
        .vertical-line {
            position: absolute;
            top: -50px;
            left: 50%;
            width: 2px;
            height: 50px;
            background-color: #64748B;
        }
        
        /* Horizontal line connecting all branches */
        .horizontal-line {
            position: absolute;
            top: 0;
            left: 10%;
            width: 80%;
            height: 2px;
            background-color: #64748B;
        }
        
        /* Branch container */
        .branch {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            width: 30%;
        }
        
        /* Vertical branch line */
        .branch-line {
            width: 2px;
            height: 60px;
            background-color: #64748B;
            margin-bottom: 15px;
        }
        
        /* Leaf node (transition role) */
        .leaf-node {
            background-color: #22C55E;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 100%;
            position: relative;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .leaf-node:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* Overlap badge */
        .overlap-badge {
            position: absolute;
            top: -10px;
            right: -10px;
            background-color: #1E293B;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid #3B82F6;
        }
        
        /* Tooltip for skill details */
        .tooltip {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1E293B;
            color: white;
            padding: 10px 15px;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 200px;
            z-index: 10;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .leaf-node:hover .tooltip {
            opacity: 1;
            visibility: visible;
        }
        
        /* Arrow for tooltip */
        .tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -8px;
            border-width: 8px;
            border-style: solid;
            border-color: #1E293B transparent transparent transparent;
        }
        
        /* Skill tag */
        .skill-tag {
            background-color: rgba(59, 130, 246, 0.2);
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            margin: 3px;
            display: inline-block;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        /* Transition info section */
        .transition-info {
            margin-top: 60px;
            background-color: rgba(30, 41, 59, 0.5);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .branches-container {
                flex-direction: column;
                align-items: center;
            }
            
            .branch {
                width: 80%;
                margin-bottom: 40px;
            }
            
            .horizontal-line {
                display: none;
            }
            
            .vertical-line {
                height: 100%;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
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
                    
                    # Calculate skill overlaps
                    overlaps = []
                    common_skills_list = []
                    
                    for transition in display_transitions:
                        # Calculate mock skill overlap percentage
                        overlap = random.randint(60, 90)
                        overlaps.append(overlap)
                        
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
                        
                        common_skills_list.append(common_skills[:3])  # Limit to 3 skills for display
                    
                    # Generate the tree diagram HTML
                    tree_html = f"""
                    <div class="tree-container">
                        <div class="root-node">{selected_role}</div>
                        <div class="branches-container">
                            <div class="vertical-line"></div>
                            <div class="horizontal-line"></div>
                    """
                    
                    # Add branches for each transition
                    for i, transition in enumerate(display_transitions):
                        overlap = overlaps[i]
                        common_skills = common_skills_list[i]
                        
                        # Determine color based on overlap
                        if overlap >= 80:
                            color = "#22C55E"  # Green for high overlap
                        elif overlap >= 70:
                            color = "#F59E0B"  # Amber for medium overlap
                        else:
                            color = "#3B82F6"  # Blue for lower overlap
                        
                        # Generate tooltip content
                        tooltip_content = f"""
                        <div class="tooltip">
                            <strong>Common Skills:</strong><br>
                        """
                        
                        for skill in common_skills:
                            tooltip_content += f'<span class="skill-tag">{skill}</span>'
                        
                        tooltip_content += f"""
                            <br><br>
                            <strong>Transition Difficulty:</strong><br>
                            <span style="color:{color}">{'Easy' if overlap >= 80 else 'Moderate' if overlap >= 70 else 'Challenging'}</span>
                            <br><br>
                            <small>Click to explore this role</small>
                        </div>
                        """
                        
                        tree_html += f"""
                        <div class="branch">
                            <div class="branch-line"></div>
                            <div class="leaf-node" style="background-color:{color};" 
                                 onclick="document.getElementById('transition-info-{i}').scrollIntoView({{behavior: 'smooth'}})">
                                {transition}
                                <div class="overlap-badge">{overlap}%</div>
                                {tooltip_content}
                            </div>
                        </div>
                        """
                    
                    tree_html += """
                        </div>
                    </div>
                    """
                    
                    # Render the tree diagram
                    st.markdown(tree_html, unsafe_allow_html=True)
                    
                    # Add detailed transition information section
                    st.markdown("""
                    <h3 style="color:white; margin:40px 0 20px 0; font-size:20px; font-weight:600;">Transition Details</h3>
                    """, unsafe_allow_html=True)
                    
                    # Display detailed information for each transition
                    for i, transition in enumerate(display_transitions):
                        overlap = overlaps[i]
                        common_skills = common_skills_list[i]
                        
                        # Determine color based on overlap
                        if overlap >= 80:
                            overlap_color = "#22C55E"  # Green for high overlap
                            difficulty = "Easy Transition"
                            difficulty_desc = "You already have most of the skills needed for this role."
                        elif overlap >= 70:
                            overlap_color = "#F59E0B"  # Amber for medium overlap
                            difficulty = "Moderate Transition"
                            difficulty_desc = "You have some transferable skills, but will need to develop new ones."
                        else:
                            overlap_color = "#3B82F6"  # Blue for lower overlap
                            difficulty = "Challenging Transition"
                            difficulty_desc = "This role requires significant upskilling but could be a rewarding pivot."
                        
                        st.markdown(f"""
                        <div id="transition-info-{i}" class="transition-info">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;">
                                <h3 style="color:white; margin:0; font-size:18px; font-weight:600;">{selected_role} → {transition}</h3>
                                <div style="background-color:rgba({overlap_color.replace('#', '')}, 0.1); padding:4px 8px; 
                                            border-radius:4px; border:1px solid {overlap_color};">
                                    <span style="color:{overlap_color}; font-size:12px; font-weight:500;">{overlap}% Skill Overlap</span>
                                </div>
                            </div>
                            
                            <div style="margin-bottom:15px;">
                                <h4 style="color:#94A3B8; font-size:14px; margin:0 0 8px 0;">Transition Difficulty:</h4>
                                <div style="display:flex; align-items:center;">
                                    <div style="width:15px; height:15px; background-color:{overlap_color}; border-radius:50%; margin-right:8px;"></div>
                                    <span style="color:white; font-weight:500;">{difficulty}</span>
                                </div>
                                <p style="color:#94A3B8; margin:5px 0 0 23px; font-size:13px;">{difficulty_desc}</p>
                            </div>
                            
                            <div style="margin-bottom:15px;">
                                <h4 style="color:#94A3B8; font-size:14px; margin:0 0 8px 0;">Transferable Skills:</h4>
                                <div style="display:flex; flex-wrap:wrap; gap:8px;">
                        """, unsafe_allow_html=True)
                        
                        # Display common skills
                        for skill in common_skills:
                            st.markdown(f"""
                            <div style="background-color:rgba(59, 130, 246, 0.1); padding:6px 10px; 
                                        border-radius:6px; border:1px solid rgba(59, 130, 246, 0.3);">
                                <span style="color:white; font-size:13px;">{skill}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Get skills to develop (skills in target role that aren't in common skills)
                        transition_skills = JOB_TOOLS.get(transition, [])
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
                        
                        # Limit to 3 skills
                        skills_to_develop = skills_to_develop[:3]
                        
                        st.markdown("""
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if skills_to_develop:
                            st.markdown(f"""
                            <div style="margin-bottom:15px;">
                                <h4 style="color:#94A3B8; font-size:14px; margin:0 0 8px 0;">Skills to Develop:</h4>
                                <div style="display:flex; flex-wrap:wrap; gap:8px;">
                            """, unsafe_allow_html=True)
                            
                            # Display skills to develop
                            for skill in skills_to_develop:
                                st.markdown(f"""
                                <div style="background-color:rgba(251, 113, 133, 0.1); padding:6px 10px; 
                                            border-radius:6px; border:1px solid rgba(251, 113, 133, 0.3);">
                                    <span style="color:white; font-size:13px;">{skill}</span>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("""
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Add recommended courses section
                        st.markdown(f"""
                        <div>
                            <h4 style="color:#94A3B8; font-size:14px; margin:0 0 8px 0;">Recommended Resources:</h4>
                            <a href="https://www.coursera.org/search?query={transition.replace(' ', '%20')}" target="_blank" style="text-decoration:none;">
                                <div style="background-color:#2563EB; color:white; padding:8px 12px; 
                                            border-radius:6px; display:inline-block; font-weight:500;
                                            font-size:14px; margin-right:10px;">
                                    Find Courses
                                </div>
                            </a>
                            <a href="https://www.linkedin.com/jobs/search/?keywords={transition.replace(' ', '%20')}" target="_blank" style="text-decoration:none;">
                                <div style="background-color:#1E293B; color:white; padding:8px 12px; 
                                            border-radius:6px; display:inline-block; font-weight:500;
                                            font-size:14px; border:1px solid #3B82F6;">
                                    View Job Listings
                                </div>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Add some spacing between transition cards
                        if i < len(display_transitions) - 1:
                            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                else:
                    st.info(f"No common transitions defined for {selected_role}. Try another role.")
        else:
            st.info(f"No roles defined for the {cluster} cluster. Try another cluster.")
