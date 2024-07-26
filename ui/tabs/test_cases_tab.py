import streamlit as st
from src.test_cases import (
    create_test_cases_prompt,
    get_test_cases,
    get_test_cases_azure,
    get_test_cases_google,
)


def test_cases_tab():
    st.markdown(
        """
    Test cases are used to validate the security of an application and ensure that potential vulnerabilities are identified and 
    addressed. This tab allows you to generate test cases using Gherkin syntax. Gherkin provides a structured way to describe application 
    behaviours in plain text, using a simple syntax of Given-When-Then statements. This helps in creating clear and executable test 
    scenarios.
    """
    )
    st.markdown("""---""")

    test_cases_submit_button = st.button(label="Generate Test Cases")

    if test_cases_submit_button:
        if "threat_model" in st.session_state and st.session_state["threat_model"]:
            threats_markdown = st.session_state["threat_model"]
            test_cases_prompt = create_test_cases_prompt(threats_markdown)

            with st.spinner("Generating test cases..."):
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
                            test_cases_markdown = get_test_cases_azure(
                                azure_api_endpoint,
                                azure_api_key,
                                azure_api_version,
                                azure_deployment_name,
                                test_cases_prompt,
                            )
                        elif model_provider == "OpenAI API":
                            openai_api_key = st.session_state.get("openai_api_key_tab")
                            selected_model = st.session_state.get("selected_model_tab")
                            test_cases_markdown = get_test_cases(
                                openai_api_key, selected_model, test_cases_prompt
                            )
                        elif model_provider == "Google AI API":
                            google_api_key = st.session_state.get("google_api_key_tab")
                            google_model = st.session_state.get("google_model_tab")
                            test_cases_markdown = get_test_cases_google(
                                google_api_key, google_model, test_cases_prompt
                            )

                        st.markdown(test_cases_markdown)
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(
                                f"Error generating test cases after {max_retries} attempts: {e}"
                            )
                            test_cases_markdown = ""
                        else:
                            st.warning(
                                f"Error generating test cases. Retrying attempt {retry_count+1}/{max_retries}..."
                            )

            st.markdown("")

            st.download_button(
                label="Download Test Cases",
                data=test_cases_markdown,
                file_name="test_cases.md",
                mime="text/markdown",
            )

            st.session_state["test_cases"] = test_cases_markdown
        else:
            st.error(
                "Please generate a threat model first before requesting test cases."
            )
