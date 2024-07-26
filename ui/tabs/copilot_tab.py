import streamlit as st
from ui_ops import UIOps
from db_ops import add_data

def copilot_tab():
    st.title("Copilot Page")

    # Chats section
    st.subheader("Chats")
    if "history" not in st.session_state:
        st.session_state.history = []

    st.text("(Chat list would appear here)")
    st.markdown("---")  # Add a horizontal rule for separation

    # Chatbox section
    st.subheader("Chatbox")

    # Display chat history
    chat_history_container = st.container()
    with chat_history_container:
        for speaker, message in st.session_state.history:
            st.markdown(f"**{speaker}**: {message}")

    # Chat input and send button
    chat_input = st.text_input("Send a message...", key="chat_input")
    send_button = st.button("Send", key="send_button")
    
    ui_ops = UIOps()
    
    if send_button and chat_input:
        history_text = "\n".join([f"{speaker}: {message}" for speaker, message in st.session_state.history])
        result, updated_history = ui_ops.handle_text_submission(chat_input, history_text)
        
        st.session_state.history.append(("User", chat_input))
        st.session_state.history.append(("Bot", result))

        # Update chat history
        with chat_history_container:
            st.markdown(f"**User**: {chat_input}")
            st.markdown(f"**Bot**: {result}")
    st.markdown("---")  # Add a horizontal rule for separation

    # Local Docs section
    st.subheader("Local Docs")
    uploaded_file = st.file_uploader("Add Docs")
    if uploaded_file:
        add_data(uploaded_file)
        st.success("Document added successfully")
        st.text("Select a collection to make it available to the chat model")