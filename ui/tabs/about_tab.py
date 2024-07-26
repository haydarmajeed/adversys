import streamlit as st


def about_tab():
    st.title("About")
    st.markdown(
        """
    Welcome to adversys, an AI-powered tool designed to help teams produce better threat models for their applications. Threat modelling is a key activity in the software development lifecycle, but is often overlooked or poorly executed. adversys aims to help teams produce more comprehensive threat models by leveraging the power of Large Language Models (LLMs) to generate a threat list, attack tree and/or mitigating controls for an application based on the details provided. Created by Haydar Majeed.

    Below is an example application description that you can use to test adversys:

    > A web application that allows users to create, store, and share personal notes. The application is built using the React frontend framework and a Node.js backend with a MongoDB database. Users can sign up for an account and log in using OAuth2 with Google or Facebook. The notes are encrypted at rest and are only accessible by the user who created them. The application also supports real-time collaboration on notes with other users.

    ### FAQs
    """
    )

    with st.expander("What is adversys?"):
        st.write(
            "adversys is an AI-powered tool that helps teams produce better threat models for their applications."
        )

    with st.expander("How to perform Threat Modeling with adversys?"):
        st.write(
            "Provide a description of the application and the type of authentication it uses (e.g. OAuth2, JWT, etc.). Below is an example application description that you can use to test adversys:"
        )
        st.write(
            """
        > A web application that allows users to create, store, and share personal notes. The application is built using the React frontend framework and a Node.js backend with a MongoDB database. Users can sign up for an account and log in using OAuth2 with Google or Facebook. The notes are encrypted at rest and are only accessible by the user who created them. The application also supports real-time collaboration on notes with other users.
        """
        )

    with st.expander("What should I upload to speedup the threat modeling process?"):
        st.write(
            "Uploading an architecture diagram of the application you are threat modeling will help us understand the application better and generate a more accurate threat model."
        )

    with st.expander("What framework is used to create the threat model?"):
        st.write("adversys leverages the STRIDE framework to create the threat model.")

    with st.expander("What is STRIDE?"):
        st.write(
            """
        STRIDE is a threat modeling methodology that helps to identify and categorise potential security risks in software applications. 
        It stands for **S**poofing, **T**ampering, **R**epudiation, **I**nformation Disclosure, **D**enial of Service, and **E**levation of Privilege.
        """
        )

    with st.expander("How does adversys work?"):
        st.write(
            """
        When you enter an application description and other relevant details, the tool will use a GPT model to generate a threat model for your application. 
        The model uses the application description and details to generate a list of potential threats and then categorises each threat according to the STRIDE methodology.
        """
        )

    with st.expander("Do you store the application details provided?"):
        st.write(
            "No, adversys does not store your application description or other details. All entered data is deleted after you close the browser tab."
        )

    with st.expander("Why does it take so long to generate a threat model?"):
        st.write(
            """
        If you are using a free OpenAI API key, it will take a while to generate a threat model. This is because the free API key has strict rate limits. 
        To speed up the process, you can use a paid API key.
        """
        )

    with st.expander("Are the threat models 100% accurate?"):
        st.write(
            """
        No, the threat models are not 100% accurate. adversys uses GPT Large Language Models (LLMs) to generate its output. The GPT models are powerful, 
        but they sometimes make mistakes and are prone to 'hallucinations' (generating irrelevant or inaccurate content). 
        Please use the output only as a starting point for identifying and addressing potential security risks in your applications.
        """
        )

    with st.expander("How can I improve the accuracy of the threat models?"):
        st.write(
            """
        You can improve the accuracy of the threat models by providing a detailed description of the application and selecting the correct application type, 
        authentication methods, and other relevant details. The more information you provide, the more accurate the threat models will be.
        """
        )
