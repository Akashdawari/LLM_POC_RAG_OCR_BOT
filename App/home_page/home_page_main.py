import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_timeline import timeline
import os
import json

from assets.template.page1_html import *

# Function to fetch personal data from JSON
def fetch_data(filname):
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir,"App", 'assets', 'data', filname)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to load Lottie animation from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Function to create gradient text
def gradient_text(content1, content2, profile_picture_url):
    st.markdown(GRADIENT_TEXT.format(profile_picture_url, content1, content2),
        unsafe_allow_html=True
    )


# Main function for the LinkedIn-like page
def page1():
    # Load personal information
    info = fetch_data("personal_info.json")

    # Load Lottie animations
    python_lottie = load_lottieurl("https://lottie.host/08e61c91-d9f8-4e44-9d88-162a9c89cdbb/VCfbO27kkO.json")
    my_sql_lottie = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_w11f2rwn.json")
    git_lottie = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_03cuemhb.json")
    docker_lottie = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_35uv2spq.json")
    tf_lottie = load_lottieurl("https://lottie.host/dcc87c77-3e96-4fe9-b07a-78723e073529/8bHxw4YPGX.json")

    # Header section with gradient text
    full_name = info['Full_Name']
    base_dir = os.getcwd()
    profile_pic_file_path = os.path.join(base_dir,"App", 'assets', 'data', "myself.jpg")
    
    gradient_text(f"Hi, I'm {full_name}👋", info["Intro"], profile_pic_file_path)

    contact_info_html = CONTANT_STRUCTURE.format(info["Phone"], info["Email"], info["Linkedin"], info["Youtube"], info["Medium"])

    st.markdown(contact_info_html, unsafe_allow_html=True)
    # Section for main content in columns
    st.markdown("---")
    st.subheader('⚒️ Skills')

    # Displaying skills using Lottie animations
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st_lottie(python_lottie, height=100,  key="python")
        st.write("Python")
        # Replacing st.image with HTML using streamlit.markdown
        st.markdown(
            SKILL_STRUCTURE["langchain"],
            unsafe_allow_html=True
        )
        

    with col2:
        st_lottie(git_lottie, height=100, key="git")
        st.write("Git")
        st.markdown(
            SKILL_STRUCTURE["azure"],
            unsafe_allow_html=True
        )

    with col3:
        st_lottie(docker_lottie, height=100, key="docker")
        st.write("Docker")
        st.markdown(
            SKILL_STRUCTURE["sklearn"],
            unsafe_allow_html=True
        )

    with col4:
        st_lottie(tf_lottie, height=100, key="js")
        st.write("Tensorflow")
        st_lottie(my_sql_lottie, height=100, key="mysql")
        st.write("MySQL")



    # Define your work experiences as a list of dictionaries
    work_experiences = fetch_data("workExp.json")

    st.subheader('Work Experience')

    # Create collapsible sections for each work experience
    # Create collapsible sections for each work experience
    for experience in work_experiences:
        with st.expander(f"{experience['role']} at {experience['company']} ({experience['start_date']} - {experience['end_date']})"):
            st.markdown(WORK_EXP_STRUCTURE.format(experience['role'], experience['company'], experience['start_date'], experience['end_date']),
              unsafe_allow_html=True)
            for responsibility in experience['responsibilities']:
                st.markdown(f"<li class='responsibility-item'>{responsibility}</li>", unsafe_allow_html=True)
            st.markdown("""
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
