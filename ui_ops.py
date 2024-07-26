import streamlit as st
from query_data import query_rag

class UIOps:
    def __init__(self):
        self.chroma_db = None

    def handle_text_submission(self, text, chat_history):
        user_input = text
        chat_history += f"User: {user_input}\n"
        session_data = {
            "image_analysis_content": st.session_state['image_analysis_content'],
            "attack_tree": st.session_state['attack_tree'],
            "app_type": st.session_state['app_type2'],
            "sensitive_data": st.session_state['sensitive_data2'],
            "internet_facing": st.session_state['internet_facing2'],
            "authentication": st.session_state['authentication2'],
            "threat_model": st.session_state['threat_model'],
            "mitigations": st.session_state['mitigations'],
            "dread_assessment": st.session_state['dread_assessment'],
            "test_cases": st.session_state['test_cases']
        }

        print("FIRST SESSION DATA ------------------------------------------------------")
        print("image_analysis_content", st.session_state['image_analysis_content'])
        print("app_type", st.session_state['app_type2'])
        print("sensitive_data", st.session_state['sensitive_data2'])
        print("internet_facing", st.session_state['internet_facing2'])
        print("authentication", st.session_state['authentication2'])
        print("threat_model", st.session_state['threat_model'])
        print("mitigations", st.session_state['mitigations'])
        print("dread_assessment", st.session_state['dread_assessment'])
        print("test_cases", st.session_state['test_cases'])
        print("END OF FIRST SESSION DATA ------------------------------------------------------")

        result = query_rag(user_input, chat_history, session_data, fetch_context=False, chroma_db=self.chroma_db, route=None)
        result = result.content
        chat_history += f"Bot: {result}\n"
        
        return result, chat_history
