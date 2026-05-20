import streamlit as st
import pandas as pd
import plotly.express as px
from utils.parser import extract_text_from_pdf
from utils.preprocess import clean_text
from utils.skills import extract_skills
from utils.matcher import get_match_score
from utils.insights import  generate_recruiter_summary
from utils.interview import generate_questions
# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="HireSense AI",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("HireSense AI")

    st.caption(
        "AI-Powered Semantic Talent Intelligence"
    )

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

    st.info(
        "Built using NLP, Sentence Transformers, "
        "and Streamlit."
    )


# -----------------------------------
# HEADER
# -----------------------------------

st.title("HireSense AI")

st.caption(
    "Semantic Resume Intelligence Platform"
)

st.markdown("---")


# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

jd_text = st.text_area(
    "Paste Job Description",
    height=200
)


# -----------------------------------
# RECRUITER INSIGHT FUNCTION
# -----------------------------------

def recruiter_insight(score, missing_skills):

    if score > 80 and len(missing_skills) <= 2:

        return """
        Strong candidate profile with high alignment
        to the job description.
        """

    elif score > 60:

        return """
        Candidate demonstrates moderate alignment
        but has some skill gaps that should be addressed.
        """

    else:

        return """
        Candidate profile shows significant gaps
        relative to the job requirements.
        """


# -----------------------------------
# MAIN PIPELINE
# -----------------------------------

if uploaded_file is not None and jd_text:

    # Save uploaded resume

    file_path = f"resumes/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract resume text

    try:

        raw_text = extract_text_from_pdf(file_path)

    except Exception as e:

        st.error(f"Error reading PDF: {e}")
        st.stop()

    # Clean text

    cleaned_text = clean_text(raw_text)

    jd_cleaned = clean_text(jd_text)

    # Extract skills

    skills = extract_skills(cleaned_text)

    jd_skills = extract_skills(jd_cleaned)

    # Semantic similarity

    score = get_match_score(
        cleaned_text,
        jd_cleaned
    )

    # Skill analysis

    matched_skills = list(
        set(skills).intersection(set(jd_skills))
    )

    missing_skills = list(
        set(jd_skills) - set(skills)
    )
    summary = generate_recruiter_summary(score,matched_skills,missing_skills)
    # Recruiter insight

    insight = recruiter_insight(
        score,
        missing_skills
    )
    st.subheader("AI Recruiter Summary")

    st.info(summary)
    if score >= 80: st.success( "Recommended for Interview")
    elif score >= 60: st.warning  ( "Potential Candidate")
    else: st.error("Low Recommendation Score")
    with st.container(): 
        st.subheader("Candidate Intelligence Report")
        st.write(summary)
    # -----------------------------------
    # TOP METRICS
    # -----------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Match Score",
            f"{score}%"
        )

    with col2:

        st.metric(
            "Matched Skills",
            len(matched_skills)
        )

    with col3:

        st.metric(
            "Missing Skills",
            len(missing_skills)
        )

    st.progress(score / 100)

    # -----------------------------------
    # MATCH STATUS
    # -----------------------------------

    if score >= 80:

        st.success(
            "Excellent Match: Candidate strongly aligns "
            "with the role."
        )

    elif score >= 60:

        st.warning(
            "Moderate Match: Candidate has partial alignment."
        )

    else:

        st.error(
            "Low Match: Candidate may not fit the role well."
        )

    st.markdown("---")

    # -----------------------------------
    # TABS
    # -----------------------------------

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

            "Category": [
                "Matched Skills",
                "Missing Skills"
            ],

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

                st.warning(
                    "No matched skills identified."
                )

        # Missing Skills

        with col2:

            st.subheader("Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.error(f"✘ {skill}")

            else:

                st.success(
                    "No major skill gaps found."
                )

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

