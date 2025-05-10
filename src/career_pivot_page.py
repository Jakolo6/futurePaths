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
    Extracts a career path from free-form CV text with improved cleaning.
    """
    # Split the CV into lines
    lines = cv_text.strip().split('\n')
    
    # Keywords that might indicate job titles
    job_keywords = ["analyst", "head", "manager", "director", "intern", "assistant", 
                   "coordinator", "specialist", "engineer", "developer", "designer",
                   "marketing", "financial", "finance", "sales", "executive", "consultant"]
    
    # Words to remove from extracted titles
    filter_words = ["from", "in", "to", "at", "since", "until"]
    
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
                        potential_title = re.sub(r'\d{4}', '', potential_title)  # Remove years
                        
                        # Remove filter words
                        for filter_word in filter_words:
                            potential_title = re.sub(r'\b' + filter_word + r'\b', '', potential_title)
                        
                        # Clean up extra spaces
                        potential_title = re.sub(r'\s+', ' ', potential_title).strip()
                        
                        if potential_title and len(potential_title.split()) <= 5:  # Reasonable title length
                            # Check if this is semantically similar to any existing role
                            is_duplicate = False
                            for existing_role in extracted_roles:
                                # Simple duplicate check - if the main keywords match
                                if keyword in existing_role and len(set(potential_title.split()) & set(existing_role.split())) >= 2:
                                    is_duplicate = True
                                    break
                            
                            if not is_duplicate:
                                extracted_roles.append(potential_title)
                        break
    
    # Format as a career path
    if extracted_roles:
        return " → ".join(extracted_roles)
    else:
        return None

def run():
    # Clean, consistent header with rocket icon
    st.markdown("""
    <div style="background-color:#1E3A8A; padding:16px; border-radius:10px; margin-bottom:20px;">
        <div style="display:flex; align-items:center;">
            <span style="font-size:24px; margin-right:12px;">🚀</span>
            <div>
                <h1 style="color:white; margin:0; font-size:24px; font-weight:600;">Career Changer Pathfinder</h1>
                <p style="color:#94A3B8; margin:4px 0 0 0; font-size:14px;">Find your next career pivot with smarter AI suggestions! 🎯</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    model, index, next_jobs = load_predictor()

    # Streamlined upload section with consistent sizing
    st.markdown("""
    <div style="background-color:#0F172A; padding:16px; border-radius:10px; margin-bottom:20px; border-left:3px solid #3B82F6;">
        <div style="display:flex; align-items:center; margin-bottom:8px;">
            <span style="font-size:18px; margin-right:10px;">📄</span>
            <h2 style="color:white; margin:0; font-size:18px; font-weight:600;">Upload your CV or enter your career path manually</h2>
        </div>
        <p style="color:#94A3B8; margin:0; font-size:14px;">We'll analyze your career history to suggest your next move</p>
    </div>
    """, unsafe_allow_html=True)
    
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
                st.markdown(f"""
                <div style="background-color:rgba(34, 197, 94, 0.1); padding:12px; border-radius:8px; 
                            margin:16px 0; border-left:3px solid #22C55E;">
                    <div style="display:flex; align-items:center;">
                        <span style="font-size:18px; margin-right:10px;">✅</span>
                        <div>
                            <p style="color:white; margin:0; font-size:14px;">Career path extracted:</p>
                            <p style="color:#22C55E; margin:4px 0 0 0; font-size:15px; font-weight:500;">{extracted_path}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Consistent label for text input
                st.markdown("""
                <p style="color:white; margin:16px 0 8px 0; font-size:15px; font-weight:500;">You can edit the extracted career path or enter manually:</p>
                """, unsafe_allow_html=True)
                
                career_input = st.text_area(
                    "",
                    value=extracted_path,
                    height=100,
                    placeholder="Example: Marketing Intern → Marketing Specialist → Digital Marketing Manager"
                )
            else:
                st.markdown("""
                <div style="background-color:rgba(251, 113, 133, 0.1); padding:12px; border-radius:8px; 
                            margin:16px 0; border-left:3px solid #FB7185;">
                    <div style="display:flex; align-items:center;">
                        <span style="font-size:18px; margin-right:10px;">⚠️</span>
                        <p style="color:white; margin:0; font-size:14px;">Could not extract a clear career path. Please enter manually below.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Consistent label for text input
                st.markdown("""
                <p style="color:white; margin:16px 0 8px 0; font-size:15px; font-weight:500;">Enter your career path:</p>
                """, unsafe_allow_html=True)
                
                career_input = st.text_area(
                    "",
                    height=100,
                    placeholder="Example: Marketing Intern → Marketing Specialist → Digital Marketing Manager"
                )
    else:
        # If no file is uploaded, show empty text area with consistent styling
        st.markdown("""
        <p style="color:white; margin:16px 0 8px 0; font-size:15px; font-weight:500;">Enter your career path:</p>
        """, unsafe_allow_html=True)
        
        career_input = st.text_area(
            "",
            height=100,
            placeholder="Example: Marketing Intern → Marketing Specialist → Digital Marketing Manager"
        )

    # Centered button with consistent styling
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        suggest_clicked = st.button("🔎 Suggest Next Steps", type="primary", use_container_width=True)

    if suggest_clicked:
        if career_input.strip() == "":
            st.markdown("""
            <div style="background-color:rgba(251, 113, 133, 0.1); padding:12px; border-radius:8px; 
                        margin:16px 0; border-left:3px solid #FB7185;">
                <div style="display:flex; align-items:center;">
                    <span style="font-size:18px; margin-right:10px;">⚠️</span>
                    <p style="color:white; margin:0; font-size:14px;">Please enter your career path above.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Analyzing and generating suggestions..."):
                # Embed user input
                input_embedding = model.encode([career_input])
                input_embedding = input_embedding / np.linalg.norm(input_embedding, axis=1, keepdims=True)
                input_embedding = input_embedding.astype('float32')

                # Search using FAISS index
                distances, indices = index.search(input_embedding, 3)

                # Consistent success message for recommendations
                st.markdown("""
                <div style="background-color:#22C55E; padding:12px; border-radius:8px; margin:20px 0 16px 0;">
                    <div style="display:flex; align-items:center;">
                        <span style="font-size:18px; margin-right:10px;">✅</span>
                        <h3 style="color:white; margin:0; font-size:16px; font-weight:600;">Here are your Top 3 Career Pivot Suggestions:</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Consistent job recommendations
                for i, idx in enumerate(indices[0]):
                    confidence = distances[0][i]
                    raw_text = next_jobs[idx]
                    job_title, job_desc = extract_job_title_and_description(raw_text)

                    with st.expander(f"🔎 {job_title} (Similarity: {confidence:.2f})"):
                        st.markdown(f"""
                        <div style="background-color:#1E293B; padding:16px; border-radius:8px; margin:8px 0;">
                            <div style="margin-bottom:16px;">
                                <h4 style="color:#94A3B8; margin:0 0 8px 0; font-weight:500; display:flex; align-items:center;">
                                    <span style="font-size:16px; margin-right:8px;">📝</span>What You'll Do:
                                </h4>
                                <p style="color:white; margin:0; line-height:1.5; font-size:14px;">{job_desc[:300]}...</p>
                            </div>
                            <div style="margin-bottom:16px;">
                                <h4 style="color:#94A3B8; margin:0 0 8px 0; font-weight:500; display:flex; align-items:center;">
                                    <span style="font-size:16px; margin-right:8px;">💼</span>Why It's Interesting:
                                </h4>
                                <p style="color:white; margin:0; line-height:1.5; font-size:14px;">This role is ideal if you want to gain experience in the field and build towards mid- and senior-level positions.</p>
                            </div>
                            <div>
                                <h4 style="color:#94A3B8; margin:0 0 8px 0; font-weight:500; display:flex; align-items:center;">
                                    <span style="font-size:16px; margin-right:8px;">🔗</span>Learn More:
                                </h4>
                                <a href="https://www.google.com/search?q={job_title.replace(' ', '+')}+Internships" 
                                   target="_blank" style="text-decoration:none;">
                                    <div style="background-color:#2563EB; color:white; padding:6px 12px; 
                                                border-radius:6px; display:inline-block; font-weight:500;
                                                font-size:14px;">
                                        Search {job_title} Internships
                                    </div>
                                </a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    # Subtle footer
    st.markdown("""
    <div style="background-color:rgba(15, 23, 42, 0.3); padding:8px; border-radius:6px; margin-top:30px; text-align:center;">
        <p style="color:#64748B; font-size:11px; margin:0;">© 2025 FuturePaths | Career Guidance Platform</p>
    </div>
    """, unsafe_allow_html=True)
