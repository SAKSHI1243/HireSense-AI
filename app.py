import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.preprocess import clean_text
from utils.skills import SKILLS
from utils.matcher import get_match_score
def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))
st.set_page_config(
    page_title="HireSense AI",
    layout="wide"
)

st.title("HireSense AI")
st.subheader("Semantic Resume Intelligence System")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    raw_text = extract_text_from_pdf(uploaded_file.name)
    cleaned_text = clean_text(raw_text)
    skills = extract_skills(cleaned_text)
    st.subheader("Extracted Resume Text")

    st.write(cleaned_text[:5000])
    st.success("Resume uploaded successfully")
    st.subheader("Extracted Skills")
    for skill in skills:
        st.success(skill)
    with st.expander("View Cleaned Text"):
         st.write(cleaned_text[:3000])   
    st.sidebar.title("HireSense AI")
    st.sidebar.write(
    "AI-powered Resume Intelligence"
    )  
    st.metric(
            "Skills Found",
            len(skills)
    )     
jd_text = st.text_area( "Paste Job Description", height=200) 
if jd_text:
    score = get_match_score(cleaned_text, jd_text)
    st.subheader("Semantic Match Score")
    st.metric("Match %", f"{score}%")
    st.progress(score / 100)  
    st.subheader("AI Match Insight")
    if score > 75: st.success("Strong Match: Candidate is highly suitable")
    elif score > 50: st.warning("Moderate Match: Some skill gaps exist")
    else: st.error("Low Match: Not a strong fit") 
    with st.expander("View Resume Text"): st.write(cleaned_text[:3000])
    with st.expander("View Job Description"): st.write(jd_text)