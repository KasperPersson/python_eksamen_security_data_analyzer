import api
import matplotlib.pyplot as plt
import requests
import streamlit as st

st.set_page_config(page_title="Top IPs", layout="wide")
st.title("Top Source IPs")


@st.cache_data(ttl=300)
def load_top_ips(n):
    return api.get_top_ips(n)


n = st.slider("Number of IPs to show", min_value=5, max_value=25, value=10)

try:
    items = load_top_ips(n)["items"]

    ips = [item["ip"] for item in items]
    counts = [item["count"] for item in items]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(ips[::-1], counts[::-1], color="blue")
    ax.set_xlabel("Connection Count")
    ax.set_title(f"Top {n} Source IPs by Connection Frequency")
    ax.bar_label(bars, padding=4, fmt="%d")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

except requests.RequestException as e:
    st.error(f"Could not reach backend: {e}")
