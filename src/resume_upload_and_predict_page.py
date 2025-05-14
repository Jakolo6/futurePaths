# resume_upload_and_predict_page.py
import streamlit as st
import numpy as np

# Import functions from other files in the src directory
from utils.resume_parser import parse_resume_data
from career_pivot_page import load_predictor, extract_job_title_and_description

def generate_suggestions_from_text(model, index, next_jobs_data, query_text, top_n=5):
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
    for i, idx in enumerate(indices[0]):
        if idx < 0 or idx >= len(next_jobs_data):
            continue
        confidence_score = distances[0][i] 
        raw_job_text = next_jobs_data[idx]
        job_title, job_desc = extract_job_title_and_description(raw_job_text)
        results.append({
            "title": job_title,
            "description": job_desc,
            "confidence": confidence_score 
        })
    return results

def run():
    st.title("📄 Resume Analyzer & Career Suggester")

    try:
        model, faiss_index, next_jobs_data = load_predictor()
    except Exception as e:
        st.error(f"Failed to load predictor resources: {e}")
        st.stop()

    st.markdown("""
    Upload your resume (PDF) to extract your experience and skills.
    Then, get tailored career suggestions for conventional paths or exciting pivots!
    """)

    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

    if uploaded_file:
        with st.spinner("🔬 Analyzing your resume..."):
            parsed_data = parse_resume_data(uploaded_file)
            if "error" in parsed_data:
                st.error(parsed_data["error"])
                return
    else:
        st.info("👋 Upload a resume to begin.")
        return

    job = parsed_data.get("most_recent_job", {})
    skills = parsed_data.get("skills", [])

    job_title = st.text_input("Most Recent Job Title", job.get("title", ""))
    job_desc = st.text_area("Role Description", job.get("description", ""), height=150)
    skill_text = st.text_area("Skills (comma separated)", ", ".join(skills), height=100)
    aspirations = st.text_area("Optional: What are your career aspirations?", height=100)

    if st.button("Suggest Career Pivots"):
        query_text = ""
        aspirations_lower = aspirations.strip().lower()

        if "consult" in aspirations_lower:
            aspiration_boost = (
                "I am actively looking to pivot into consulting roles such as Strategy Consultant or Business Analyst. "
                "My goal is to use my analytical skills in a consulting environment to solve business challenges. "
            ) * 2  # Boost by repeating
            query_text += aspiration_boost
        else:
            query_text += f"Career Aspiration: {aspirations.strip()}. "

        if skill_text.strip():
            query_text += f"Skills: {skill_text}. "
        if job_desc.strip():
            desc_snippet = job_desc[:300] + ("..." if len(job_desc) > 300 else "")
            query_text += f"Experience summary: {desc_snippet}. "

        if not query_text.strip():
            st.warning("Please provide enough information to generate suggestions.")
            return

        with st.spinner("Generating suggestions..."):
            suggestions = generate_suggestions_from_text(model, faiss_index, next_jobs_data, query_text, top_n=3)
            if suggestions:
                st.success("Here are your pivot suggestions:")
                for s in suggestions:
                    with st.expander(f"{s['title']} (Similarity: {s['confidence']:.2f})"):
                        st.markdown(f"**Description:**\n{s['description'][:300]}...")
                        st.markdown(f"[🔗 Search Jobs for {s['title']}](https://www.google.com/search?q={s['title'].replace(' ', '+')}+jobs)")
            else:
                st.info("No matching pivot found. Try refining your input.")
