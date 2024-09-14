

import os
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

import streamlit as st


def llm_instance_builder():

    llm=None
    if "OpenAI" == st.session_state.model_type:
        pass
    elif "Azure OpenAI" == st.session_state.model_type:
        llm = AzureChatOpenAI(  model=st.session_state.azure_deployment,
                                deployment_name=st.session_state.azure_deployment,
                                api_key=st.session_state.azure_key,
                                api_version=st.session_state.azure_version,
                                azure_endpoint =st.session_state.azure_endpoint)

    elif "Google Gemini (Free)" == st.session_state.model_type:
        llm = ChatGoogleGenerativeAI(
                            model="gemini-1.5-flash",
                            temperature=0,
                        )    
        
    return llm
        