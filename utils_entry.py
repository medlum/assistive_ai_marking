
import streamlit as st
from pathlib import Path
import shutil
from utils_twilio_coffee import send_sms_txt, buymecoffee, buymecoffee_btn_css
from utils_help_msg import *

extracted_files_path = Path("./extracted_files")
extracted_pyfiles_path = Path("./extracted_pyfiles")

def find_user_credentials(user_id, password):
    users = st.secrets["users"]
    for user in users:
        if user['user_id'] == user_id and user['password'] == password:
            return True

    return None


def login():

    col1, col2, col3 = st.columns([1,1,1])
    
    col2.subheader(":orange[Assistive AI Marking Tool]", help=app_usage_text)

    user_id = col2.text_input(f":gray[User ID]")
    
    access_token = col2.text_input(label=":gray[API Key]", 
                                      type='password',
                                      help=togetherai_signup_msg)
    
    password = col2.text_input(":gray[Password]", type="password")

    with col2.expander(":gray[How to obtain an API key?] "):
        st.write("1. Set up your account at https://www.together.ai")
        st.image("./data/togetherai_signup.png")
        st.write("2. Generate API key in settings")
        st.image("./data/togetherai_api.png")
        st.write("3. Enable :blue[No] in Privacy and Security")
        st.image("./data/togetherai_data_protection.png")
        st.write("4. How to check credit balance?")
        st.image("./data/togetherai_billing.png")

        
    
    #col2.markdown(f'<span style="text-align: justify; font-size:12px; color:gray;">{app_usage_text}</span>', unsafe_allow_html=True)
    
    # buymecoffee button

    col2.markdown(buymecoffee_btn_css, unsafe_allow_html=True)
    if col2.button("☕ Buy me coffee"):
        buymecoffee()

    col2.markdown(f'<span style="font-size:12px; color:gray;">{development_msg}</span>', unsafe_allow_html=True)
    
    login_state = find_user_credentials(user_id, password)

    if login_state:

        if access_token :
            st.session_state.access_token = access_token  
            # st.session_state.access_token contains a tuple -> (xxxx, )   
            # hence st.session_state.access_token[0]

        else: 
            col2.warning("API KEY REQUIRED")
            st.stop()
        #st.session_state.access_token = st.secrets.api_keys.huggingfacehub_api_token, 
            
        with col2.status("Logging in...", expanded=False):
            
            st.session_state.logged_in = True
            st.session_state.user_id = user_id

            col2.success(f"Successfully authenticated as: {user_id}")

            sms_txt = f"LOGIN ALERT: {st.session_state.user_id}."
            send_sms_txt(sms_txt)
            
            st.rerun()
    
def logout():

    sms_txt = f"LOGOUT ALERT: {st.session_state.user_id}."
    send_sms_txt(sms_txt)
     
    if Path("./extracted_files").exists():
        shutil.rmtree('./extracted_files')

    if Path("./extracted_pyfiles").exists():
        shutil.rmtree('./extracted_pyfiles')
    
    if Path(f"./{st.session_state.user_id}").exists():
        shutil.rmtree(f"./{st.session_state.user_id}")

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.access_token = None
    st.session_state.clear()

    st.rerun()
