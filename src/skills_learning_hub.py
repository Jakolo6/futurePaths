import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random

# Mock data for course recommendations
COURSE_RECOMMENDATIONS = {
    "Data Analyst": [
        {"title": "Data Analysis with Python", "platform": "Coursera", "provider": "IBM", "level": "Intermediate", "duration": "5 weeks", "url": "https://www.coursera.org/learn/data-analysis-with-python"},
        {"title": "SQL for Data Analysis", "platform": "Udemy", "provider": "365 Careers", "level": "Beginner", "duration": "4 weeks", "url": "https://www.udemy.com/course/sql-for-data-analysis/"},
        {"title": "Data Visualization with Tableau", "platform": "Coursera", "provider": "UC Davis", "level": "Intermediate", "duration": "6 weeks", "url": "https://www.coursera.org/learn/data-visualization-tableau"},
        {"title": "Excel for Data Analysis", "platform": "LinkedIn Learning", "provider": "Microsoft", "level": "Beginner", "duration": "3 weeks", "url": "https://www.linkedin.com/learning/excel-data-analysis-forecasting"}
    ],
    "Data Scientist": [
        {"title": "Machine Learning", "platform": "Coursera", "provider": "Stanford University", "level": "Advanced", "duration": "11 weeks", "url": "https://www.coursera.org/learn/machine-learning"},
        {"title": "Deep Learning Specialization", "platform": "Coursera", "provider": "deeplearning.ai", "level": "Advanced", "duration": "3 months", "url": "https://www.coursera.org/specializations/deep-learning"},
        {"title": "Python for Data Science", "platform": "edX", "provider": "MIT", "level": "Intermediate", "duration": "8 weeks", "url": "https://www.edx.org/course/python-for-data-science-2"},
        {"title": "Applied Data Science with Python", "platform": "Coursera", "provider": "University of Michigan", "level": "Intermediate", "duration": "5 weeks", "url": "https://www.coursera.org/specializations/data-science-python"}
    ],
    "UX Designer": [
        {"title": "UI / UX Design Specialization", "platform": "Coursera", "provider": "California Institute of the Arts", "level": "Beginner", "duration": "6 months", "url": "https://www.coursera.org/specializations/ui-ux-design"},
        {"title": "User Experience Research and Design", "platform": "Coursera", "provider": "University of Michigan", "level": "Intermediate", "duration": "6 months", "url": "https://www.coursera.org/specializations/michiganux"},
        {"title": "Figma UI UX Design Essentials", "platform": "Udemy", "provider": "Daniel Walter Scott", "level": "Beginner", "duration": "10 hours", "url": "https://www.udemy.com/course/figma-ux-ui-design-user-experience-tutorial/"},
        {"title": "Adobe XD - UI/UX Design", "platform": "Udemy", "provider": "Daniel Walter Scott", "level": "Beginner", "duration": "12 hours", "url": "https://www.udemy.com/course/adobe-xd-ui-ux-design/"}
    ],
    "Software Engineer": [
        {"title": "The Web Developer Bootcamp", "platform": "Udemy", "provider": "Colt Steele", "level": "Beginner", "duration": "9 weeks", "url": "https://www.udemy.com/course/the-web-developer-bootcamp/"},
        {"title": "Data Structures and Algorithms", "platform": "Coursera", "provider": "UC San Diego", "level": "Intermediate", "duration": "6 months", "url": "https://www.coursera.org/specializations/data-structures-algorithms"},
        {"title": "Full Stack Web Development", "platform": "Coursera", "provider": "Hong Kong University", "level": "Intermediate", "duration": "6 months", "url": "https://www.coursera.org/specializations/full-stack-react"},
        {"title": "DevOps with Docker", "platform": "edX", "provider": "University of Helsinki", "level": "Intermediate", "duration": "6 weeks", "url": "https://www.edx.org/course/devops-with-docker"}
    ],
    "Marketing Manager": [
        {"title": "Digital Marketing Specialization", "platform": "Coursera", "provider": "University of Illinois", "level": "Intermediate", "duration": "8 months", "url": "https://www.coursera.org/specializations/digital-marketing"},
        {"title": "Marketing Analytics", "platform": "Coursera", "provider": "University of Virginia", "level": "Intermediate", "duration": "4 months", "url": "https://www.coursera.org/learn/uva-darden-market-analytics"},
        {"title": "Google Digital Marketing & E-commerce", "platform": "Coursera", "provider": "Google", "level": "Beginner", "duration": "6 months", "url": "https://www.coursera.org/professional-certificates/google-digital-marketing-ecommerce"},
        {"title": "Social Media Marketing", "platform": "LinkedIn Learning", "provider": "LinkedIn", "level": "Beginner", "duration": "4 weeks", "url": "https://www.linkedin.com/learning/social-media-marketing-foundations-2021"}
    ],
    "Product Manager": [
        {"title": "Digital Product Management", "platform": "edX", "provider": "Boston University", "level": "Intermediate", "duration": "4 weeks", "url": "https://www.edx.org/course/digital-product-management"},
        {"title": "Agile Development", "platform": "Coursera", "provider": "University of Virginia", "level": "Intermediate", "duration": "4 weeks", "url": "https://www.coursera.org/learn/uva-darden-agile-development"},
        {"title": "Product Management Essentials", "platform": "Udemy", "provider": "Cole Mercer", "level": "Beginner", "duration": "8 hours", "url": "https://www.udemy.com/course/productmanagement/"},
        {"title": "Product Strategy", "platform": "LinkedIn Learning", "provider": "LinkedIn", "level": "Advanced", "duration": "2 weeks", "url": "https://www.linkedin.com/learning/product-strategy-for-product-managers"}
    ]
}

# Add more job titles from your salary page to maintain consistency
for job_title in ["Frontend Developer", "Backend Developer", "Full Stack Developer", "DevOps Engineer", 
                 "Machine Learning Engineer", "Business Analyst", "Project Manager", "Content Writer", "Graphic Designer"]:
    if job_title not in COURSE_RECOMMENDATIONS:
        # Generate generic courses for jobs not specifically defined
        COURSE_RECOMMENDATIONS[job_title] = [
            {"title": f"Essential Skills for {job_title}s", "platform": "Coursera", "provider": "Industry Experts", "level": "Beginner", "duration": "6 weeks", "url": f"https://www.coursera.org/search?query={job_title.replace(' ', '%20')}"},
            {"title": f"Advanced {job_title} Techniques", "platform": "Udemy", "provider": "Top Instructors", "level": "Advanced", "duration": "8 weeks", "url": f"https://www.udemy.com/courses/search/?q={job_title.replace(' ', '%20')}"},
            {"title": f"{job_title} Certification Preparation", "platform": "edX", "provider": "Leading University", "level": "Intermediate", "duration": "10 weeks", "url": f"https://www.edx.org/search?q={job_title.replace(' ', '%20')}"},
            {"title": f"Practical {job_title} Projects", "platform": "LinkedIn Learning", "provider": "Industry Professionals", "level": "Intermediate", "duration": "4 weeks", "url": f"https://www.linkedin.com/learning/search?keywords={job_title.replace(' ', '%20')}"}
        ]

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

def display_course_recommendations():
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                padding:16px; border-radius:10px; margin:20px 0 15px 0; 
                display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <span style="font-size:24px; margin-right:10px;">🎓</span>
        <h3 style="color:white; margin:0; font-weight:600;">Recommended Online Courses</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#94A3B8; margin-bottom:20px;">
        Discover courses that can help you develop the skills needed for your target career path.
    </p>
    """, unsafe_allow_html=True)
    
    # Job title selection
    job_title = st.selectbox(
        "Select a career path to explore courses:",
        sorted(list(COURSE_RECOMMENDATIONS.keys()))
    )
    
    if job_title:
        courses = COURSE_RECOMMENDATIONS.get(job_title, [])
        
        if courses:
            st.markdown(f"""
            <div style="background-color:rgba(59, 130, 246, 0.1); padding:12px; border-radius:8px; 
                        margin:16px 0; border-left:3px solid #3B82F6;">
                <div style="display:flex; align-items:center;">
                    <span style="font-size:18px; margin-right:10px;">💡</span>
                    <p style="color:white; margin:0; font-size:14px;">
                        We found <strong>{len(courses)}</strong> recommended courses for <strong>{job_title}s</strong>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                level_filter = st.multiselect(
                    "Filter by level:",
                    ["Beginner", "Intermediate", "Advanced"],
                    default=["Beginner", "Intermediate", "Advanced"]
                )
            with col2:
                platform_filter = st.multiselect(
                    "Filter by platform:",
                    ["Coursera", "Udemy", "edX", "LinkedIn Learning"],
                    default=["Coursera", "Udemy", "edX", "LinkedIn Learning"]
                )
            
            # Apply filters
            filtered_courses = [
                course for course in courses 
                if course["level"] in level_filter and course["platform"] in platform_filter
            ]
            
            if filtered_courses:
                # Display courses in cards
                for course in filtered_courses:
                    level_color = {
                        "Beginner": "#22C55E",
                        "Intermediate": "#3B82F6",
                        "Advanced": "#8B5CF6"
                    }.get(course["level"], "#3B82F6")
                    
                    platform_icon = {
                        "Coursera": "🔵",
                        "Udemy": "🔴",
                        "edX": "🟣",
                        "LinkedIn Learning": "🔷"
                    }.get(course["platform"], "🔶")
                    
                    st.markdown(f"""
                    <div style="background-color:#1E293B; padding:16px; border-radius:10px; margin-bottom:16px; 
                                border:1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                            <h3 style="color:white; margin:0; font-size:18px; font-weight:600;">{course["title"]}</h3>
                            <div style="background-color:rgba({level_color.replace('#', '')}, 0.1); padding:4px 8px; 
                                        border-radius:4px; border:1px solid {level_color};">
                                <span style="color:{level_color}; font-size:12px; font-weight:500;">{course["level"]}</span>
                            </div>
                        </div>
                        <div style="display:flex; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
                            <div style="display:flex; align-items:center;">
                                <span style="color:#94A3B8; font-size:14px; margin-right:4px;">Platform:</span>
                                <span style="color:white; font-size:14px;">{platform_icon} {course["platform"]}</span>
                            </div>
                            <div style="display:flex; align-items:center;">
                                <span style="color:#94A3B8; font-size:14px; margin-right:4px;">Provider:</span>
                                <span style="color:white; font-size:14px;">{course["provider"]}</span>
                            </div>
                            <div style="display:flex; align-items:center;">
                                <span style="color:#94A3B8; font-size:14px; margin-right:4px;">Duration:</span>
                                <span style="color:white; font-size:14px;">{course["duration"]}</span>
                            </div>
                        </div>
                        <a href="{course["url"]}" target="_blank" style="text-decoration:none;">
                            <div style="background-color:#2563EB; color:white; padding:8px 12px; 
                                        border-radius:6px; display:inline-block; font-weight:500;
                                        font-size:14px; margin-top:8px;">
                                View Course
                            </div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No courses match your filter criteria. Try adjusting the filters.")
        else:
            st.info(f"No specific course recommendations available for {job_title}. Try another career path.")

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
                gaps = []
                strengths = []
                
                for skill in categories:
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

def display_career_timeline():
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                padding:16px; border-radius:10px; margin:20px 0 15px 0; 
                display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <span style="font-size:24px; margin-right:10px;">⏳</span>
        <h3 style="color:white; margin:0; font-weight:600;">Career Timeline</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color:#94A3B8; margin-bottom:20px;">
        Explore typical career progression paths and timeframes for different roles.
    </p>
    """, unsafe_allow_html=True)
    
    # Mock career paths with timeline data
    CAREER_PATHS = {
        "Data Analyst": [
            {"role": "Data Analyst Intern", "duration": "3-6 months", "salary": "€25,000", "skills": ["Excel", "SQL basics", "Data visualization"]},
            {"role": "Junior Data Analyst", "duration": "1-2 years", "salary": "€45,000", "skills": ["SQL", "Python basics", "Tableau/Power BI"]},
            {"role": "Data Analyst", "duration": "2-3 years", "salary": "€60,000", "skills": ["Advanced SQL", "Python/R", "Statistical analysis"]},
            {"role": "Senior Data Analyst", "duration": "3+ years", "salary": "€75,000", "skills": ["Data modeling", "Team leadership", "Business strategy"]},
            {"role": "Analytics Manager", "duration": "4+ years", "salary": "€90,000", "skills": ["Team management", "Strategic planning", "Executive communication"]}
        ],
        "Software Engineer": [
            {"role": "Software Engineering Intern", "duration": "3-6 months", "salary": "€30,000", "skills": ["Programming basics", "Version control", "Testing"]},
            {"role": "Junior Software Engineer", "duration": "1-2 years", "salary": "€55,000", "skills": ["Full-stack development", "Agile methodologies", "Code reviews"]},
            {"role": "Software Engineer", "duration": "2-3 years", "salary": "€70,000", "skills": ["System design", "Performance optimization", "CI/CD"]},
            {"role": "Senior Software Engineer", "duration": "3-5 years", "salary": "€85,000", "skills": ["Architecture design", "Technical leadership", "Mentoring"]},
            {"role": "Lead Engineer / Architect", "duration": "5+ years", "salary": "€100,000+", "skills": ["System architecture", "Team leadership", "Strategic planning"]}
        ],
        "UX Designer": [
            {"role": "UX Design Intern", "duration": "3-6 months", "salary": "€25,000", "skills": ["Design tools", "Wireframing", "User research basics"]},
            {"role": "Junior UX Designer", "duration": "1-2 years", "salary": "€43,000", "skills": ["Prototyping", "User testing", "Information architecture"]},
            {"role": "UX Designer", "duration": "2-3 years", "salary": "€55,000", "skills": ["Interaction design", "User research", "Design systems"]},
            {"role": "Senior UX Designer", "duration": "3-5 years", "salary": "€70,000", "skills": ["Strategic design", "Team leadership", "Cross-functional collaboration"]},
            {"role": "UX Lead / Manager", "duration": "5+ years", "salary": "€85,000+", "skills": ["Design leadership", "Design strategy", "Mentoring"]}
        ],
        "Data Scientist": [
            {"role": "Data Science Intern", "duration": "3-6 months", "salary": "€30,000", "skills": ["Python", "Statistics basics", "Data visualization"]},
            {"role": "Junior Data Scientist", "duration": "1-2 years", "salary": "€52,500", "skills": ["Machine learning basics", "Data preprocessing", "Model evaluation"]},
            {"role": "Data Scientist", "duration": "2-3 years", "salary": "€70,000", "skills": ["Advanced ML algorithms", "Feature engineering", "Model deployment"]},
            {"role": "Senior Data Scientist", "duration": "3-5 years", "salary": "€85,000", "skills": ["Deep learning", "MLOps", "Research leadership"]},
            {"role": "Lead Data Scientist / ML Manager", "duration": "5+ years", "salary": "€100,000+", "skills": ["AI strategy", "Team leadership", "Business impact"]}
        ],
        "Product Manager": [
            {"role": "Associate Product Manager", "duration": "1-2 years", "salary": "€50,000", "skills": ["User research", "Agile methodologies", "Product requirements"]},
            {"role": "Product Manager", "duration": "2-3 years", "salary": "€65,000", "skills": ["Product strategy", "Stakeholder management", "Data analysis"]},
            {"role": "Senior Product Manager", "duration": "3-5 years", "salary": "€80,000", "skills": ["Product roadmapping", "Cross-functional leadership", "Market analysis"]},
            {"role": "Product Lead / Director", "duration": "5+ years", "salary": "€100,000+", "skills": ["Product vision", "Team leadership", "Executive communication"]}
        ]
    }
    
    # Add generic paths for other roles
    for job_title in ["Frontend Developer", "Backend Developer", "Full Stack Developer", "DevOps Engineer", 
                     "Machine Learning Engineer", "Business Analyst", "Project Manager", "Content Writer", "Graphic Designer"]:
        if job_title not in CAREER_PATHS:
            CAREER_PATHS[job_title] = [
                {"role": f"{job_title} Intern", "duration": "3-6 months", "salary": "€25,000-€30,000", "skills": ["Entry-level skills", "Basic tools", "Fundamentals"]},
                {"role": f"Junior {job_title}", "duration": "1-2 years", "salary": "€40,000-€55,000", "skills": ["Core competencies", "Team collaboration", "Industry standards"]},
                {"role": f"{job_title}", "duration": "2-3 years", "salary": "€55,000-€70,000", "skills": ["Advanced techniques", "Project leadership", "Specialized skills"]},
                {"role": f"Senior {job_title}", "duration": "3-5 years", "salary": "€70,000-€85,000", "skills": ["Strategic thinking", "Mentoring", "Cross-functional collaboration"]},
                {"role": f"Lead {job_title} / Manager", "duration": "5+ years", "salary": "€85,000+", "skills": ["Leadership", "Strategic planning", "Business alignment"]}
            ]
    
    # Job title selection
    job_title = st.selectbox(
        "Select a career path to explore:",
        sorted(list(CAREER_PATHS.keys())),
        key="timeline_job"
    )
    
    if job_title:
        career_path = CAREER_PATHS.get(job_title, [])
        
        if career_path:
            st.markdown(f"""
            <div style="background-color:rgba(59, 130, 246, 0.1); padding:12px; border-radius:8px; 
                        margin:16px 0; border-left:3px solid #3B82F6;">
                <div style="display:flex; align-items:center;">
                    <span style="font-size:18px; margin-right:10px;">🔍</span>
                    <p style="color:white; margin:0; font-size:14px;">
                        Typical career progression for <strong>{job_title}s</strong> (timeframes may vary by company and location)
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display timeline
            st.markdown("""
            <div style="margin-top:30px;">
            """, unsafe_allow_html=True)
            
            # Calculate total years
            total_years = 0
            for step in career_path:
                # Extract the first number from the duration string
                duration = step["duration"].split("-")[0]
                if duration.isdigit():
                    total_years += int(duration)
                else:
                    # Handle cases like "3+ years"
                    total_years += int(duration.replace("+", ""))
            
            # Display each step in the career path
            for i, step in enumerate(career_path):
                # Determine the position marker color
                if i == 0:
                    marker_color = "#3B82F6"  # Blue for starting position
                elif i == len(career_path) - 1:
                    marker_color = "#22C55E"  # Green for final position
                else:
                    marker_color = "#8B5CF6"  # Purple for intermediate positions
                
                # Calculate the year range for this position
                year_start = 2025
                if i > 0:
                    # Calculate based on previous positions
                    for j in range(i):
                        prev_duration = career_path[j]["duration"].split("-")[0]
                        if prev_duration.isdigit():
                            year_start += int(prev_duration)
                        else:
                            # Handle cases like "3+ years"
                            year_start += int(prev_duration.replace("+", ""))
                
                # Extract the first number from the duration string
                duration = step["duration"].split("-")[0]
                if duration.isdigit():
                    year_end = year_start + int(duration)
                else:
                    # Handle cases like "3+ years"
                    year_end = year_start + int(duration.replace("+", ""))
                
                # Create the timeline entry
                st.markdown(f"""
                <div style="display:flex; margin-bottom:30px; position:relative;">
                    <div style="position:relative; margin-right:20px; display:flex; flex-direction:column; align-items:center;">
                        <div style="width:20px; height:20px; background-color:{marker_color}; border-radius:50%; z-index:2;"></div>
                        {'' if i == len(career_path) - 1 else '<div style="width:2px; height:100%; background-color:#475569; position:absolute; top:20px; bottom:0;"></div>'}
                    </div>
                    <div style="flex:1;">
                        <div style="background-color:#1E293B; padding:16px; border-radius:10px; 
                                    border:1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                                <h3 style="color:white; margin:0; font-size:18px; font-weight:600;">{step["role"]}</h3>
                                <div style="background-color:rgba(59, 130, 246, 0.1); padding:4px 8px; 
                                            border-radius:4px; border:1px solid #3B82F6;">
                                    <span style="color:#3B82F6; font-size:12px; font-weight:500;">{year_start}-{year_end if "+" not in step["duration"] else year_end+"+"}</span>
                                </div>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                                <div style="display:flex; align-items:center;">
                                    <span style="color:#94A3B8; font-size:14px; margin-right:4px;">Duration:</span>
                                    <span style="color:white; font-size:14px;">{step["duration"]}</span>
                                </div>
                                <div style="display:flex; align-items:center;">
                                    <span style="color:#94A3B8; font-size:14px; margin-right:4px;">Typical Salary:</span>
                                    <span style="color:white; font-size:14px;">{step["salary"]}</span>
                                </div>
                            </div>
                            <div>
                                <span style="color:#94A3B8; font-size:14px; margin-right:4px;">Key Skills:</span>
                                <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px;">
                """, unsafe_allow_html=True)
                
                # Display skills as badges
                for skill in step["skills"]:
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
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add a note about alternative paths
            st.markdown("""
            <div style="background: linear-gradient(90deg, rgba(139, 92, 246, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
                        padding:16px; border-radius:10px; margin-top:30px; 
                        border-left:5px solid #8B5CF6; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                <div style="display:flex; align-items:flex-start;">
                    <span style="font-size:24px; margin-right:10px; margin-top:2px;">💡</span>
                    <div>
                        <p style="color:white; margin:0 0 10px 0; font-weight:600;">Alternative Career Paths:</p>
                        <p style="color:white; margin:5px 0; font-size:14px;">• Career progression can vary significantly based on industry, company size, and location</p>
                        <p style="color:white; margin:5px 0; font-size:14px;">• Many professionals take non-linear paths, including lateral moves to gain diverse experience</p>
                        <p style="color:white; margin:5px 0; font-size:14px;">• Consider specializing in high-demand areas to accelerate your career growth</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"No career timeline available for {job_title}. Try another career path.")

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
                    
                    # Tips for career transitions
                    st.markdown("""
                    <div style="background: linear-gradient(90deg, rgba(34, 197, 94, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
                                padding:16px; border-radius:10px; margin-top:30px; 
                                border-left:5px solid #22C55E; box-shadow: 0 4px 6px rgba(0, 0, 0,
