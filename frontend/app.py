import streamlit as st

st.set_page_config(
    page_title="Security Data Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Security Data Analyzer")
st.write(
    "A cybersecurity log analysis tool. "
    "Navigate using the sidebar to explore threat patterns in the dataset."
)
st.info("Select a page from the sidebar to begin.")
