import streamlit as st
from utils.parser import extract_text_from_pdf

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

    extracted_text = extract_text_from_pdf(
        uploaded_file.name
    )

    st.subheader("Extracted Resume Text")

    st.write(extracted_text[:5000])