import streamlit as st
import random

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
                    # Extract only the numeric part using string split
                    numeric_part = duration.replace("+", "").split()[0]  # This will get just the "5" from "5 years"
                    total_years += int(numeric_part)

            
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
                                    <span style="color:#3B82F6; font-size:12px; font-weight:500;">{year_start}-{year_end if "+" not in step["duration"] else str(year_end)+"+"}</span>
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

