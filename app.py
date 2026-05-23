import streamlit as st
import pandas as pd
import plotly.express as px
from utils.parser import extract_text_from_pdf
from utils.preprocess import clean_text
from utils.skills import extract_skills
from utils.matcher import get_match_score
from utils.insights import  generate_recruiter_summary
from utils.interview import generate_questions
import nltk
try:
    from nltk.corpus import stopwords
    stop_words = set(
        stopwords.words("english")
    )
except LookupError:
    nltk.download("stopwords")
    from nltk.corpus import stopwords
    stop_words = set(
        stopwords.words("english")
    )
st.set_page_config( page_title="HireSense AI", page_icon="📄",layout="wide")
with st.sidebar:
    st.title("HireSense AI")
    st.caption("AI-Powered Semantic Talent Intelligence")
    st.divider()
    st.markdown("""
    ### Features

    ✔ Semantic Resume Matching  
    ✔ Skill Gap Analysis  
    ✔ Recruiter Insights  
    ✔ Resume Intelligence  
    ✔ NLP + Embedding Pipeline  
    """)

    st.divider()

    st.info(  "Built using NLP, Sentence Transformers, " "and Streamlit.")

st.title("HireSense AI")

st.caption("Semantic Resume Intelligence Platform")

st.markdown("---")

with st.form("resume_form"):

    uploaded_file = st.file_uploader( "Upload Resume PDF", type=["pdf"])
    jd_text = st.text_area("Paste Job Description",height=200)
    submit_button = st.form_submit_button("Analyze Resume")
    if submit_button:
        if not uploaded_file or not jd_text:    
            st.warning("Please upload resume and job description.")
            st.stop()
def recruiter_insight(

    final_score,
    skill_score,
    missing_skills

):

    if skill_score >= 75 and len(missing_skills) <= 2:

        return """
        Candidate demonstrates strong technical alignment
        with the job requirements and possesses most
        of the core required skills.
        """

    elif final_score >= 55:

        return """
        Candidate shows moderate compatibility with
        the role but may require improvement in
        certain technical areas.
        """

    else:

        return """
        Candidate profile currently lacks sufficient
        alignment with the role requirements.
        """

if submit_button and uploaded_file is not None and jd_text:
 with st.spinner( "Analyzing candidate compatibility..."):
    file_path = f"resumes/{uploaded_file.name}"
    with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
    try:
        raw_text = extract_text_from_pdf(file_path)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        st.stop()
    cleaned_text = clean_text(raw_text)
    jd_cleaned = clean_text(jd_text)
    skills = extract_skills(cleaned_text)
    jd_skills = extract_skills(jd_cleaned)
    # Semantic similarity
    semantic_score = get_match_score(cleaned_text,jd_cleaned)
    # Skill analysis
    matched_skills = list(set(skills).intersection(set(jd_skills)))
    if len(jd_skills) > 0: skill_score = (len(matched_skills)/ len(jd_skills)) * 100
    else: skill_score = 0
    missing_skills = list(set(jd_skills) - set(skills))
    jd_keywords = jd_cleaned.split()
    jd_keywords = list(set(jd_keywords))
    jd_keywords = [
        word for word in jd_keywords
        if len(word) > 3]
    jd_keywords = [
    word for word in jd_keywords
    if word not in stop_words]
    keyword_matches = sum(
    1 for word in jd_keywords
    if word in cleaned_text)
    if len(jd_keywords) > 0:keyword_score = ( keyword_matches / len(jd_keywords) ) * 100
    else:keyword_score = 0
    semantic_score = semantic_score * 1.3
    semantic_score = min(semantic_score,100)
    final_score = round((skill_score * 0.6) +(semantic_score * 0.3) +(keyword_score * 0.1),2)
    if final_score >= 80: st.success( "Recommended for Interview")
    elif final_score >= 60: st.warning  ( "Potential Candidate")
    else: st.error("Low Recommendation Score")
    summary = recruiter_insight(
    final_score,
    skill_score,
    missing_skills)
    insight = recruiter_insight(
    final_score,
    skill_score,
    missing_skills)
    with st.container(): 
        st.subheader("Candidate Intelligence Report")
        st.write(summary)
  
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("ATS Score",f"{round(final_score)}%")
    with col2: st.metric("Skill Match",   f"{round(skill_score)}%")
    with col3:  st.metric("Semantic Match", f"{round(semantic_score)}%")
    with col4:   st.metric("Keyword Match",f"{round(keyword_score)}%")
    st.progress(final_score / 100)
    # MATCH STATUS
    if final_score >= 80: st.success( "Excellent Match: Candidate strongly aligns with the role." )
    elif final_score >= 60:st.warning("Moderate Match: Candidate has partial alignment.")
    else:st.error(   "Low Match: Candidate may not fit the role well.")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Analysis",
        "Skills",
        "Resume Data",
        "Interview Questions"
    ])

    # -----------------------------------
    # TAB 1 — ANALYSIS
    # -----------------------------------

    with tab1:
        st.subheader("Recruiter Insight")
        st.info(insight)
        st.markdown("---")
        # Chart
        chart_data = pd.DataFrame({
            "Category": [ "Matched Skills","Missing Skills"],
            "Count": [
                len(matched_skills),
                len(missing_skills)
            ]
        })
        fig = px.pie(
            chart_data,
            names="Category",
            values="Count",
            title="Skill Match Distribution"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    # -----------------------------------
    # TAB 2 — SKILLS
    # -----------------------------------
    with tab2:
        col1, col2 = st.columns(2)
        # Matched Skills
        with col1:
            st.subheader("Matched Skills")
            if matched_skills:
                for skill in matched_skills:
                    st.success(f"✔ {skill}")
            else:
                st.warning(   "No matched skills identified.")
        # Missing Skills
        with col2:
            st.subheader("Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.error(f"✘ {skill}")
            else:
                st.success(   "No major skill gaps found.")
    # -----------------------------------
    # TAB 3 — RESUME DATA
    # -----------------------------------
    with tab3:
        with st.expander("View Extracted Resume Text"):
            st.write(cleaned_text[:5000])
        with st.expander("View Job Description"):
            st.write(jd_text)
    with tab4:
        st.subheader("generated Interview Questions")
        questions = generate_questions( matched_skills)
        for question in questions: st.info(question)
    # -----------------------------------
    # FOOTER
    # -----------------------------------
    st.markdown("---")
    st.caption(
        "Built with NLP, Sentence Transformers, "
        "and Streamlit"
    )
else:
    st.info(
        "Upload a resume and paste a job description "
        "to begin semantic analysis."
    )