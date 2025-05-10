import streamlit as st
import pandas as pd
import altair as alt

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
    st.caption("Explore average salary ranges and find real-world internships 🔎")

    # Two-column layout
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
        # Display growth trend
        growth_score = JOB_GROWTH.get(job_title, 3)
        st.metric(
            label="Market Growth Trend", 
            value=f"{growth_score}/5",
            delta="Growing" if growth_score >= 4 else ("Stable" if growth_score >= 3 else "Slow")
        )

    if job_title and location:
        st.subheader(f"💰 Salary Estimate for {job_title} in {location}:")
        base_salary = SALARY_BASE_ESTIMATES.get(job_title, 45000)
        adjusted_salary = get_adjusted_salary(base_salary, location)
        st.info(adjusted_salary)
        
        # Salary growth projection
        st.subheader("📈 Salary Growth Projection (5 Years)")
        chart = create_salary_growth_chart(job_title, location)
        st.altair_chart(chart, use_container_width=True)
        
        # Required tools/software
        st.subheader(f"🧰 Required Tools & Software for {job_title}:")
        tools = JOB_TOOLS.get(job_title, ["No specific tools data available"])
        for tool in tools:
            st.markdown(f"- {tool}")
        
        st.subheader(f"🔗 Find {job_title} Opportunities:")
        google_link, linkedin_link, indeed_link = internship_search_links(job_title)

        st.markdown(f"- [🌐 Google Search]({google_link})")
        st.markdown(f"- [💼 LinkedIn Jobs]({linkedin_link})")
        st.markdown(f"- [🔍 Indeed]({indeed_link})")

        # Pro tip section
        st.info(
            f"💡 **Pro Tip:** Consider setting job alerts on LinkedIn to stay updated for new {job_title} opportunities in {location}!"
        )
