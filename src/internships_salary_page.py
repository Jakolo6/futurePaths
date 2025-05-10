import streamlit as st
import pandas as pd
import altair as alt

# Add custom CSS for enhanced styling
st.markdown("""
<style>
.card {
  background-color: #1E293B;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 35px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}
.card-header {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 20px;
  letter-spacing: 0.5px;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 15px;
}
.salary-card {
  background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
  border-left: 5px solid #3B82F6;
}
.tool-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background-color: rgba(59, 130, 246, 0.1);
  margin-bottom: 15px;
}
.tool-item img {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}
.job-link {
  text-decoration: none;
  display: block;
  padding: 15px;
  background-color: #1E293B;
  border-radius: 10px;
  text-align: center;
  color: white;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.job-link:hover {
  background-color: #2D3748;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.header-container {
  background-color: #1E3A8A;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 25px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
.growth-indicator {
  background-color: #0F172A;
  padding: 15px;
  border-radius: 12px;
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.pro-tip {
  background-color: #0F172A;
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
  border-left: 5px solid #22C55E;
}
.footer {
  background-color:rgba(15, 23, 42, 0.3);
  padding:8px;
  border-radius:6px;
  margin-top:40px;
  text-align:center;
  width:100%;
}
</style>
""", unsafe_allow_html=True)

# 🔧 Enhanced salary database with more roles
SALARY_BASE_ESTIMATES = {
    "Data Analyst": 45000,
    "Data Scientist": 52500,
    "UX Designer": 43000,
    "Marketing Manager": 48500,
    "Product Manager": 60000,
    "Software Engineer": 55000,
    "Frontend Developer": 50000,
    "Backend Developer": 53000,
    "Full Stack Developer": 57000,
    "DevOps Engineer": 62000,
    "Machine Learning Engineer": 65000,
    "Business Analyst": 47000,
    "Project Manager": 55000,
    "Content Writer": 40000,
    "Graphic Designer": 42000,
}

# 🌍 Global location adjustment factors (percentage)
LOCATION_ADJUSTMENTS = {
    "New York, USA": 1.0,  # Base reference
    "San Francisco, USA": 0.90,
    "London, UK": 0.78,
    "Zurich, Switzerland": 1.04,
    "Singapore": 0.79,
    "Tokyo, Japan": 0.75,
    "Sydney, Australia": 0.68,
    "Paris, France": 0.68,
    "Amsterdam, Netherlands": 0.68,
    "Dubai, UAE": 0.72,
    "Hong Kong": 0.74,
    "Berlin, Germany": 0.65,
    "Munich, Germany": 0.66,
    "Toronto, Canada": 0.67,
    "Seoul, South Korea": 0.63,
    "Remote": 0.70,
}

# 🛠️ Required tools/software by role
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

# 📈 Growth trend indicators (1-5 scale, 5 being highest growth)
JOB_GROWTH = {
    "Data Analyst": 4,
    "Data Scientist": 5,
    "UX Designer": 4,
    "Marketing Manager": 3,
    "Product Manager": 4,
    "Software Engineer": 5,
    "Frontend Developer": 4,
    "Backend Developer": 4,
    "Full Stack Developer": 5,
    "DevOps Engineer": 5,
    "Machine Learning Engineer": 5,
    "Business Analyst": 3,
    "Project Manager": 3,
    "Content Writer": 2,
    "Graphic Designer": 3,
}

# 🔍 Helper to create search links
def internship_search_links(job_title):
    google_link = f"https://www.google.com/search?q={job_title.replace(' ', '+')}+Internships"
    linkedin_link = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}%20Internship"
    indeed_link = f"https://de.indeed.com/jobs?q={job_title.replace(' ', '+')}"
    return google_link, linkedin_link, indeed_link

# 💰 Calculate adjusted salary based on location
def get_adjusted_salary(base_salary, location):
    adjustment_factor = LOCATION_ADJUSTMENTS.get(location, 1.0)
    adjusted_salary = base_salary * adjustment_factor
    return f"€{int(adjusted_salary - 5000)} - €{int(adjusted_salary + 5000)} / year"

# 📊 Create salary growth chart
def create_salary_growth_chart(job_title, location):
    # Mock data for 5-year salary progression
    base = SALARY_BASE_ESTIMATES.get(job_title, 45000)
    adjustment = LOCATION_ADJUSTMENTS.get(location, 1.0)
    
    years = list(range(2025, 2030))
    salaries = [int(base * adjustment * (1 + 0.05 * i)) for i in range(5)]
    
    df = pd.DataFrame({
        'Year': years,
        'Salary (€)': salaries
    })
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Salary (€):Q', title='Estimated Salary (€)'),
        tooltip=['Year', 'Salary (€)']
    ).properties(
        title=f'Projected Salary Growth for {job_title} in {location}',
        width=500,
        height=300
    )
    
    return chart

def run():
    st.title("💼 Internship & Salary Insights")
    
    # Enhanced header with better styling
    st.markdown("""
    <div class="header-container">
        <h3 style="color:white; margin:0;">Explore average salary ranges and find real-world internships 🔎</h3>
    </div>
    """, unsafe_allow_html=True)

    # Two-column layout with better spacing
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User input: select a job role to explore
        job_title = st.selectbox(
            "Select a job title to explore:",
            sorted(list(SALARY_BASE_ESTIMATES.keys()))
        )
        
        # Location selection
        location = st.selectbox(
            "Select a location:",
            sorted(list(LOCATION_ADJUSTMENTS.keys()))
        )

    with col2:
        # Visual growth meter
        growth_score = JOB_GROWTH.get(job_title, 3)
        growth_color = "#22C55E" if growth_score >= 4 else ("#64748B" if growth_score >= 3 else "#EF4444")
        growth_percentage = (growth_score / 5) * 100
        
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
                    padding:20px; border-radius:12px; height:100%;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
            <h4 style="color:white; margin:0 0 15px 0; text-align:center; font-weight:600;">Market Growth Trend</h4>
            <div style="font-size:38px; text-align:center; margin-bottom:10px; color:{growth_color};">{growth_score}/5</div>
            <div style="background-color:#1E293B; height:10px; border-radius:5px; margin:15px 0;">
                <div style="background-color:{growth_color}; width:{growth_percentage}%; height:10px; border-radius:5px;"></div>
            </div>
            <p style="color:{growth_color}; margin:10px 0 0 0; text-align:center; font-weight:500;">
                {"Growing" if growth_score >= 4 else ("Stable" if growth_score >= 3 else "Slow")}
            </p>
        </div>
        """, unsafe_allow_html=True)

    if job_title and location:
        # Enhanced salary card with more visual impact
        base_salary = SALARY_BASE_ESTIMATES.get(job_title, 45000)
        adjusted_salary = get_adjusted_salary(base_salary, location)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
                    border-radius:12px; padding:25px; margin:20px 0;
                    border-left:5px solid #3B82F6; box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);">
            <div style="display:flex; align-items:center; margin-bottom:15px;">
                <span style="font-size:32px; margin-right:15px;">💰</span>
                <h3 style="color:white; margin:0; font-weight:600;">Salary Estimate for {job_title} in {location}:</h3>
            </div>
            <div style="background-color:rgba(59, 130, 246, 0.1); padding:15px; border-radius:8px; text-align:center;">
                <h2 style="color:#3B82F6; font-size:32px; margin:0; font-weight:700;">{adjusted_salary}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced section header with gradient and icon
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                    padding:15px; border-radius:10px; margin:25px 0 15px 0; 
                    display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <span style="font-size:24px; margin-right:10px;">📈</span>
            <h3 style="color:white; margin:0; font-weight:600;">Salary Growth Projection (5 Years)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        chart = create_salary_growth_chart(job_title, location)
        st.altair_chart(chart, use_container_width=True)
        
        # Enhanced section header for tools
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                    padding:15px; border-radius:10px; margin:25px 0 15px 0; 
                    display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <span style="font-size:24px; margin-right:10px;">🧰</span>
            <h3 style="color:white; margin:0; font-weight:600;">Required Tools & Software for {job_title}:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Tools displayed as cards in a grid
        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top:20px;">
        """, unsafe_allow_html=True)
        
        tools = JOB_TOOLS.get(job_title, ["No specific tools data available"])
        tools_html = ""
        
        for tool in tools:
            # Map tool names to appropriate icons with more variety
            icon = "⚙️"
            if "Python" in tool:
                icon = "🐍"
            elif "SQL" in tool:
                icon = "🗃️"
            elif "Excel" in tool:
                icon = "📊"
            elif "Tableau" in tool or "Power BI" in tool:
                icon = "📈"
            elif "Git" in tool:
                icon = "🔄"
            elif "Docker" in tool:
                icon = "🐳"
            elif "Kubernetes" in tool:
                icon = "☸️"
            elif "JavaScript" in tool:
                icon = "🌐"
            elif "React" in tool:
                icon = "⚛️"
            elif "Adobe" in tool:
                icon = "🎨"
            elif "Figma" in tool:
                icon = "🖌️"
            elif "Sketch" in tool:
                icon = "✏️"
            elif "Jira" in tool:
                icon = "📋"
            elif "Asana" in tool:
                icon = "📝"
            
            tools_html += f"""
            <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
                        border-radius:10px; padding:15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                        transition: transform 0.2s, box-shadow 0.2s; height:100%;">
                <div style="font-size:28px; margin-bottom:10px; text-align:center;">{icon}</div>
                <p style="margin:0; color:white; text-align:center; font-weight:500;">{tool}</p>
            </div>
            """
        
        st.markdown(f"{tools_html}</div>", unsafe_allow_html=True)
        
        # Enhanced section header for job opportunities
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #1E3A8A 0%, #1E293B 100%); 
                    padding:15px; border-radius:10px; margin:25px 0 15px 0; 
                    display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <span style="font-size:24px; margin-right:10px;">🔗</span>
            <h3 style="color:white; margin:0; font-weight:600;">Find {job_title} Opportunities:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Modern Apple-style buttons for job search
        google_link, linkedin_link, indeed_link = internship_search_links(job_title)
        
        st.markdown(f"""
        <div style="margin-top:20px;">
            <div style="display:flex; gap:15px; flex-wrap:wrap; justify-content:center;">
                <a href="{google_link}" target="_blank" style="text-decoration:none; flex:1;">
                    <div style="background-color:#2563EB; color:white; padding:12px 20px; 
                                border-radius:12px; text-align:center; min-width:120px;
                                box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
                                transition: all 0.3s ease;">
                        <div style="font-size:24px; margin-bottom:8px;">🌐</div>
                        <p style="margin:0; font-weight:500;">Google Search</p>
                    </div>
                </a>
                <a href="{linkedin_link}" target="_blank" style="text-decoration:none; flex:1;">
                    <div style="background-color:#0077B5; color:white; padding:12px 20px; 
                                border-radius:12px; text-align:center; min-width:120px;
                                box-shadow: 0 4px 6px rgba(0, 119, 181, 0.2);
                                transition: all 0.3s ease;">
                        <div style="font-size:24px; margin-bottom:8px;">💼</div>
                        <p style="margin:0; font-weight:500;">LinkedIn Jobs</p>
                    </div>
                </a>
                <a href="{indeed_link}" target="_blank" style="text-decoration:none; flex:1;">
                    <div style="background-color:#2557A7; color:white; padding:12px 20px; 
                                border-radius:12px; text-align:center; min-width:120px;
                                box-shadow: 0 4px 6px rgba(37, 87, 167, 0.2);
                                transition: all 0.3s ease;">
                        <div style="font-size:24px; margin-bottom:8px;">🔍</div>
                        <p style="margin:0; font-weight:500;">Indeed</p>
                    </div>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced pro tip with better visual design
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, rgba(34, 197, 94, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
                    padding:15px; border-radius:10px; margin-top:30px; 
                    border-left:5px solid #22C55E; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; margin-right:10px;">💡</span>
                <p style="margin:0; color:white;"><strong>Pro Tip:</strong> Consider setting job alerts on LinkedIn to stay updated for new {job_title} opportunities in {location}!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # More subtle footer
        st.markdown("""
        <div style="background-color:rgba(15, 23, 42, 0.3); padding:8px; border-radius:6px; margin-top:40px; text-align:center; width:100%;">
            <p style="color:#64748B; font-size:11px; margin:0;">© 2025 FuturePaths | Career Guidance Platform</p>
        </div>
        """, unsafe_allow_html=True)
