import fitz  # PyMuPDF
import json
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import streamlit as st
import torch
import math

# --- Configuration ---
DEFAULT_MODEL_NAME = "google/flan-t5-base"
MAX_INPUT_TOKEN_LENGTH_FOR_CHUNK = 450 # Max tokens for a chunk fed to LLM for one question
CHUNK_TARGET_CHAR_COUNT = 2500 # Approximate character count for initial chunk selection
CHUNK_OVERLAP_CHAR_COUNT = 500 # Approximate overlap for sliding window if needed

# --- PDF to Text ---
def pdf_to_text(pdf_bytes: bytes) -> str:
    """Converts PDF bytes to raw text."""
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text", sort=True) + "\n\n" # sort=True can help with reading order
        doc.close()
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return ""
    return text.strip()

# --- LLM Information Extractor (Iterative QA) ---
class LLMInfoExtractor:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model_name = model_name
        self.tokenizer = None
        self.model_pipeline = None
        self._load_model()

    @st.cache_resource(show_spinner="Loading extraction model...")
    def _load_model(_self):
        try:
            _self.tokenizer = AutoTokenizer.from_pretrained(_self.model_name)
            _self.model_pipeline = pipeline(
                "text2text-generation",
                model=_self.model_name,
                tokenizer=_self.tokenizer,
                device=0 if torch.cuda.is_available() else -1,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32,
                max_new_tokens=150 # Max tokens for the *generated answer*
            )
            st.success(f"LLM '{_self.model_name}' loaded successfully.")
        except Exception as e:
            st.error(f"Failed to load LLM '{_self.model_name}': {e}")
            _self.model_pipeline = None

    def _truncate_text_to_token_limit(self, text: str, max_tokens: int) -> str:
        """Truncates text to fit within the specified token limit."""
        if not self.tokenizer:
            return text[:max_tokens * 5] # Fallback if tokenizer not ready

        tokens = self.tokenizer.encode(text, truncation=False, padding=False)
        if len(tokens) > max_tokens:
            truncated_tokens = tokens[:max_tokens]
            return self.tokenizer.decode(truncated_tokens, skip_special_tokens=True)
        return text

    def _get_relevant_chunks(self, full_resume_text: str, keywords: list = None, chunk_target_chars: int = CHUNK_TARGET_CHAR_COUNT, overlap_chars: int = CHUNK_OVERLAP_CHAR_COUNT) -> list[str]:
        """
        Generates chunks of text. If keywords are provided, tries to center chunks around them.
        Otherwise, creates overlapping sliding windows.
        """
        relevant_chunks = []

        if keywords:
            for keyword in keywords:
                # Case-insensitive search for keyword
                search_keyword = keyword.lower()
                text_lower = full_resume_text.lower()
                last_idx = 0
                while True:
                    match_idx = text_lower.find(search_keyword, last_idx)
                    if match_idx == -1:
                        break

                    # Define a window around the keyword
                    start_idx = max(0, match_idx - (chunk_target_chars // 2))
                    end_idx = min(len(full_resume_text), match_idx + len(keyword) + (chunk_target_chars // 2))
                    chunk = full_resume_text[start_idx:end_idx]
                    relevant_chunks.append(self._truncate_text_to_token_limit(chunk, MAX_INPUT_TOKEN_LENGTH_FOR_CHUNK))
                    last_idx = match_idx + len(keyword) # Move past current match
                if relevant_chunks: # If any keyword match found, prioritize these
                    return list(set(relevant_chunks)) # Remove duplicates

        # If no keywords provided or no matches, use sliding window
        if not relevant_chunks:
            text_len = len(full_resume_text)
            if text_len <= chunk_target_chars: # If text is short enough, use all of it
                 relevant_chunks.append(self._truncate_text_to_token_limit(full_resume_text, MAX_INPUT_TOKEN_LENGTH_FOR_CHUNK))
            else:
                step_size = chunk_target_chars - overlap_chars
                for i in range(0, text_len - overlap_chars, step_size): # ensure last chunk is also captured
                    chunk = full_resume_text[i : i + chunk_target_chars]
                    relevant_chunks.append(self._truncate_text_to_token_limit(chunk, MAX_INPUT_TOKEN_LENGTH_FOR_CHUNK))
                # Ensure the very end of the document is captured if missed by step size
                if text_len % step_size != 0 and text_len > chunk_target_chars:
                    final_chunk_start = max(0, text_len - chunk_target_chars)
                    final_chunk = full_resume_text[final_chunk_start:text_len]
                    relevant_chunks.append(self._truncate_text_to_token_limit(final_chunk, MAX_INPUT_TOKEN_LENGTH_FOR_CHUNK))


        return list(set(relevant_chunks)) # Remove duplicates

    def _construct_specific_qa_prompt(self, text_chunk: str, question: str) -> str:
        prompt = f"""
        Based ONLY on the following text snippet from a resume, answer the question.
        If the information is not present in THIS snippet, respond with "Not found in snippet".
        Be concise.

        Text Snippet:
        ---
        {text_chunk}
        ---
        Question: {question}
        Answer:
        """
        return prompt.strip()

    def _clean_llm_answer(self, raw_answer: str) -> str:
        cleaned = re.sub(r"^(Answer:|Response:|Output:)\s*", "", raw_answer, flags=re.IGNORECASE).strip()
        # Remove common "not found" variations if they are the primary response
        if re.match(r"^(not found|n/a|not present|no information|i don't know|cannot determine|not specified|not mentioned|not available|none found|unable to find)", cleaned.lower()) and len(cleaned) < 30:
            return "Not found"
        if "not found in snippet" in cleaned.lower() and len(cleaned) < 30:
            return "Not found"
        return cleaned

    def _aggregate_answers(self, answers: list, field_key: str) -> any:
        """ Aggregates answers from multiple chunks. More sophisticated logic may be needed. """
        valid_answers = [ans for ans in answers if ans.lower() != "not found" and ans.strip()]
        if not valid_answers:
            return None

        if field_key == "skills":
            all_skills = []
            for ans_str in valid_answers:
                all_skills.extend([s.strip() for s in ans_str.split(',') if s.strip()])
            return list(set(all_skills)) # Unique skills
        elif field_key == "previous_job_titles" or field_key == "previous_employers":
            combined_list = []
            for ans_str in valid_answers:
                combined_list.extend([s.strip() for s in ans_str.split(',') if s.strip()]) # Assuming comma-separated list format from LLM
            return list(set(combined_list))
        elif field_key == "education": # Expecting more structured text, return concatenated or best single answer
            # This is tricky. For now, join unique valid answers.
            # LLM might return full education entries.
            return " | ".join(list(set(valid_answers))) # Simple join, needs better parsing ideally
        else: # For single-value fields like name, email, current_job_title, total_years_experience
            # Prioritize longer, more specific answers, or the first one found.
            # This is a simple heuristic.
            valid_answers.sort(key=len, reverse=True)
            return valid_answers[0] if valid_answers else None


    def extract_info_iteratively(self, full_resume_text: str) -> dict:
        if not self.model_pipeline or not self.tokenizer:
            return {"error": "LLM or Tokenizer not loaded."}

        extracted_data = {}
        # Define questions and keywords for finding relevant text sections
        fields_to_query = {
            "name": {"question": "What is the candidate's full name?", "keywords": ["name", r"^\s*([A-Z][a-z]+)\s+([A-Z][a-z'-]+)(\s+[A-Z][a-z]+)?\s*$"]}, # Regex for typical name at start
            "email": {"question": "What is the candidate's email address?", "keywords": ["email", "@", "contact"]},
            "phone": {"question": "What is the candidate's phone number?", "keywords": ["phone", "tel", "contact", r"\(\d{3}\)\s*\d{3}-\d{4}", r"\d{3}-\d{3}-\d{4}"]},
            "linkedin": {"question": "What is the candidate's LinkedIn profile URL?", "keywords": ["linkedin.com/in/"]},
            "github": {"question": "What is the candidate's GitHub profile URL?", "keywords": ["github.com/"]},
            "summary": {"question": "Provide a brief professional summary or objective statement from the resume.", "keywords": ["summary", "objective", "profile"]},
            "current_job_title": {"question": "What is the candidate's most recent or current job title?", "keywords": ["experience", "employment", "current role", "present"]},
            "skills": {"question": "List all key technical skills, programming languages, tools, and software mentioned (as a comma-separated list).", "keywords": ["skills", "technical skills", "proficiencies", "expertise", "technologies", "languages", "tools"]},
            "education": {"question": "List all educational qualifications, including degree, institution, and graduation year/period (provide each as a distinct entry if possible).", "keywords": ["education", "academic", "degree", "university", "college", "qualification"]},
            "previous_job_titles": {"question": "List previous job titles (excluding current, as a comma-separated list).", "keywords": ["experience", "employment", "work history"]}, # Might overlap with current
            "previous_employers": {"question": "List previous employers or companies worked for (excluding current, as a comma-separated list).", "keywords": ["experience", "employment", "work history"]},
            "total_years_experience": {"question": "Based on the employment dates, estimate the total years of professional work experience. Respond with a number or a phrase like 'X years'.", "keywords": ["experience", "summary", "profile"]}
        }

        st.write("Iteratively extracting information from resume:")
        total_fields = len(fields_to_query)
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, (field_key, query_info) in enumerate(fields_to_query.items()):
            question = query_info["question"]
            keywords = query_info.get("keywords")
            status_text.text(f"Processing: {field_key.replace('_', ' ').title()}...")

            # 1. Get relevant chunks
            # For 'name', 'email', 'phone' which are often at the top, prioritize first chunk
            if field_key in ['name', 'email', 'phone', 'linkedin', 'github', 'summary']:
                 first_chunk_text = self._truncate_text_to_token_limit(full_resume_text, MAX_INPUT_TOKEN_LENGTH_FOR_CHUNK * 2) # A bit longer for intro info
                 chunks_to_process = [first_chunk_text]
            else:
                chunks_to_process = self._get_relevant_chunks(full_resume_text, keywords)

            if not chunks_to_process:
                status_text.text(f"No relevant chunks found for {field_key}. Skipping.")
                extracted_data[field_key] = None
                progress_bar.progress((i + 1) / total_fields)
                continue

            answers_for_field = []
            for chunk_idx, text_chunk in enumerate(chunks_to_process):
                # 2. Construct QA prompt
                prompt = self._construct_specific_qa_prompt(text_chunk, question)

                # 3. LLM Inference
                try:
                    raw_llm_output = self.model_pipeline(prompt) # max_new_tokens is set in pipeline init
                    answer_text = raw_llm_output[0]['generated_text']
                    cleaned_answer = self._clean_llm_answer(answer_text)
                    if cleaned_answer.lower() != "not found":
                        answers_for_field.append(cleaned_answer)
                    if field_key in ['name', 'email', 'phone', 'current_job_title', 'total_years_experience'] and cleaned_answer.lower() != "not found":
                        break # For single-value fields, often the first good answer is enough
                except Exception as e:
                    st.warning(f"LLM Error for {field_key} (chunk {chunk_idx+1}): {e}")
                    answers_for_field.append(f"LLM Error") # Store error placeholder

            # 4. Aggregate answers from multiple chunks
            extracted_data[field_key] = self._aggregate_answers(answers_for_field, field_key)
            progress_bar.progress((i + 1) / total_fields)

        status_text.text("Information extraction complete!")
        return extracted_data

# --- Helper for app.py ---
@st.cache_resource
def get_info_extractor():
    return LLMInfoExtractor()