import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.preprocess import clean_text
from utils.skills import SKILLS
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

    raw_text = extract_text_from_pdf(
    uploaded_file.name
)
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