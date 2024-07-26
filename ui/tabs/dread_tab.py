import streamlit as st
from src.dread import (
    create_dread_assessment_prompt,
    get_dread_assessment,
    get_dread_assessment_azure,
    get_dread_assessment_google,
    dread_json_to_markdown,
)


def dread_tab():
    st.markdown(
        """
    DREAD is a method for evaluating and prioritising risks associated with security threats. It assesses threats based on **D**amage potential, 
    **R**eproducibility, **E**xploitability, **A**ffected users, and **D**iscoverability. This helps in determining the overall risk level and 
    focusing on the most critical threats first. Use this tab to perform a DREAD risk assessment for your application / system.
    """
    )
    st.markdown("""---""")

    dread_assessment_submit_button = st.button(label="Generate DREAD Risk Assessment")
    if dread_assessment_submit_button:
        if "threat_model" in st.session_state and st.session_state["threat_model"]:
            threats_markdown = st.session_state["threat_model"]
            dread_assessment_prompt = create_dread_assessment_prompt(threats_markdown)
            with st.spinner("Generating DREAD Risk Assessment..."):
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
                            dread_assessment = get_dread_assessment_azure(
                                azure_api_endpoint,
                                azure_api_key,
                                azure_api_version,
                                azure_deployment_name,
                                dread_assessment_prompt,
                            )
                        elif model_provider == "OpenAI API":
                            openai_api_key = st.session_state.get("openai_api_key_tab")
                            selected_model = st.session_state.get("selected_model_tab")
                            dread_assessment = get_dread_assessment(
                                openai_api_key, selected_model, dread_assessment_prompt
                            )
                        elif model_provider == "Google AI API":
                            google_api_key = st.session_state.get("google_api_key_tab")
                            google_model = st.session_state.get("google_model_tab")
                            dread_assessment = get_dread_assessment_google(
                                google_api_key, google_model, dread_assessment_prompt
                            )
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(
                                f"Error generating DREAD risk assessment after {max_retries} attempts: {e}"
                            )
                            dread_assessment = []
                        else:
                            st.warning(
                                f"Error generating DREAD risk assessment. Retrying attempt {retry_count+1}/{max_retries}..."
                            )
            dread_assessment_markdown = dread_json_to_markdown(dread_assessment)
            st.markdown(dread_assessment_markdown)
            st.download_button(
                label="Download DREAD Risk Assessment",
                data=dread_assessment_markdown,
                file_name="dread_assessment.md",
                mime="text/markdown",
            )
            st.session_state["dread_assessment"] = dread_assessment
        else:
            st.error(
                "Please generate a threat model first before requesting a DREAD risk assessment."
            )
