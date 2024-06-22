import streamlit as st
import requests
import shelve

st.title("CBU CHART-BOT")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = load_chat_history()

# Sidebar with a button to delete chat history and contact information
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state["messages"] = []
        save_chat_history([])

    with st.expander("Developers"):
        st.markdown("- Future")
        st.markdown("- Kundananji")
        st.markdown("- Lubinda")
        st.markdown("- Lawrence")
        st.markdown("- Emmanuel")

# Display chat messages
for message in st.session_state["messages"]:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()

        # Send prompt to Flask API
        try:
            response = requests.post("http://localhost:5000/chat", json={"prompt": prompt})
            response.raise_for_status()
            full_response = response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            full_response = f"Error: {e}"

        message_placeholder.markdown(full_response)
        st.session_state["messages"].append({"role": "assistant", "content": full_response})

    # Save chat history after each interaction
    save_chat_history(st.session_state["messages"])
