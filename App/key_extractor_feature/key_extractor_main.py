import streamlit as st
from tempfile import NamedTemporaryFile
import os
from ocr_component import text_extractor
from llm_component import key_extractor




def page3():

    
    if ('model_type' not in st.session_state):
        st.subheader("Set Environment Variables")
        model_type = st.selectbox("Select type of LLM",
                                    ("OpenAI", "Azure OpenAI", "Google Gemini (Free)"))
        if model_type == "OpenAI":
            openai_key = st.text_input("Enter OpenAI Key")
        elif model_type == "Azure OpenAI":
            azure_key = st.text_input("Enter Azure OpenAI Key")
            azure_endpoint = st.text_input("Enter Azure OpenAI Endpoint")
            azure_deployment = st.text_input("Enter Azure OpenAI Deployment")
            azure_version = st.text_input("Enter Azure OpenAI Version")
        elif model_type == "Google Gemini (Free)":
            st.warning("Note: By selecting this free model, you may experience limited performance and receive unintended results, as it is less powerful compared to premium models.")
        if st.button("Submit"):
            st.session_state.model_type = model_type
            if model_type == "Azure OpenAI":
                st.session_state.azure_key = azure_key
                st.session_state.azure_endpoint = azure_endpoint
                st.session_state.azure_deployment = azure_deployment
                st.session_state.azure_version = azure_version
            elif model_type == "OpenAI":
                st.session_state.openai_key = openai_key
            elif model_type == "Google Gemini (Free)":
                pass
            st.rerun()
    else:
        st.title("Key-Value Extractor")

        if "model_type" not in st.session_state:
            st.error("Please provide a llm to procide further")
        else:

            uploaded_file = st.file_uploader("Upload PDF, JPEG, or PNG files", type=['pdf', 'jpeg', 'jpg', 'png'])


            if uploaded_file is not None:
                # Save uploaded file to a temporary file
                with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    temp_file_path = temp_file.name

                type_file = st.selectbox("Select the type of file", ["Ticket", "ID Card", "Invoice"])


                if st.button("Start Process"):
                    # Extract text from the file
                    raw_text = text_extractor(temp_file_path)
                    json_data = key_extractor(raw_text, type_file)
                    
                    st.subheader("Extracted Data")
                    if type_file == "Ticket" and not json_data.get("IsTicket", False):
                        st.warning("Uploaded Document is not a Ticket Document Category")
                    elif type_file == "ID Card" and not json_data.get("IsIDCard", False):
                        st.warning("Uploaded Document is not a ID Card Document Category")
                    elif type_file == "Invoice" and not json_data.get("IsInvoice", False):
                        st.warning("Uploaded Document is not a Invoice Document Category")
                    # Display each key-value pair in columns
                    for key, value in json_data.items():
                        # If the value is a list (like ItemDetails), handle it separately
                        if isinstance(value, list):
                            for item in value:
                                for item_key, item_value in item.items():
                                    st.markdown(f"**{item_key}**: {item_value}")
                        else:
                            st.markdown(f"**{key}**: {value}")

                    st.subheader("Json Structure")
                    st.json(json_data)

