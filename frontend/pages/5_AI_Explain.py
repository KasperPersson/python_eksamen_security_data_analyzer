import api
import requests
import streamlit as st

st.set_page_config(page_title="AI Assessment", layout="wide")
st.title("AI Security Assessment")
st.write(
    "Click the button to get a security analysis of the dataset. "
    "The AI uses real numbers from the logs in its answer."
)

if "explanation" not in st.session_state:
    st.session_state["explanation"] = None

if st.button("Generate Assessment", type="primary"):
    with st.spinner("Analyzing dataset - this may take a few seconds..."):
        try:
            st.session_state["explanation"] = api.post_explain()
        except requests.RequestException as e:
            st.error(f"Could not reach backend: {e}")

if st.session_state["explanation"]:
    st.divider()
    st.markdown(st.session_state["explanation"])
