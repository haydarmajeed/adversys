import streamlit as st

from ui.tabs.threat_model_tab import threat_model_tab
from ui.tabs.attack_tree_tab import attack_tree_tab
from ui.tabs.mitigations_tab import mitigations_tab
from ui.tabs.dread_tab import dread_tab
from ui.tabs.test_cases_tab import test_cases_tab
from ui.tabs.copilot_tab import copilot_tab
from ui.tabs.about_tab import about_tab
from ui.tabs.rfps_tab import rfps_tab
# from ui.tabs.library_tab import library_tab

from ui.sidebar import create_sidebar
from src.utils import update_st_session_data


# Function to get user input for the application description and key details
def get_input():
    input_text = st.text_area(
        label="Describe the application to be modelled",
        placeholder="Enter your application details...",
        height=150,
        key="app_desc",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )
    st.session_state["image_analysis_content"] = input_text
    return input_text


# Main function
def main():

    selected = create_sidebar()

    # Update session state data
    update_st_session_data()

    # # Display the session data
    # print(session_data)

    if selected == "RFPs":
        rfps_tab()

    elif selected == "Threat Model":
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Threat Model", "Attack Tree", "Mitigations", "DREAD", "Test Cases"]
        )
        with tab1:
            threat_model_tab()
        with tab2:
            attack_tree_tab()
        with tab3:
            mitigations_tab()
        with tab4:
            dread_tab()
        with tab5:
            test_cases_tab()

    # elif selected == "Library":
    #     library_tab()

    elif selected == "About":
        about_tab()
    elif selected == "Copilot":
        copilot_tab()

    else:
        st.title(f"{selected} Page")
        st.write("This page is under construction.")


if __name__ == "__main__":
    main()
