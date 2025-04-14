from twilio.rest import Client
import streamlit as st
from streamlit_extras.buy_me_a_coffee import button


account_sid = st.secrets.twilio.account_sid

auth_token = st.secrets.twilio.auth_token
client = Client(account_sid, auth_token)

def send_sms_txt(body):
    try:
        client.messages.create(
            from_='+17087266912',
            body=body,
            to='+6594235231'
        )
    except Exception:
        st.warning("Twilio SMS limit reached")

# custom CSS for buttons
buymecoffee_btn_css = """
<style>
    .stButton > button {
        background-color: #ffdd00; /* Yellow background */
        color: #383736; 
        border: none; /* No border */
        padding: 5px 22px; /* Reduced top and bottom padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 8px !important;
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 9px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }
    .stButton > button:hover {
        color: #383736; 
        background-color: #877c27; /* Slightly darker yellow on hover */
    }
</style>
"""

coffee_text = """

Hey there! If you’ve found my work helpful, consider buying me a coffee - it’s a small but meaningful way to show your support.

- It helps me keep going - Developing and maintaining this takes time, and your support keeps me motivated.

- It keeps things free - I love sharing my work with everyone, and a coffee helps cover costs like hosting and development tools.

- It encourages new features - Your support lets me dedicate more time to improving and expanding what I offer.

- It’s a simple way to say thanks - If you’ve benefited from my work, this is an easy way to show appreciation.

Every coffee means a lot, thanks for being awesome!
"""

@st.dialog("Why ☕ ?")
def buymecoffee():
    st.markdown(f'<span style="font-size:14px; color:gray;">{coffee_text}</span>', unsafe_allow_html=True)
    st.image('./data/paynowME.jpeg')







# Custom CSS for floating button
#floating_button_css = """
#<link href="https://fonts.googleapis.com/css2?family=Cookie&display=swap" rel="stylesheet">
#<style>
#    .floating-button {
#        position: fixed;
#        bottom: 20px;
#        right: 20px;
#        background-color: #ffdd00;
#        color: #4B382A !important;
#        padding: 5px 20px;
#        border-radius: 12px;
#        text-align: center;
#        font-weight: 550;
#        font-size: 25px;
#        font-family: 'Cookie', cursive;
#        text-decoration: none !important;
#        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
#        transition: all 0.3s ease-in-out;
#        display: inline-block;
#    }
#    .floating-button:hover {
#        background-color: #ffcc00;
#        transform: scale(1.1);
#    }
#    .floating-button a {
#        color: inherit !important;
#        text-decoration: none !important;
#        display: inline-block;
#        width: 100%;
#        height: 100%;
#    }
#</style>
#"""

# HTML for Buy Me a Coffee button
#floating_button_html = """
#<a class="floating-button" href="?page=donate" target="_blank">☕ Buy Me a Coffee</a>
#"""

# Inject HTML and CSS
#st.markdown(floating_button_css, unsafe_allow_html=True)
#st.markdown(floating_button_html, unsafe_allow_html=True)

# Handle navigation
#query_params = st.query_params
#if "page" in query_params and query_params["page"] == "donate":
#    st.write("Welcome to the donation page!")
#    st.balloons()
