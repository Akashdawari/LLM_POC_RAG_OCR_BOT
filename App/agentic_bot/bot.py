import streamlit as st
from agent_components import agent_assembler, build_chat_history
from llm_initilizer import llm_instance_builder



def page4():

    
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
        llm = llm_instance_builder()
        agent_executor = agent_assembler(llm)
        st.title("Bot")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if len(st.session_state.messages)==0:
            text = agent_executor.invoke({"input": "hi", "chat_history": build_chat_history()})["output"]
            st.chat_message("assistant").markdown(text)
            st.session_state.messages.append({"role": "assistant", "content": text})

        # React to user input
        if prompt := st.chat_input("What is up?"):

            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            k = prompt
            response = f'{agent_executor.invoke({"input": prompt, "chat_history": build_chat_history()})["output"]}'
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})