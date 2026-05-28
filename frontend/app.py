import streamlit as st

st.set_page_config(
    page_title="Security Data Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(":rainbow[Security Data Analyzer]")
st.write(
    "A cybersecurity application that lets you explore ~6 million network log entries "
    "from a real dataset.  \n"
    "Use it to analyze threat patterns, suspicious IP's  \n"
    "Or use the AI function to generate an assesment and chat about the data "
)
st.info("Select a page from the sidebar to begin.")
