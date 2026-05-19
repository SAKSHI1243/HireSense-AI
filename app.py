import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.preprocess import clean_text
from utils.skills import extract_skills
from utils.matcher import get_match_score

st.set_page_config(
    page_title="HireSense AI",
    layout="wide"
)
st.title("HireSense AI")
st.markdown("---")
st.subheader("Candidate Compatibility Analysis")
st.sidebar.title("HireSense AI")
st.sidebar.write("AI-powered Resume Intelligence")  
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)
st.markdown("---")
def recruiter_insight(score, missing_skills):

    if score > 80 and len(missing_skills) <= 2:

        return """
        Strong candidate profile with high alignment
        to the job description.
        """

    elif score > 60:

        return """
        Candidate shows moderate alignment but
        requires improvement in some areas.
        """

    else:

        return """
        Candidate profile has significant gaps
        for this role.
        """
if uploaded_file is not None:

    file_path = f"resumes/{uploaded_file.name}"

    with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())

    try:raw_text = extract_text_from_pdf(file_path)
    except Exception as e: 
        st.error(f"Error reading PDF: {e}")
        st.stop()
    cleaned_text = clean_text(raw_text)
    skills = extract_skills(cleaned_text)
    with st.expander("View Extracted Resume Text"): st.write(cleaned_text[:3000])
    st.success("Resume uploaded successfully")
    st.subheader("Extracted Skills")
    st.write(", ".join(skills))
    with st.expander("View Cleaned Text"):
         st.write(cleaned_text[:3000])   
    
    st.metric(
            "Skills Found",
            len(skills)
    )     
jd_text = st.text_area( "Paste Job Description", height=200) 
if uploaded_file is not None and jd_text:
    score = get_match_score(cleaned_text, jd_text)
    jd_cleaned = clean_text(jd_text)
    jd_skills = extract_skills(jd_cleaned)
    matched_skills = list(set(skills).intersection(set(jd_skills)))
    st.subheader("Matched Skills")
    if matched_skills:  st.write(", ".join(matched_skills))
    else: st.warning("No matched skills found")
    missing_skills = list(set(jd_skills) - set(skills))
    st.subheader("Missing Skills")
    if missing_skills:  st.write(", ".join(missing_skills))
    else: st.success("No major skill gaps found")
    st.subheader("Semantic Match Score")
    col1, col2 = st.columns(2)
    with col1: st.metric("Match Score", f"{score}%")
    with col2:st.metric( "Matched Skills", len(matched_skills))
    st.progress(score / 100)  
    st.subheader("Candidate Fit Assessment")
    if score > 75: st.success("Strong Match: Candidate is highly suitable")
    elif score > 50: st.warning("Moderate Match: Some skill gaps exist")
    else: st.error("Low Match: Not a strong fit") 
    
    st.subheader("Recruiter Insight")
    insight = recruiter_insight(score, missing_skills)
    st.info(insight)    

    with st.expander("View Resume Text"): st.write(cleaned_text[:3000])
    with st.expander("View Job Description"): st.write(jd_text)


