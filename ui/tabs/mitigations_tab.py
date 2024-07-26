import streamlit as st
from src.mitigations import (
    create_mitigations_prompt,
    get_mitigations,
    get_mitigations_azure,
    get_mitigations_google,
)


def mitigations_tab():
    st.markdown(
        """
    Use this tab to generate potential mitigations for the threats identified in the threat model. Mitigations are security controls or
    countermeasures that can help reduce the likelihood or impact of a security threat. The generated mitigations can be used to enhance
    the security posture of the application and protect against potential attacks.
    """
    )
    st.markdown("""---""")

    mitigations_submit_button = st.button(label="Suggest Mitigations")

    if mitigations_submit_button:
        if "threat_model" in st.session_state and st.session_state["threat_model"]:
            threats_markdown = st.session_state["threat_model"]
            mitigations_prompt = create_mitigations_prompt(threats_markdown)

            with st.spinner("Suggesting mitigations..."):
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        model_provider = st.session_state.get("model_provider_tab")
                        if model_provider == "Azure OpenAI Service":
                            azure_api_endpoint = st.session_state.get(
                                "azure_api_endpoint_tab"
                            )
                            azure_api_key = st.session_state.get("azure_api_key_tab")
                            azure_api_version = "2023-12-01-preview"
                            azure_deployment_name = st.session_state.get(
                                "azure_deployment_name_tab"
                            )
                            mitigations_markdown = get_mitigations_azure(
                                azure_api_endpoint,
                                azure_api_key,
                                azure_api_version,
                                azure_deployment_name,
                                mitigations_prompt,
                            )
                        elif model_provider == "OpenAI API":
                            openai_api_key = st.session_state.get("openai_api_key_tab")
                            selected_model = st.session_state.get("selected_model_tab")
                            mitigations_markdown = get_mitigations(
                                openai_api_key, selected_model, mitigations_prompt
                            )
                        elif model_provider == "Google AI API":
                            google_api_key = st.session_state.get("google_api_key_tab")
                            google_model = st.session_state.get("google_model_tab")
                            mitigations_markdown = get_mitigations_google(
                                google_api_key, google_model, mitigations_prompt
                            )

                        st.markdown(mitigations_markdown)
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(
                                f"Error suggesting mitigations after {max_retries} attempts: {e}"
                            )
                            mitigations_markdown = ""
                        else:
                            st.warning(
                                f"Error suggesting mitigations. Retrying attempt {retry_count+1}/{max_retries}..."
                            )

            st.markdown("")

            st.download_button(
                label="Download Mitigations",
                data=mitigations_markdown,
                file_name="mitigations.md",
                mime="text/markdown",
            )
            st.session_state["mitigations"] = mitigations_markdown
        else:
            st.error(
                "Please generate a threat model first before suggesting mitigations."
            )
