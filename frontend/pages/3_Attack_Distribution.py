import api
import matplotlib.pyplot as plt
import requests
import streamlit as st

st.set_page_config(page_title="Attack Distribution", layout="wide")
st.title("Attack Distribution")

LABEL_COLORS = {
    "benign": "green",
    "suspicious": "orange",
    "malicious": "red",
}


@st.cache_data(ttl=300)
def load_distribution():
    return api.get_attack_distribution()


try:
    items = load_distribution()["items"]

    labels = [item["label"] for item in items]
    counts = [item["count"] for item in items]
    colors = [LABEL_COLORS.get(label, "gray") for label in labels]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        counts,
        labels=[lbl.capitalize() for lbl in labels],
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
    )
    ax.set_title("Threat Label Distribution")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Details by Label")
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        col.metric(item["label"].capitalize(), f"{item['count']:,}")
        col.caption(f"Avg {item['bytes_mean']:,.0f} B/conn")
        col.caption(f"Total {item['bytes_total']:,} B")

except requests.RequestException as e:
    st.error(f"Could not reach backend: {e}")
