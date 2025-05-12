# resume_parser.py
import fitz  # PyMuPDF
import re
from collections import Counter  # Not used in current version, but can be useful for advanced skill counting


def pdf_to_text(uploaded_file_object):
    """Converts a PDF file object to text."""
    try:
        # uploaded_file_object is Streamlit's UploadedFile, which has a read() method
        pdf_document = fitz.open(stream=uploaded_file_object.getvalue(), filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        pdf_document.close()
        return text
    except Exception as e:
        print(f"Error converting PDF to text: {e}")
        return None


def extract_sections(text):
    """
    Tries to identify common resume sections and their content.
    Returns a dictionary like {'Experience': 'text content', 'Skills': 'text content'}
    """
    sections = {}
    section_keywords = [
        "summary", "objective", "profile",
        "experience", "work experience", "professional experience", "employment history",
        "education", "academic background",
        "skills", "technical skills", "proficiencies", "competencies",
        "projects", "personal projects",
        "certifications", "licenses",
        "awards", "honors",
        "publications",
        "references"
    ]
    pattern_parts = []
    for keyword in section_keywords:
        # Build regex without backslashes inside f-string
        escaped_kw = keyword.replace(" ", r"\s+")
        pattern = (
            r"^(?:\s*[-*•]?\s*)(" + escaped_kw + r")(?:\s*:|\s*\n)"
        )
        pattern_parts.append(pattern)
    regex_pattern = re.compile("|".join(pattern_parts), re.IGNORECASE | re.MULTILINE)

    last_match_end = 0
    current_section_title_key = None
    matches = list(regex_pattern.finditer(text))

    for i, match in enumerate(matches):
        section_title_found = next(s for s in match.groups() if s is not None).lower().strip()
        # Normalize common variations
        normalized_title = section_title_found
        if "experience" in section_title_found or "employment" in section_title_found:
            normalized_title = "Experience"
        elif "skill" in section_title_found or "proficienc" in section_title_found or "competen" in section_title_found:
            normalized_title = "Skills"
        elif "education" in section_title_found or "academic" in section_title_found:
            normalized_title = "Education"
        elif "summary" in section_title_found or "profile" in section_title_found or "objective" in section_title_found:
            normalized_title = "Summary"
        elif "project" in section_title_found:
            normalized_title = "Projects"
        else:
            normalized_title = section_title_found.capitalize()

        if current_section_title_key and last_match_end < match.start():
            content = text[last_match_end:match.start()].strip()
            if current_section_title_key in sections:
                sections[current_section_title_key] += "\n" + content
            else:
                sections[current_section_title_key] = content
        current_section_title_key = normalized_title
        last_match_end = match.end()

    if current_section_title_key and last_match_end < len(text):
        content = text[last_match_end:].strip()
        if current_section_title_key in sections:
            sections[current_section_title_key] += "\n" + content
        else:
            sections[current_section_title_key] = content
    
    if not sections and text:
        # Fallback if no sections detected
        sections["Experience"] = text

    return sections


def extract_job_entries(experience_text):
    """
    Extracts job titles, companies, dates, and descriptions from experience text.
    Returns a list of dictionaries. Assumes reverse chronological order.
    """
    if not experience_text:
        return []

    entries = []
    # Split and parse logic omitted for brevity
    # ... (rest of function unchanged) ...
    return entries


def extract_skills(skills_text):
    if not skills_text:
        return []
    # ... (rest of function unchanged) ...
    return []


def parse_resume_data(uploaded_file_object):
    """
    Main parsing function.
    Returns a dictionary with 'most_recent_job', 'all_jobs', 'skills', 'summary'.
    """
    text = pdf_to_text(uploaded_file_object)
    if not text:
        return {"error": "Could not read text from PDF."}

    sections = extract_sections(text)
    parsed_data = {
        "most_recent_job": None,
        "all_jobs": [],
        "skills": [],
        "summary": sections.get("Summary", sections.get("Profile", sections.get("Objective", ""))),
        "full_text": text
    }
    # Parsing logic unchanged
    return parsed_data
