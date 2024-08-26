import os
import sys
from dotenv import load_dotenv
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# Add project root and individual package directories to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, "utils"))
sys.path.append(os.path.join(project_root, "key_extractor_feature"))
sys.path.append(os.path.join(project_root, "database"))
sys.path.append(os.path.join(project_root, "home_page"))
sys.path.append(os.path.join(project_root, "rag_bot"))
sys.path.append(os.path.join(project_root, "agentic_bot"))
load_dotenv()

import streamlit as st
import re
import hashlib
from db_components import get_db_connection
from home_page_main import page1
from key_extractor_main import page3
from qna_assambler import page2
from bot import page4
from email_utils import send_email_with_attachment
from llm_initilizer import llm_instance_builder

CONN = get_db_connection()
C = CONN.cursor()


st.set_page_config(layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</syle>'.format(f.read()), unsafe_allow_html=True)

base_dir = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(base_dir, 'assets', 'style', 'style.css')
local_css(css_path)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, password, reason):
    C.execute('INSERT INTO users (username, email, password, reason) VALUES (?, ?, ?, ?)', 
              (username, email, hash_password(password), reason))
    CONN.commit()

def authenticate_user(username, password):
    C.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    return C.fetchone()


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_strong_password(password):
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(regex, password) is not None

def is_username_taken(username):
    C.execute('SELECT * FROM users WHERE username = ?', (username,))
    return C.fetchone() is not None

def signup():
    st.title("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    reason = st.text_area("Why are you using the app?")
    
    if st.button("Sign Up"):
        if not is_valid_email(email):
            st.error("Invalid email format!")
        elif is_username_taken(name):
            st.error("Username already taken!")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        elif not is_strong_password(password):
            st.error("Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, one number, and one special character.")
        elif not name or not email or not password or not reason:
            st.error("Please fill all the fields!")
        else:
            add_user(name, email, password, reason)
            send_email_with_attachment(email)
            st.success("User registered successfully!")
            st.session_state['authenticated'] = True
            st.rerun()

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success("Logged in successfully!")
            st.rerun()  # Refresh

        else:
            st.error("Invalid username or password.")

def set_environment_variables():

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
    if st.button("Submit"):
        st.success("Successfully! assign the required keys")
        if model_type == "OpenAI":
            llm = llm_instance_builder(model_type, openai_key)
        elif model_type == "Azure OpenAI":
            llm = llm_instance_builder(model_type, azure_key, azure_endpoint, 
                                       azure_deployment, azure_version)
        return llm

# Function to clear cache
def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()

# Dictionary to link page names to functions
pages = {
    "Home": page1,
    "RAG QnA": page2,
    "Extract Data": page3,
    "Page 4": page4,
}


# Main app
def main():
    
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:

        st.sidebar.title("Menu")
        page = st.sidebar.radio("Go to", list(pages.keys()))

        # Call the function of the selected page
        pages[page]()

        

    else:
        st.sidebar.title("Authentication")
        auth_choice = st.sidebar.radio("Choose Auth Option", ["Login", "Sign Up"])
        
        if auth_choice == "Login":
            login()
        else:
            signup()

if __name__ == "__main__":
    main()