import streamlit as st
from src.utils import mermaid
from src.attack_tree import (
    create_attack_tree_prompt,
    get_attack_tree,
    get_attack_tree_azure,
)


def attack_tree_tab():
    st.markdown(
        """
    Attack trees are a structured way to analyse the security of a system. They represent potential attack scenarios in a hierarchical format, 
    with the ultimate goal of an attacker at the root and various paths to achieve that goal as branches. This helps in understanding system 
    vulnerabilities and prioritising mitigation efforts.
    """
    )
    st.markdown("""---""")

    model_provider = st.session_state.get("model_provider_tab")

    if model_provider == "Google AI API":
        st.warning(
            "⚠️ Google's safety filters prevent the reliable generation of attack trees. Please use a different model provider."
        )
    else:
        attack_tree_submit_button = st.button(label="Generate Attack Tree")

        if attack_tree_submit_button and st.session_state.get("image_analysis_content"):
            image_analysis_content = st.session_state.get("image_analysis_content")
            app_type = st.session_state.get("app_type2")
            authentication = st.session_state.get("authentication2")
            internet_facing = st.session_state.get("internet_facing2")
            sensitive_data = st.session_state.get("sensitive_data2")
            attack_tree_prompt = create_attack_tree_prompt(
                app_type,
                authentication,
                internet_facing,
                sensitive_data,
                image_analysis_content,
            )

            with st.spinner("Generating attack tree..."):
                try:
                    if model_provider == "Azure OpenAI Service":
                        azure_api_endpoint = st.session_state.get(
                            "azure_api_endpoint_tab"
                        )
                        azure_api_key = st.session_state.get("azure_api_key_tab")
                        azure_api_version = "2023-12-01-preview"
                        azure_deployment_name = st.session_state.get(
                            "azure_deployment_name_tab"
                        )
                        mermaid_code = get_attack_tree_azure(
                            azure_api_endpoint,
                            azure_api_key,
                            azure_api_version,
                            azure_deployment_name,
                            attack_tree_prompt,
                        )
                    elif model_provider == "OpenAI API":
                        openai_api_key = st.session_state.get("openai_api_key_tab")
                        selected_model = st.session_state.get("selected_model_tab")
                        mermaid_code = get_attack_tree(
                            openai_api_key, selected_model, attack_tree_prompt
                        )

                    st.write("Attack Tree Code:")
                    st.session_state["attack_tree"] = mermaid_code

                    st.code(mermaid_code)

                    st.write("Attack Tree Diagram Preview:")
                    mermaid(mermaid_code)

                    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

                    with col1:
                        st.download_button(
                            label="Download Diagram Code",
                            data=mermaid_code,
                            file_name="attack_tree.md",
                            mime="text/plain",
                            help="Download the Mermaid code for the attack tree diagram.",
                        )

                    with col2:
                        st.link_button("Open Mermaid Live", "https://mermaid.live")

                except Exception as e:
                    st.error(f"Error generating attack tree: {e}")
