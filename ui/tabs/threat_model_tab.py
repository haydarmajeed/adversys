import streamlit as st
import base64
from threat_models.stride import create_stride_threat_model_prompt
from threat_models.pasta import create_pasta_prompt
from threat_models.owasp import create_owasp_prompt

from dread import create_dread_assessment_prompt
from utils import (
    get_threat_model,
    get_threat_model_azure,
    get_threat_model_google,
    json_to_markdown,
    get_image_analysis,
    create_image_analysis_prompt,
)
def get_input():
    input_text = st.text_area(
        label="Describe the application to be modelled",
        placeholder="Enter your application details...",
        height=150,
        key="app_desc",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )
    st.session_state['image_analysis_content'] = input_text
    return input_text

def threat_model_tab():
    st.header("Threat Model")
    st.markdown("""
    A threat model helps identify and evaluate potential security threats to applications / systems. It provides a systematic approach to 
    understanding possible vulnerabilities and attack vectors. Use this tab to generate a threat model using the STRIDE methodology.
    """)
    st.markdown("""---""")

    threat_model = st.selectbox(
        "Select your preferred threat model:",
        ["STRIDE", "DREAD", "PASTA", "OWASP"],
        key="threat_model_provider_tab",
        help="Select the threat model you would like to use.",
    )

    model_provider = st.selectbox(
        "Select your preferred model provider:",
        ["OpenAI API", "Azure OpenAI Service", "Google AI API"],
        key="model_provider_tab",
        help="Select the model provider you would like to use. This will determine the models available for selection.",
    )

    # Add input fields for API keys and model selection based on the provider
    if model_provider == "OpenAI API":
        openai_api_key = st.text_input("Enter your OpenAI API key:", type="password", key="openai_api_key_tab")
        selected_model = st.selectbox("Select the model:", ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"], key="selected_model_tab")
    elif model_provider == "Azure OpenAI Service":
        azure_api_key = st.text_input("Azure OpenAI API key:", type="password", key="azure_api_key_tab")
        azure_api_endpoint = st.text_input("Azure OpenAI endpoint:", key="azure_api_endpoint_tab")
        azure_deployment_name = st.text_input("Deployment name:", key="azure_deployment_name_tab")
        azure_api_version = '2023-12-01-preview'
    elif model_provider == "Google AI API":
        google_api_key = st.text_input("Enter your Google AI API key:", type="password", key="google_api_key_tab")
        google_model = st.selectbox("Select the model:", ["gemini-1.5-pro-latest"], key="google_model_tab")

    col1, col2 = st.columns([1, 1])

    with col1:
        if model_provider == "OpenAI API" and selected_model in ["gpt-4-turbo", "gpt-4o"]:
            uploaded_file = st.file_uploader("Upload architecture diagram", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                if not openai_api_key:
                    st.error("Please enter your OpenAI API key to analyse the image.")
                else:
                    if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
                        st.session_state.uploaded_file = uploaded_file
                        with st.spinner("Analysing the uploaded image..."):
                            base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                            image_analysis_prompt = create_image_analysis_prompt()
                            try:
                                image_analysis_output = get_image_analysis(openai_api_key, selected_model, image_analysis_prompt, base64_image)
                                if image_analysis_output and 'choices' in image_analysis_output and image_analysis_output['choices'][0]['message']['content']:
                                    st.session_state['image_analysis_content'] = image_analysis_output['choices'][0]['message']['content']
                                else:
                                    st.error("Failed to analyze the image. Please check the API key and try again.")
                            except Exception as e:
                                st.error("An unexpected error occurred while analyzing the image.")
                                print(f"Error: {e}")

            image_analysis_content = st.text_area(
                label="Describe the application to be modelled",
                value=st.session_state['image_analysis_content'],
                key="image_analysis_content_widget",
                help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
            )
            if image_analysis_content != st.session_state['image_analysis_content']:
                st.session_state['image_analysis_content'] = image_analysis_content
        else:
            image_analysis_content = get_input()

    with col2:
        app_type = st.selectbox("Select the application type", ["Web application", "Mobile application", "Desktop application", "Cloud application", "IoT application", "Other"], key="app_type")
        sensitive_data = st.selectbox("What is the highest sensitivity level of the data processed by the application?", ["Top Secret", "Secret", "Confidential", "Restricted", "Unclassified", "None"], key="sensitive_data")
        internet_facing = st.selectbox("Is the application internet-facing?", ["Yes", "No"], key="internet_facing")
        authentication = st.selectbox("What authentication methods are supported by the application?", ["SSO", "MFA", "OAUTH2", "Basic", "None"], key="authentication")

    st.session_state['app_type2'] = app_type
    st.session_state['sensitive_data2'] = sensitive_data
    st.session_state['internet_facing2'] = internet_facing
    st.session_state['authentication2'] = authentication

    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

    with col1:
        threat_model_submit_button = st.button(label="Generate Threat Model")

    with col3:
        save_report = st.button(label="Save Report")

    if threat_model_submit_button and st.session_state.get('image_analysis_content'):
        image_analysis_content = st.session_state['image_analysis_content']
        if threat_model == "STRIDE":
            threat_model_prompt = create_stride_threat_model_prompt(app_type, authentication, internet_facing, sensitive_data, image_analysis_content)
        elif threat_model == "DREAD":
            threat_model_prompt = create_dread_assessment_prompt(app_type, authentication, internet_facing, sensitive_data, image_analysis_content)
        elif threat_model == "PASTA":
            threat_model_prompt = create_pasta_prompt(app_type, authentication, internet_facing, sensitive_data, image_analysis_content)
        elif threat_model == "OWASP":
            threat_model_prompt = create_owasp_prompt(app_type, authentication, internet_facing, sensitive_data, image_analysis_content)

        with st.spinner("Analysing potential threats..."):
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:
                    if model_provider == "Azure OpenAI Service":
                        model_output = get_threat_model_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, threat_model_prompt)
                    elif model_provider == "OpenAI API":
                        model_output = get_threat_model(openai_api_key, selected_model, threat_model_prompt)
                    elif model_provider == "Google AI API":
                        model_output = get_threat_model_google(google_api_key, google_model, threat_model_prompt)

                    threat_model = model_output.get("threat_model", [])
                    improvement_suggestions = model_output.get("improvement_suggestions", [])

                    st.session_state['threat_model'] = threat_model
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        st.error(f"Error generating threat model after {max_retries} attempts: {e}")
                        threat_model = []
                        improvement_suggestions = []
                    else:
                        st.warning(f"Error generating threat model. Retrying attempt {retry_count+1}/{max_retries}...")

        markdown_output = json_to_markdown(threat_model, improvement_suggestions)
        st.markdown(markdown_output)

        st.download_button(
            label="Download Threat Model",
            data=markdown_output,
            file_name="stride_gpt_threat_model.md",
            mime="text/markdown",
        )

    if threat_model_submit_button and not st.session_state.get('image_analysis_content'):
        st.error("Please enter your application details before submitting.")