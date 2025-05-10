import streamlit as st
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json # For displaying extracted info and editing

# Import from our new module
from resume_parser import pdf_to_text, get_info_extractor

# --- Load existing FuturePaths data and models (same as before) ---
@st.cache_data
def load_data_cleaned(path="data/final_cleaned_data.csv"):
    return pd.read_csv(path)

@st.cache_data
def load_job_skills_data(path="data/job_skills_tfidf.csv"):
    df = pd.read_csv(path)
    df['Skills_String'] = df['Skills_TFIDF'].astype(str) # Ensure 'Skills_TFIDF' is treated as a string
    return df

@st.cache_resource
def load_tfidf_vectorizer(path="data/tfidf_vectorizer.pkl"):
    with open(path, 'rb') as f:
        return pickle.load(f)

data_cleaned = load_data_cleaned()
job_skills_data = load_job_skills_data()
tfidf_vectorizer_skills = load_tfidf_vectorizer() # Assuming this vectorizer is for skills

# --- Core Suggestion Logic (same as before) ---
def get_career_suggestions_from_title(current_job_title, data, top_n=10):
    if not current_job_title or not isinstance(current_job_title, str):
        return pd.Series(dtype='float64')
    # Simple cleaning for job title matching
    current_job_title_cleaned = current_job_title.strip().lower()
    data['Current Job Title Cleaned'] = data['Current Job Title'].astype(str).str.strip().str.lower()

    if current_job_title_cleaned in data['Current Job Title Cleaned'].values:
        # Use original casing for display if desired, or stick to cleaned
        original_title_matches = data[data['Current Job Title Cleaned'] == current_job_title_cleaned]['Current Job Title'].unique()
        # For simplicity, take the first original match if multiple exist, or use cleaned title
        title_to_filter = original_title_matches[0] if len(original_title_matches) > 0 else current_job_title_cleaned

        next_roles = data[data['Current Job Title Cleaned'] == title_to_filter]['Next Job Title'].value_counts(normalize=True)
        return next_roles.head(top_n) * 100
    return pd.Series(dtype='float64')


def get_career_suggestions_with_skills(user_skills_list, job_skills_df, vectorizer, top_n=10):
    if not user_skills_list or not isinstance(user_skills_list, list) or not all(isinstance(s, str) for s in user_skills_list):
        st.warning("No valid skills provided for skill-based matching.")
        return pd.Series(dtype='float64')

    user_skills_text = ", ".join(user_skills_list)
    if not user_skills_text.strip():
        st.warning("Skills text is empty after joining.")
        return pd.Series(dtype='float64')

    try:
        # Assuming vectorizer is already fit on job_skills_df['Skills_String']
        # And job_skills_df has 'Job Title' and 'Skills_String'
        job_skills_matrix = vectorizer.transform(job_skills_df['Skills_String'])
        user_skill_vector = vectorizer.transform([user_skills_text])
        cosine_similarities = cosine_similarity(user_skill_vector, job_skills_matrix).flatten()

        actual_top_n = min(top_n, len(cosine_similarities))
        similar_indices = cosine_similarities.argsort()[:-actual_top_n-1:-1]

        results = []
        for i in similar_indices:
            if i < len(job_skills_df):
                job_title = job_skills_df['Job Title'].iloc[i]
                similarity_score = cosine_similarities[i]
                results.append({'Job Title': job_title, 'Similarity': similarity_score * 100})

        if not results:
            return pd.Series(dtype='float64')
        return pd.DataFrame(results).set_index('Job Title')['Similarity']

    except Exception as e:
        st.error(f"Error in skill-based suggestion: {e}")
        return pd.Series(dtype='float64')

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🚀 futurePaths: AI Career Navigator")
st.markdown("Upload your PDF resume or enter your job title to get career path suggestions.")

# Initialize session state
if 'extracted_resume_info' not in st.session_state:
    st.session_state.extracted_resume_info = None
if 'suggestions_df' not in st.session_state:
    st.session_state.suggestions_df = None
if 'skill_suggestions_df' not in st.session_state:
    st.session_state.skill_suggestions_df = None
if 'current_job_title_input' not in st.session_state:
    st.session_state.current_job_title_input = ""
if 'extracted_skills_list' not in st.session_state:
    st.session_state.extracted_skills_list = []


input_method = st.radio("Choose input method:", ("Upload PDF Resume", "Enter Job Title Manually"), horizontal=True, key="input_method_selector")
st.markdown("---")

if input_method == "Upload PDF Resume":
    uploaded_file = st.file_uploader("Upload your PDF resume", type="pdf", key="pdf_uploader")
    if uploaded_file is not None:
        # Process only if it's a new file or if info not already extracted
        if st.session_state.extracted_resume_info is None or getattr(uploaded_file, '_streamlit_uploaded_file_id', '') != st.session_state.get('last_uploaded_file_id', None):
            st.session_state.last_uploaded_file_id = getattr(uploaded_file, '_streamlit_uploaded_file_id', '')

            with st.spinner("Processing resume with AI... This may take a few minutes for long resumes."):
                pdf_bytes = uploaded_file.getvalue()
                resume_text = pdf_to_text(pdf_bytes)

                if resume_text:
                    with st.expander("View Raw Extracted Text (First 1000 Chars)", expanded=False):
                        st.text_area("", resume_text[:1000] + "...", height=150, disabled=True, key="raw_text_display")

                    info_extractor = get_info_extractor() # Gets cached extractor
                    if info_extractor.model_pipeline:
                        st.session_state.extracted_resume_info = info_extractor.extract_info_iteratively(resume_text)
                        # Populate editable fields from newly extracted info
                        if st.session_state.extracted_resume_info and "error" not in st.session_state.extracted_resume_info:
                            st.session_state.current_job_title_input = st.session_state.extracted_resume_info.get("current_job_title", "")
                            skills = st.session_state.extracted_resume_info.get("skills", [])
                            st.session_state.extracted_skills_list = skills if isinstance(skills, list) else [str(skills)] if skills else []
                        else:
                            st.session_state.current_job_title_input = ""
                            st.session_state.extracted_skills_list = []
                    else:
                        st.error("Information extraction model could not be loaded. Please check logs.")
                        st.session_state.extracted_resume_info = {"error": "Model not loaded"}
                else:
                    st.warning("Could not extract text from the PDF.")
                    st.session_state.extracted_resume_info = None
                    st.session_state.current_job_title_input = ""
                    st.session_state.extracted_skills_list = []

    # Display and allow editing of extracted information
    if st.session_state.extracted_resume_info and "error" not in st.session_state.extracted_resume_info:
        st.subheader("📄 Extracted Resume Information (Editable)")
        st.info("AI extraction may not be perfect. Please verify and edit the details below.")

        # Make primary fields directly editable
        st.session_state.current_job_title_input = st.text_input(
            "Current Job Title",
            value=st.session_state.current_job_title_input,
            key="resume_job_title_edit"
        )
        skills_text_area = st.text_area(
            "Skills (comma-separated)",
            value=", ".join(st.session_state.extracted_skills_list), # Join list for display
            key="resume_skills_edit"
        )
        st.session_state.extracted_skills_list = [s.strip() for s in skills_text_area.split(',') if s.strip()]


        with st.expander("View/Edit All Extracted Details (JSON Format)", expanded=False):
            try:
                # Make sure all keys are present even if None from extraction
                all_expected_keys = ["name", "email", "phone", "linkedin", "github", "summary", "current_job_title", "skills", "education", "previous_job_titles", "previous_employers", "total_years_experience"]
                display_info = {key: st.session_state.extracted_resume_info.get(key) for key in all_expected_keys}

                edited_json_str = st.text_area("Raw Extracted JSON (Editable)",
                                               value=json.dumps(display_info, indent=2),
                                               height=350, key="json_edit_area")
                # Update session state with edits from JSON
                try:
                    updated_info = json.loads(edited_json_str)
                    st.session_state.extracted_resume_info.update(updated_info) # Update existing dict
                    # Re-populate primary fields from potentially edited JSON
                    st.session_state.current_job_title_input = st.session_state.extracted_resume_info.get("current_job_title", "")
                    skills_from_json = st.session_state.extracted_resume_info.get("skills", [])
                    st.session_state.extracted_skills_list = skills_from_json if isinstance(skills_from_json, list) else [str(skills_from_json)] if skills_from_json else []

                except json.JSONDecodeError:
                    st.error("Invalid JSON format in the edited details. Please correct it.")
            except Exception as e:
                st.error(f"Error displaying/updating JSON details: {e}")

    elif st.session_state.extracted_resume_info and "error" in st.session_state.extracted_resume_info:
        st.error(f"Could not extract information: {st.session_state.extracted_resume_info.get('error')}")

elif input_method == "Enter Job Title Manually":
    unique_job_titles = [""] + sorted(data_cleaned['Current Job Title'].astype(str).unique().tolist())
    st.session_state.current_job_title_input = st.selectbox(
        "Select or type your current job title:",
        options=unique_job_titles,
        index=unique_job_titles.index(st.session_state.current_job_title_input) if st.session_state.current_job_title_input in unique_job_titles else 0,
        key="manual_job_title_select"
    )
    if not st.session_state.current_job_title_input:
         st.session_state.current_job_title_input = st.text_input("Or enter your job title if not in list:", value=st.session_state.current_job_title_input, key="manual_job_title_text")

    skills_manual_input = st.text_area("Optionally, enter your key skills (comma-separated):",
                                       value=", ".join(st.session_state.extracted_skills_list), # Use session state
                                       help="This will help in skill-based recommendations.",
                                       key="manual_skills_input")
    st.session_state.extracted_skills_list = [s.strip() for s in skills_manual_input.split(',') if s.strip()]

st.markdown("---")

# --- Generate and Display Suggestions ---
if st.button("✨ Get Career Suggestions", type="primary", use_container_width=True,
             disabled=not bool(st.session_state.current_job_title_input), key="get_suggestions_button"):
    if st.session_state.current_job_title_input:
        st.session_state.suggestions_df = get_career_suggestions_from_title(st.session_state.current_job_title_input, data_cleaned)

        if st.session_state.extracted_skills_list:
            st.session_state.skill_suggestions_df = get_career_suggestions_with_skills(
                st.session_state.extracted_skills_list,
                job_skills_data,
                tfidf_vectorizer_skills
            )
        else:
            st.session_state.skill_suggestions_df = None
    else:
        st.warning("Please upload a resume or enter a job title.")
        st.session_state.suggestions_df = None
        st.session_state.skill_suggestions_df = None

# Display results
if st.session_state.suggestions_df is not None or st.session_state.skill_suggestions_df is not None:
    st.subheader("💡 Suggested Next Career Paths")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Based on Your Job Title:")
        if st.session_state.suggestions_df is not None and not st.session_state.suggestions_df.empty:
            display_df_title = st.session_state.suggestions_df.reset_index()
            display_df_title.columns = ['Suggested Role', 'Transition Likelihood (%)']
            st.dataframe(display_df_title.style.format({"Transition Likelihood (%)": "{:.2f}%"}), use_container_width=True)
        elif st.session_state.current_job_title_input:
            st.info(f"No direct career path data found for '{st.session_state.current_job_title_input}'. Try a broader title or check skill-based suggestions.")
        else:
            st.info("Enter a job title to see title-based suggestions.")

    with col2:
        st.markdown("#### Based on Your Skills:")
        if st.session_state.skill_suggestions_df is not None and not st.session_state.skill_suggestions_df.empty:
            display_df_skill = st.session_state.skill_suggestions_df.reset_index()
            display_df_skill.columns = ['Suggested Role', 'Skill Match (%)']
            st.dataframe(display_df_skill.style.format({"Skill Match (%)": "{:.2f}%"}), use_container_width=True)
        elif st.session_state.extracted_skills_list:
            st.info(f"No specific skill-based matches found for your skills. The TF-IDF model might not have enough similar skill profiles, or skill terms might differ.")
        else:
            st.info("Upload a resume with skills or enter skills manually for skill-based suggestions.")

st.markdown("---")
st.markdown("Powered by Streamlit, Pandas, Scikit-learn, and Hugging Face Transformers. Original concept by Jakolo6.")