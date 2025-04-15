import streamlit as st
from utils_entry import *


# Configure the Streamlit app with a title, layout, icon, and initial sidebar state
st.set_page_config(page_title="Marking App",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Initialize session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out (to delete data)", icon=":material/logout:")

mas_reflection_journal = st.Page("components/main.py", 
                   title="Word document Report", 
                   icon=":material/draft:")

if st.session_state.logged_in:

    st.sidebar.title(":orange[Assistive AI Marking Tool]", help=intro_var)
    #st.sidebar.text_input("Enter huggingface token")


    pg = st.navigation(
    {   
        "Marking Components": [mas_reflection_journal],
        "Account": [logout_page],
    }
        )

else:
    pg = st.navigation([login_page])

pg.run()

