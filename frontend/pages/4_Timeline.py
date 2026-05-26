import api
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Timeline", layout="wide")
st.title("Activity Timeline")


@st.cache_data(ttl=300)
def load_timeline(interval):
    return api.get_timeline(interval)


interval = st.selectbox("Aggregation interval", options=["day", "hour"], index=0)

try:
    data = load_timeline(interval)
    items = data["items"]

    times = pd.to_datetime([item["time"] for item in items])
    counts = [item["count"] for item in items]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(times, counts, color="blue", linewidth=1.5)
    ax.fill_between(times, counts, alpha=0.15, color="blue")
    ax.set_xlabel("Time")
    ax.set_ylabel("Log Entries")
    ax.set_title(f"Network Activity Over Time ({interval}ly aggregation)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(f"{len(items):,} data points  |  {sum(counts):,} total log entries")

except requests.RequestException as e:
    st.error(f"Could not reach backend: {e}")
