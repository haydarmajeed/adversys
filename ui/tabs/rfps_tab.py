import streamlit as st
from src.ui_ops import UIOps
from src.db_ops import add_data


def rfps_tab():
    st.title("RFPs Page")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.subheader("Chats")
        if "rfp_history" not in st.session_state:
            st.session_state.rfp_history = []

        new_chat_button = st.button("+ New Chat")
        if new_chat_button:
            st.session_state.rfp_history.append([])
            st.session_state.current_chat_index = len(st.session_state.rfp_history) - 1

        for i, chat in enumerate(st.session_state.rfp_history):
            if st.button(f"Chat {i+1}", key=f"chat_{i}"):
                st.session_state.current_chat_index = i

        st.text("(Chat list appears above)")

    with col2:
        st.subheader("Chatbox")

        # Display current chat history
        chat_history_container = st.container()
        with chat_history_container:
            if "current_chat_index" in st.session_state:
                current_chat = st.session_state.rfp_history[
                    st.session_state.current_chat_index
                ]
                for speaker, message in current_chat:
                    st.markdown(f"**{speaker}**: {message}")

        # Chat input and send button
        chat_input = st.text_input("Send a message...", key="rfp_chat_input")
        send_button = st.button("Send", key="rfp_send_button")

        if send_button and chat_input:
            if "current_chat_index" not in st.session_state:
                st.session_state.current_chat_index = 0
                st.session_state.rfp_history.append([])

            current_chat = st.session_state.rfp_history[
                st.session_state.current_chat_index
            ]
            history_text = "\n".join(
                [f"{speaker}: {message}" for speaker, message in current_chat]
            )
            ui_ops = UIOps()
            result, updated_history = ui_ops.handle_text_submission(
                chat_input, history_text
            )

            current_chat.append(("User", chat_input))
            current_chat.append(("Bot", result))

            # Update chat history
            with chat_history_container:
                st.markdown(f"**User**: {chat_input}")
                st.markdown(f"**Bot**: {result}")

    with col3:
        st.subheader("Local Docs")
        uploaded_file = st.file_uploader("+ Add Docs", key="rfp_file_uploader")
        if uploaded_file:
            add_data(uploaded_file)
            st.success("Document added successfully")
        st.text("Select a collection to make it available to the chat model")
