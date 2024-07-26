import os
import streamlit as st
from streamlit_option_menu import option_menu


def create_sidebar():
    # Get the absolute path of the logo
    current_dir = os.path.dirname(__file__)
    logo_path = os.path.join(current_dir, "..", "static", "logo.png")

    with st.sidebar:
        st.title("Adversarial Systems")
        st.caption("AI Powered Cybersecurity")
        st.image(logo_path, width=240)  # Replace with your logo

        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Copilot",
                "Pen Test",
                "Threat Model",
                "RFPs",
                "Integrations",
                "Team",
                "Tutorials",
                "Settings",
                "About",
            ],
            icons=[
                "speedometer2",
                "chat-dots",
                "person",
                "file-earmark-text",
                "search",
                "globe",
                "people",
                "book",
                "gear",
                "info-circle",
            ],
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                },
                "icon": {"color": "#000000", "font-size": "14px"},
                "nav-link": {
                    "font-size": "14px",
                    "color": "#000000",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "rgba(211, 211, 211, 0.5)",
                },
                "nav-link-selected": {"background-color": "rgba(255, 255, 255, 0.2)"},
            },
        )

        st.title("Beta")
        st.caption("V1.0")

    return selected
