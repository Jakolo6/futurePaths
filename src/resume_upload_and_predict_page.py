# resume_upload_and_predict_page.py
import streamlit as st
import numpy as np
# No need to import faiss or SentenceTransformer directly if using functions from career_pivot_page
# from sentence_transformers import SentenceTransformer
# import faiss

# Import functions from other files in the src directory
from utils.resume_parser import parse_resume_data
from career_pivot_page import load_predictor, extract_job_title_and_description

def generate_suggestions_from_text(model, index, next_jobs_data, query_text, top_n=5):
    """
    Generates suggestions based on a query text.
    This is similar to the logic in career_pivot_page but generalized.
    """
    if not query_text or not model or index is None or next_jobs_data is None:
        return []
        
    input_embedding = model.encode([query_text])
    input_embedding = input_embedding / np.linalg.norm(input_embedding, axis=1, keepdims=True)
    input_embedding = input_embedding.astype('float32')

    try:
        distances, indices = index.search(input_embedding, top_n)
    except Exception as e:
        st.error(f"FAISS search error: {e}. Ensure the index is loaded correctly and compatible.")
        return []
    
    results = []
    if indices.size > 0 and len(indices[0]) > 0:
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(next_jobs_data):
                # This case should ideally not happen if index and data are consistent
                # print(f"Warning: Index {idx} out of bounds for next_jobs_data (size {len(next_jobs_data)})")
                continue
            
            # In career_pivot_page, 'distances' are used directly as 'confidence'.
            # For IndexFlatIP (cosine similarity) with normalized vectors, this is correct.
            # Higher values mean higher similarity.
            confidence_score = distances[0][i] 
            
            raw_job_text = next_jobs_data[idx]
            job_title, job_desc = extract_job_title_and_description(raw_job_text) # Reusing this
            results.append({
                "title": job_title,
                "description": job_desc,
                "confidence": confidence_score 
            })
    return results


def run(): # Standardized run function for Streamlit pages
    st.title("📄 Resume Analyzer & Career Suggester")
    
    # Load the model, FAISS index, and job data
    # This uses the cached function from career_pivot_page
    try:
        model, faiss_index, next_jobs_data = load_predictor()
    except Exception as e:
        st.error(f"Failed to load predictor resources: {e}")
        st.error("Please ensure 'src/next_jobs.npy' and 'src/faiss_index.index' exist and are valid, and that 'sentence-transformers/all-MiniLM-L6-v2' can be downloaded/loaded.")
        st.warning("The application might not function correctly without these resources.")
        # Attempt to proceed if only some parts failed, or stop if critical
        if 'faiss_index' not in locals() or 'next_jobs_data' not in locals():
             st.stop() # Stop if critical components are missing

    st.markdown("""
    Upload your resume (PDF) to extract your experience and skills.
    Then, get tailored career suggestions for conventional paths or exciting pivots!
    """)

    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf", key="resume_uploader")
    
    if 'parsed_resume_data' not in st.session_state:
        st.session_state.parsed_resume_data = None
    if 'resume_filename' not in st.session_state:
        st.session_state.resume_filename = None

    if uploaded_file is not None:
        if st.session_state.resume_filename != uploaded_file.name:
            with st.spinner("🔬 Analyzing your resume... This may take a moment."):
                parsed_data = parse_resume_data(uploaded_file) # from src.resume_parser
                if parsed_data and "error" not in parsed_data:
                    st.session_state.parsed_resume_data = parsed_data
                    st.session_state.resume_filename = uploaded_file.name
                    st.success("Resume analyzed successfully!")
                elif parsed_data and "error" in parsed_data:
                    st.error(f"Resume parsing failed: {parsed_data['error']}")
                    st.session_state.parsed_resume_data = None
                    st.session_state.resume_filename = None
                else:
                    st.error("Could not parse the resume or the file is empty. Please try a different PDF.")
                    st.session_state.parsed_resume_data = None
                    st.session_state.resume_filename = None
    
    if st.session_state.parsed_resume_data:
        data = st.session_state.parsed_resume_data
        
        # Add debug section to see what's extracted
        with st.expander("Debug - View Extracted Data"):
            st.write("Raw parsed resume data:", data)
            
            # Check specific fields we're trying to access
            st.write("Most Recent Job:", data.get("most_recent_job", "Not found"))
            if data.get("most_recent_job"):
                st.write("- Job Title:", data["most_recent_job"].get("title", "Not found"))
                st.write("- Job Description:", data["most_recent_job"].get("description", "Not found"))
            
            st.write("Skills:", data.get("skills", "Not found"))
        
        st.subheader("📝 Extracted Resume Insights")

        # NEW: Add editable text fields for extracted information
        # Most recent job title and description
        if data.get("most_recent_job"):
            mrj = data["most_recent_job"]
            st.write("**Most Recent Role (extracted, you can edit):**")
            edited_job_title = st.text_input(
                "",
                value=mrj.get('title', 'N/A'),
                key="edited_job_title"
            )
            
            st.write("**Role Description (you can edit):**")
            edited_job_description = st.text_area(
                "",
                value=mrj.get('description', '')[:1000] + ("..." if len(mrj.get('description', '')) > 1000 else ""),
                height=150,
                key="edited_job_description"
            )
        else:
            st.write("**Most Recent Role (enter manually):**")
            edited_job_title = st.text_input(
                "",
                placeholder="Enter your most recent job title",
                key="manual_job_title"
            )
            
            st.write("**Role Description (enter manually):**")
            edited_job_description = st.text_area(
                "",
                placeholder="Describe your responsibilities and experience",
                height=150,
                key="manual_job_description"
            )

        # Skills section with editable field
        if data.get("skills"):
            st.write("**Extracted Skills (you can edit):**")
            skills_text = ", ".join(data['skills'][:20]) + ("..." if len(data['skills']) > 20 else "")
            edited_skills = st.text_area(
                "",
                value=skills_text,
                height=100,
                key="edited_skills"
            )
        else:
            st.write("**Skills (enter manually):**")
            edited_skills = st.text_area(
                "",
                placeholder="Enter your key skills (comma separated)",
                height=100,
                key="edited_skills_manual"
            )
        
        st.markdown("---")
        
        suggestion_type = st.radio(
            "Choose suggestion type:",
            ("📈 Conventional Career Path", "↔️ Career Pivot"),
            key="suggestion_type_radio"
        )

        if suggestion_type == "📈 Conventional Career Path":
            st.subheader("📈 Conventional Career Path Suggestions")
            
            # Check if we have enough information
            if not edited_job_title.strip() and not edited_skills.strip():
                st.warning("Limited information provided. Please enter your job title or skills above for better suggestions.")
            
            if st.button("Suggest Conventional Paths", key="conv_button"):
                # Use edited information to construct query
                query_text_conventional = ""
                if edited_job_title.strip():
                    query_text_conventional = f"Current role: {edited_job_title}. "
                if edited_job_description.strip():
                    desc_snippet = edited_job_description[:300] + "..." if len(edited_job_description) > 300 else edited_job_description
                    query_text_conventional += f"Responsibilities and experience include: {desc_snippet}. "
                if edited_skills.strip():
                    query_text_conventional += f"Key skills include: {edited_skills}."
                
                if not query_text_conventional.strip():
                    st.error("Cannot generate suggestions without some information. Please provide job title, description, or skills.")
                else:
                    with st.spinner("Finding conventional next steps..."):
                        recommendations = generate_suggestions_from_text(
                            model, faiss_index, next_jobs_data, query_text_conventional, top_n=3
                        )
                        if recommendations:
                            st.success(f"Here are your Top {len(recommendations)} Conventional Suggestions:")
                            for rec in recommendations:
                                with st.expander(f"{rec['title']} (Similarity: {rec['confidence']:.2f})"):
                                    st.markdown(f"**Description Snippet:**\n{rec['description'][:300]}...")
                                    st.markdown(f"**🔗 Learn More:** [Search for {rec['title']}](https://www.google.com/search?q={rec['title'].replace(' ', '+')})")
                        else:
                            st.info("No specific conventional path suggestions found based on the provided information. Try adjusting your job details or skills.")
        
        elif suggestion_type == "↔️ Career Pivot":
            st.subheader("↔️ Career Pivot Suggestions")
            aspirations = st.text_area(
                "Optional: Describe your professional aspirations or interests for a pivot (e.g., 'I want to work in data science', 'Interested in sustainability and tech', 'Enjoy creative problem solving and user-centered design')",
                height=100,
                key="aspirations_input_resume"
            )
            
            if st.button("Suggest Career Pivots", key="pivot_button_resume"):
                # Use edited information to construct query
                query_text_pivot = ""
                if edited_skills.strip():
                    query_text_pivot += f"Seeking a new role leveraging skills such as: {edited_skills}. "
                elif edited_job_description.strip():
                    desc_snippet = edited_job_description[:300] + "..." if len(edited_job_description) > 300 else edited_job_description
                    query_text_pivot += f"Experienced in tasks such as: {desc_snippet}. "
                
                if aspirations.strip():
                    query_text_pivot += f"Future career aspirations and interests include: {aspirations.strip()}."
                else: 
                    query_text_pivot += "Open to exploring challenging new career directions and pivot opportunities that build upon existing experience."
                
                if not query_text_pivot.strip() or (not edited_skills.strip() and not edited_job_description.strip() and not aspirations.strip()):
                    st.warning("Not enough information provided. Please enter your skills, job description, or aspirations for better pivot suggestions.")
                else:
                    with st.spinner("Exploring career pivot options..."):
                        recommendations = generate_suggestions_from_text(
                            model, faiss_index, next_jobs_data, query_text_pivot, top_n=3
                        )
                        if recommendations:
                            st.success(f"Here are your Top {len(recommendations)} Pivot Suggestions:")
                            for rec in recommendations:
                                with st.expander(f"{rec['title']} (Similarity: {rec['confidence']:.2f})"):
                                    st.markdown(f"**Description Snippet:**\n{rec['description'][:300]}...")
                                    st.markdown(f"**Why it might be a good pivot:** This role may align with your stated interests or offer a new application for your existing skills and experience.")
                                    st.markdown(f"**🔗 Learn More:** [Search for {rec['title']}](https://www.google.com/search?q={rec['title'].replace(' ', '+')})")
                        else:
                            st.info("No career pivot suggestions found. Try refining your skills, experience description, or aspirations.")
    else:
        if uploaded_file is None:
            st.info("👋 Welcome! Please upload your resume (PDF) to get started.")
        # If upload failed or parsing yielded nothing, message already shown
