import numpy as np
import faiss
import streamlit as st
import time
import re
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_predictor():
    # Load precomputed job labels + FAISS index
    next_jobs = np.load('src/next_jobs.npy', allow_pickle=True)
    index = faiss.read_index('src/faiss_index.index')

    # Load SentenceTransformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return model, index, next_jobs

def extract_job_title_and_description(raw_text):
    """
    Splits the raw job text into (title, description).
    """
    parts = raw_text.split("description:")
    title = parts[0].replace("esco role:", "").strip().capitalize()
    description = parts[1].strip() if len(parts) > 1 else "No description available."
    return title, description

def extract_career_path_from_cv(cv_text):
    """
    Extracts a career path from free-form CV text.
    """
    # Split the CV into lines
    lines = cv_text.strip().split('\n')
    
    # Keywords that might indicate job titles
    job_keywords = ["analyst", "head", "manager", "director", "intern", "assistant", 
                   "coordinator", "specialist", "engineer", "developer", "designer",
                   "marketing", "financial", "finance", "sales", "executive", "consultant"]
    
    # Extract potential job titles and create a career path
    extracted_roles = []
    
    for line in lines:
        line = line.lower()
        # Skip education-related lines if they don't contain job information
        if any(word in line for word in ["studied", "graduated", "university", "college"]) and not any(word in line for word in job_keywords):
            continue
            
        # Look for job title patterns
        for keyword in job_keywords:
            if keyword in line:
                # Extract the job title using surrounding words
                words = line.split()
                for i, word in enumerate(words):
                    if keyword in word:
                        # Try to get a few words before and after to capture the full title
                        start = max(0, i-2)
                        end = min(len(words), i+3)
                        potential_title = " ".join(words[start:end])
                        
                        # Clean up the extracted title
                        potential_title = re.sub(r'in \d{4}|until \d{4}|at .*?(?=\s\d{4}|\s[a-z]|$)', '', potential_title)
                        potential_title = potential_title.strip()
                        
                        if potential_title and len(potential_title.split()) <= 5:  # Reasonable title length
                            extracted_roles.append(potential_title)
                        break
    
    # Remove duplicates while preserving order
    unique_roles = []
    for role in extracted_roles:
        if role not in unique_roles:
            unique_roles.append(role)
    
    # Format as a career path
    if unique_roles:
        return " → ".join(unique_roles)
    else:
        return None

def run():
    st.title("🚀 Career Changer Pathfinder")
    st.caption("Find your next career pivot with smarter AI suggestions! 🎯")

    model, index, next_jobs = load_predictor()

    # Add CV upload option
    st.subheader("📄 Upload your CV or enter your career path manually")
    
    uploaded_file = st.file_uploader("Upload your CV (TXT format)", type=["txt"])
    
    # Variable to store the career path (either from upload or manual entry)
    career_input = ""
    
    if uploaded_file is not None:
        with st.spinner("Analyzing your CV..."):
            # Add a slight delay to simulate processing
            time.sleep(1.5)
            
            # Read the file content
            content = uploaded_file.getvalue().decode("utf-8")
            
            # Extract career path
            extracted_path = extract_career_path_from_cv(content)
            
            if extracted_path:
                st.success(f"✅ Career path extracted: {extracted_path}")
                # Pre-fill the text area with the extracted path
                career_input = st.text_area(
                    "You can edit the extracted career path or enter manually:",
                    value=extracted_path
                )
            else:
                st.warning("Could not extract a clear career path. Please enter manually below.")
                career_input = st.text_area(
                    "Example: Marketing Intern → Marketing Specialist → Digital Marketing Manager"
                )
    else:
        # If no file is uploaded, show empty text area
        career_input = st.text_area(
            "Example: Marketing Intern → Marketing Specialist → Digital Marketing Manager"
        )

    if st.button("🔎 Suggest Next Steps"):
        if career_input.strip() == "":
            st.warning("Please enter your career path above.")
        else:
            with st.spinner("Analyzing and generating suggestions..."):
                # Embed user input
                input_embedding = model.encode([career_input])
                input_embedding = input_embedding / np.linalg.norm(input_embedding, axis=1, keepdims=True)
                input_embedding = input_embedding.astype('float32')

                # Search using FAISS index
                distances, indices = index.search(input_embedding, 3)

                st.success("✅ Here are your Top 3 Career Pivot Suggestions:")

                for i, idx in enumerate(indices[0]):
                    confidence = distances[0][i]
                    raw_text = next_jobs[idx]
                    job_title, job_desc = extract_job_title_and_description(raw_text)

                    with st.expander(f"🔎 {job_title} (Similarity: {confidence:.2f})"):
                        st.markdown(f"**📝 What You'll Do:**\n{job_desc[:300]}...")  # Shortened
                        st.markdown("**💼 Why It's Interesting:**\nThis role is ideal if you want to gain experience in the field and build towards mid- and senior-level positions.")
                        st.markdown(f"**🔗 Learn More:** [Search {job_title} Internships](https://www.google.com/search?q={job_title.replace(' ', '+')}+Internships)")
