import streamlit as st
from tempfile import NamedTemporaryFile
import os
from ingest_component import ingest_documents, get_related_documents
from graph_component import rag_machine
from llm_initilizer import llm_instance_builder


    
def page2():

    if ('model_type' not in st.session_state):
        st.subheader("Set Environment Variables")
        model_type = st.selectbox("Select type of LLM",
                                    ("OpenAI", "Azure OpenAI"))
        if model_type == "OpenAI":
            openai_key = st.text_input("Enter OpenAI Key")
        elif model_type == "Azure OpenAI":
            azure_key = st.text_input("Enter Azure OpenAI Key")
            azure_endpoint = st.text_input("Enter Azure OpenAI Endpoint")
            azure_deployment = st.text_input("Enter Azure OpenAI Deployment")
            azure_version = st.text_input("Enter Azure OpenAI Version")
        elif model_type == "Google Gemini":
            pass
        if st.button("Submit"):
            st.session_state.model_type = model_type
            if model_type == "Azure OpenAI":
                st.session_state.azure_key = azure_key
                st.session_state.azure_endpoint = azure_endpoint
                st.session_state.azure_deployment = azure_deployment
                st.session_state.azure_version = azure_version
            elif model_type == "OpenAI":
                st.session_state.openai_key = openai_key
            elif model_type == "Google Gemini":
                pass
            st.rerun()

    else:
        st.title("QnA Bot with your Document")

        if "model_type" not in st.session_state:
            st.error("Please provide a llm to procide further")
        else:

            uploaded_file = st.file_uploader("Upload your document to chat with...", type=['pdf','docx', 'doc', 'txt', 'xlsx', 'xls', 'csv', 'pptx'])

            
            if uploaded_file is not None:
                # Save uploaded file to a temporary file
                file_extension = os.path.splitext(uploaded_file.name)[1]

                with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    temp_file_path = temp_file.name
                
                status, all_docs = ingest_documents(temp_file_path, file_extension)

                if status:
                    rag_type = st.radio(
                            "Select type of RAG",
                            ["**Simple RAG**", "***Corrective RAG***", "**Self RAG**"],
                            horizontal=True
                        )
                    st.subheader("Ask your Question")

                    question = st.text_area("Type you question in details:")

                    if question:

                        related_docs = get_related_documents(question, all_docs)
                        llm = llm_instance_builder()
                        answer = rag_machine(rag_type, related_docs, question, llm, all_docs)
                        st.subheader("Generated RAG Response")
                        st.write(answer)

                
                else:

                    st.info("""Sorry for the inconvienence as we are facing some technical issue with this service.
                            Suggest you to explore other services in the app while we fix this service.""")
                    
                    

