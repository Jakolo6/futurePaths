import streamlit as st
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

