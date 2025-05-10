import streamlit as st
import pandas as pd
import altair as alt

# Add custom CSS for enhanced styling
st.markdown("""
<style>
.card {
  background-color: #1E293B;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
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
  margin-bottom: 15px;
  letter-spacing: 0.5px;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
}
.salary-card {
  background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
  border-left: 5px solid #3B82F6;
}
.tool-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: rgba(59, 130, 246, 0.1);
  margin-bottom: 8px;
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
  background-color: #0F172A;
  padding: 10px;
  border-radius: 10px;
  margin-top: 30px;
  text-align: center;
  font-size: 12px;
  color: #94A3B8;
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

# 📊 Create salary growth chart with enhanced styling
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
    
    # Enhanced chart with gridlines and better styling
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Salary (€):Q', 
                title='Estimated Salary (€)',
                scale=alt.Scale(zero=False),
                axis=alt.Axis(grid=True, format='€,.0f')),
        tooltip=['Year', alt.Tooltip('Salary (€)', format='€,.0f')]
    ).properties(
        title=f'Projected Salary Growth for {job_title} in {location}',
        width=500,
        height=300
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
        gridColor='#1E293B',
        domainColor='#94A3B8'
    ).configure_title(
        fontSize=16,
        color='#F8FAFC'
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
        # Enhanced growth trend display with better styling
        growth_score = JOB_GROWTH.get(job_title, 3)
        growth_color = "#22C55E" if growth_score >= 4 else ("#64748B" if growth_score >= 3 else "#EF4444")
        st.markdown(f"""
        <div class="growth-indicator">
            <h4 style="color:white; margin:0 0 10px 0;">Market Growth Trend</h4>
            <h2 style="color:{growth_color}; font-size:32px; margin:0 0 10px 0;">{growth_score}/5</h2>
            <p style="color:{growth_color}; margin:0; font-weight:500;">
                {"Growing" if growth_score >= 4 else ("Stable" if growth_score >= 3 else "Slow")}
            </p>
        </div>
        """, unsafe_allow_html=True)

    if job_title and location:
        # Enhanced salary information card
        base_salary = SALARY_BASE_ESTIMATES.get(job_title, 45000)
        adjusted_salary = get_adjusted_salary(base_salary, location)
        st.markdown(f"""
        <div class="card salary-card">
            <h3 class="card-header">💰 Salary Estimate for {job_title} in {location}:</h3>
            <h2 style="color:#3B82F6; text-align:center; font-size:28px; margin:0;">{adjusted_salary}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced salary growth projection
        st.markdown(f"""
        <div class="card">
            <h3 class="card-header">📈 Salary Growth Projection (5 Years)</h3>
        </div>
        """, unsafe_allow_html=True)
        chart = create_salary_growth_chart(job_title, location)
        st.altair_chart(chart, use_container_width=True)
        
        # Enhanced tools section with better styling
        st.markdown(f"""
        <div class="card">
            <h3 class="card-header">🧰 Required Tools & Software for {job_title}:</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        """, unsafe_allow_html=True)
        
        # Generate tool items HTML
        tools_html = ""
        tools = JOB_TOOLS.get(job_title, ["No specific tools data available"])
        for tool in tools:
            # Map tool names to appropriate icons
            icon = "⚙️"
            if "Python" in tool:
                icon = "🐍"
            elif "SQL" in tool:
                icon = "🗃️"
            elif "Excel" in tool or "Tableau" in tool:
                icon = "📊"
            elif "Git" in tool:
                icon = "🔄"
            elif "Docker" in tool or "Kubernetes" in tool:
                icon = "🐳"
            elif "JavaScript" in tool or "React" in tool:
                icon = "🌐"
            elif "Adobe" in tool or "Figma" in tool or "Sketch" in tool:
                icon = "🎨"
            elif "Jira" in tool or "Asana" in tool:
                icon = "📋"
            
            tools_html += f"""
            <div class="tool-item">
                <span style="margin-right:10px;">{icon}</span>
                <span>{tool}</span>
            </div>
            """
        
        st.markdown(f"{tools_html}</div></div>", unsafe_allow_html=True)
        
        # Enhanced job links section
        st.markdown(f"""
        <div class="card">
            <h3 class="card-header">🔗 Find {job_title} Opportunities:</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
        """, unsafe_allow_html=True)
        
        google_link, linkedin_link, indeed_link = internship_search_links(job_title)
        
        links_html = f"""
        <a href="{google_link}" target="_blank" class="job-link">
            🌐 Google Search
        </a>
        
        <a href="{linkedin_link}" target="_blank" class="job-link">
            💼 LinkedIn Jobs
        </a>
        
        <a href="{indeed_link}" target="_blank" class="job-link">
            🔍 Indeed
        </a>
        """
        
        st.markdown(f"{links_html}</div></div>", unsafe_allow_html=True)

        # Enhanced pro tip with better styling
        st.markdown(f"""
        <div class="pro-tip">
            <p style="margin:0; color:white;">💡 <strong>Pro Tip:</strong> Consider setting job alerts on LinkedIn to stay updated for new {job_title} opportunities in {location}!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="footer">
            © 2025 FuturePaths | Career Guidance Platform
        </div>
        """, unsafe_allow_html=True)
