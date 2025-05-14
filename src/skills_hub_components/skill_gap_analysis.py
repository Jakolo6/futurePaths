import streamlit as st
import plotly.graph_objects as go
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

# Create skill proficiency requirements for each job
SKILL_REQUIREMENTS = {}

# Function to convert tools to skill requirements
def generate_skill_requirements():
    for job, tools in JOB_TOOLS.items():
        skill_dict = {}
        for tool in tools:
            # Create a skill name from the tool
            skill_name = tool.split('/')[0] if '/' in tool else tool
            # Assign a required proficiency level (7-10 for most job requirements)
            skill_dict[skill_name] = random.randint(7, 10)
        SKILL_REQUIREMENTS[job] = skill_dict

# Generate the skill requirements
generate_skill_requirements()

def display_skill_gap_analysis():
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                padding:16px; border-radius:10px; margin:20px 0 15px 0; 
                display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <span style="font-size:24px; margin-right:10px;">📊</span>
        <h3 style="color:white; margin:0; font-weight:600;">Skill Gap Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#94A3B8; margin-bottom:20px;">
        Compare your current skills with those required for your target career path. Identify gaps and prioritize your learning.
    </p>
    """, unsafe_allow_html=True)
    
    # Job title selection
    job_title = st.selectbox(
        "Select a target career path:",
        sorted(list(JOB_TOOLS.keys())),
        key="skill_gap_job"
    )
    
    if job_title:
        # Get the skills for this job
        job_skills = JOB_TOOLS.get(job_title, [])
        skill_requirements = SKILL_REQUIREMENTS.get(job_title, {})
        
        if job_skills:
            st.markdown(f"""
            <div style="background-color:rgba(59, 130, 246, 0.1); padding:12px; border-radius:8px; 
                        margin:16px 0; border-left:3px solid #3B82F6;">
                <div style="display:flex; align-items:center;">
                    <span style="font-size:18px; margin-right:10px;">💡</span>
                    <p style="color:white; margin:0; font-size:14px;">
                        Rate your proficiency in each skill required for a <strong>{job_title}</strong> role
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # User skill assessment
            st.markdown("""
            <p style="color:white; margin:20px 0 10px 0; font-size:16px; font-weight:500;">Rate your skills (1-10):</p>
            """, unsafe_allow_html=True)
            
            # Create a dictionary to store user's skill ratings
            user_skills = {}
            
            # Display sliders for each skill
            for tool in job_skills:
                # Extract the main skill name
                skill_name = tool.split('/')[0] if '/' in tool else tool
                
                # Get the required proficiency for this skill
                required_proficiency = skill_requirements.get(skill_name, 8)
                
                # Create a slider for user to rate their proficiency
                user_proficiency = st.slider(
                    f"{skill_name}",
                    min_value=1,
                    max_value=10,
                    value=5,
                    help=f"Required proficiency: {required_proficiency}/10"
                )
                
                # Store the user's rating
                user_skills[skill_name] = user_proficiency
            
            # Create radar chart data
            if user_skills:
                st.markdown("""
                <p style="color:white; margin:30px 0 15px 0; font-size:18px; font-weight:600;">Your Skill Gap Analysis:</p>
                """, unsafe_allow_html=True)
                
                # Prepare data for radar chart
                categories = list(user_skills.keys())
                user_values = [user_skills[skill] for skill in categories]
                required_values = [skill_requirements.get(skill, 8) for skill in categories]
                
                # Close the loop by repeating the first point at the end
                categories = categories + [categories[0]]
                user_values = user_values + [user_values[0]]
                required_values = required_values + [required_values[0]]
                
                # Create radar chart using Plotly
                fig = go.Figure()
                
                # Add required skills trace
                fig.add_trace(go.Scatterpolar(
                    r=required_values,
                    theta=categories,
                    fill='toself',
                    name='Required Skills',
                    line_color='rgba(59, 130, 246, 0.8)',
                    fillcolor='rgba(59, 130, 246, 0.2)'
                ))
                
                # Add user skills trace
                fig.add_trace(go.Scatterpolar(
                    r=user_values,
                    theta=categories,
                    fill='toself',
                    name='Your Skills',
                    line_color='rgba(34, 197, 94, 0.8)',
                    fillcolor='rgba(34, 197, 94, 0.2)'
                ))
                
                # Update layout
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 10]
                        )
                    ),
                    showlegend=True,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    ),
                    margin=dict(l=80, r=80, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                # Display the chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate skill gaps and strengths
                # Note: Use the original categories without the duplicated point for calculations
                original_categories = list(user_skills.keys())
                gaps = []
                strengths = []
                
                for skill in original_categories:
                    user_value = user_skills[skill]
                    required_value = skill_requirements.get(skill, 8)
                    
                    if user_value < required_value:
                        gap_size = required_value - user_value
                        gaps.append((skill, gap_size))
                    elif user_value >= required_value:
                        strength_size = user_value - required_value
                        strengths.append((skill, strength_size))
                
                # Sort gaps by size (largest first)
                gaps.sort(key=lambda x: x[1], reverse=True)
                
                # Display gaps and recommendations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div style="background-color:#1E293B; padding:16px; border-radius:10px; height:100%;
                                border:1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <h3 style="color:white; margin:0 0 15px 0; font-size:18px; font-weight:600; display:flex; align-items:center;">
                            <span style="font-size:20px; margin-right:8px;">🔍</span>Skills to Improve
                        </h3>
                    """, unsafe_allow_html=True)
                    
                    if gaps:
                        for skill, gap_size in gaps:
                            gap_color = "#EF4444" if gap_size >= 3 else "#F59E0B"
                            
                            st.markdown(f"""
                            <div style="margin-bottom:12px; padding-bottom:12px; border-bottom:1px solid rgba(255, 255, 255, 0.05);">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                                    <span style="color:white; font-weight:500;">{skill}</span>
                                    <span style="color:{gap_color}; font-weight:600;">Gap: {gap_size}</span>
                                </div>
                                <div style="background-color:#1E293B; height:6px; border-radius:3px; width:100%;">
                                    <div style="background-color:{gap_color}; width:{gap_size*10}%; height:6px; border-radius:3px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <p style="color:#94A3B8; font-size:14px;">No significant skill gaps detected. You're well-prepared for this role!</p>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background-color:#1E293B; padding:16px; border-radius:10px; height:100%;
                                border:1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <h3 style="color:white; margin:0 0 15px 0; font-size:18px; font-weight:600; display:flex; align-items:center;">
                            <span style="font-size:20px; margin-right:8px;">💪</span>Your Strengths
                        </h3>
                    """, unsafe_allow_html=True)
                    
                    if strengths:
                        for skill, strength_size in strengths:
                            st.markdown(f"""
                            <div style="margin-bottom:12px; padding-bottom:12px; border-bottom:1px solid rgba(255, 255, 255, 0.05);">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                                    <span style="color:white; font-weight:500;">{skill}</span>
                                    <span style="color:#22C55E; font-weight:600;">+{strength_size}</span>
                                </div>
                                <div style="background-color:#1E293B; height:6px; border-radius:3px; width:100%;">
                                    <div style="background-color:#22C55E; width:{min(strength_size*10, 100)}%; height:6px; border-radius:3px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <p style="color:#94A3B8; font-size:14px;">Keep developing your skills to exceed the requirements for this role.</p>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Recommended next steps
                if gaps:
                    st.markdown("""
                    <div style="background: linear-gradient(90deg, rgba(34, 197, 94, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
                                padding:16px; border-radius:10px; margin-top:20px; 
                                border-left:5px solid #22C55E; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                        <div style="display:flex; align-items:flex-start;">
                            <span style="font-size:24px; margin-right:10px; margin-top:2px;">💡</span>
                            <div>
                                <p style="color:white; margin:0 0 10px 0; font-weight:600;">Recommended Next Steps:</p>
                    """, unsafe_allow_html=True)
                    
                    # Get the top 2 gaps to focus on
                    focus_gaps = gaps[:2]
                    for skill, _ in focus_gaps:
                        st.markdown(f"""
                        <p style="color:white; margin:5px 0; font-size:14px;">• Focus on improving your <strong>{skill}</strong> skills</p>
                        """, unsafe_allow_html=True)
                    
                    # Add a recommendation to check the courses tab
                    st.markdown("""
                        <p style="color:white; margin:5px 0; font-size:14px;">• Check the <strong>Courses</strong> tab for learning resources</p>
                        <p style="color:white; margin:5px 0; font-size:14px;">• Consider projects that will help you develop these skills</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"No specific skill requirements available for {job_title}. Try another career path.")
