import api
import requests
import streamlit as st

st.set_page_config(page_title="Chat", layout="wide")
st.title("Chat with the Data")
st.write(
    "Ask follow-up questions about the dataset. "
    "The AI has access to the full dataset summary and remembers the conversation."
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if st.button("Clear chat", type="secondary"):
    st.session_state["chat_history"] = []
    st.rerun()

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something about the security logs..."):
    st.session_state["chat_history"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = api.post_chat(prompt, st.session_state["chat_history"][:-1])
                st.markdown(reply)
                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": reply}
                )
            except requests.RequestException as e:
                st.error(f"Could not reach backend: {e}")
