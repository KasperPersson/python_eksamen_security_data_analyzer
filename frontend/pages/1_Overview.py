import api
import requests
import streamlit as st

st.set_page_config(page_title="Overview", layout="wide")
st.title("Dataset Overview")


@st.cache_data(ttl=300)
def load_overview():
    return api.get_overview()


try:
    data = load_overview()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Log Entries", f"{data['total_rows']:,}")
    col2.metric("Start", data["start_time"][:10])
    col3.metric("End", data["end_time"][:10])

    st.subheader("Threat Label Distribution")
    total = data["total_rows"]
    for label, count in data["label_counts"].items():
        pct = count / total * 100
        st.write(f"**{label.capitalize()}**: {count:,} ({pct:.1f}%)")

    st.subheader("Bytes Transferred")
    col4, col5, col6 = st.columns(3)
    col4.metric("Mean", f"{data['bytes_mean']:,.0f} B")
    col5.metric("Min", f"{data['bytes_min']:,} B")
    col6.metric("Max", f"{data['bytes_max']:,} B")

except requests.RequestException as e:
    st.error(f"Could not reach backend: {e}")
