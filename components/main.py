import streamlit as st
from huggingface_hub import InferenceClient
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer
from docx import Document
from report_utils import *
import ast
from utils_twilio_coffee import buymecoffee_btn_css, buymecoffee
from utils_inference import initialize_inferenceclient, model_list
from utils_help_msg import *

# ---------set css-------------#
#st.markdown(btn_css, unsafe_allow_html=True)
#st.markdown(image_css, unsafe_allow_html=True)

# Initialize the Inference Client with the API key 
client = initialize_inferenceclient()

# ------- create side bar --------#
with st.sidebar:
   
    #st.subheader("MAS Reflection Journal")

    model_id = model_list[0]    

#    with st.expander(":blue[SYSTEM SETUP]"):
#
#        tab1, tab2 = st.tabs(["Set your prompts", "Default Prompt settings"])
#
#        user_system_message = tab1.text_area("Enter prompts in points", height=200, placeholder="- First prompt\n- Second prompt\n- Third prompt")
#
#        tab2.text(system_message)
#
#        st.divider()
#        temperature_setting = 0.2
#
#        temperature_slider = st.slider("Temperature Parameter (default: 0.2)", 
#                                min_value=0.1, 
#                                max_value=1.0, step=0.1, 
#                                value=temperature_setting,
#                                help=ai_temperature_msg)
#        
#        if temperature_slider != temperature_setting:
#            temperature_setting = temperature_slider

    #pdf = './data/fmi_marking_rubrics.pdf'
    pdf = st.file_uploader(":gray[Upload marking rubrics]", ".pdf")
    if pdf is not None:
        rubric = ""
        reader = PdfReader(pdf)
        for page in reader.pages:
            rubric += page.extract_text()
        st.success("Marking rubrics accepted")
        #st.write(rubric)

    group_zip = st.sidebar.file_uploader(":gray[Upload a zip file]", type=['zip'], help='Zip file should contain students submission in .docx')
       
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)
    st.markdown(buymecoffee_btn_css, unsafe_allow_html=True)
    if st.button("☕ Buy me coffee"):
        buymecoffee()

# --- extract text in docs and add to session state---#
if group_zip is not None:

    data = []

    extracted_contents = extract_and_read_files(group_zip)

    for key in extracted_contents:

        if 'msg_history' not in st.session_state:
            st.session_state.msg_history = []
        
        st.session_state.msg_history.append({"role": "system", 
                                            "content": f"{system_message}"})
        
        st.session_state.msg_history.append({"role": "system", 
                                            "content": f"Here are the marking rubrics: {rubric}"})
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"Mark the following report for student name: {key}" })
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"{extracted_contents[key]}" })
        
        st.session_state.msg_history.append({"role": "user", 
                                            "content": f"Mark the report with high standard and be stringent when awarding marks." })

        st.subheader(f":blue[{key}]")

       # st.text(f"msg_history : {st.session_state.msg_history}")

        with st.expander(f":grey[*Submitted report*]"):         
            st.write(extracted_contents[key][1])            

        try:
            
            with st.status("Evaluating report...", expanded=True) as status:
                with st.empty():
                    try:
                        stream = client.chat_completion(
                            model=model_id,
                            messages=st.session_state.msg_history,
                            temperature=0.2,
                            max_tokens=5524,
                            top_p=0.7,
                            stream=True
                            )
                        collected_response = ""
                        for chunk in stream:
                            if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                                collected_response += chunk.choices[0].delta.content
                                st.text(collected_response.replace('{','').replace('}','').replace("'",""))
                        
                        actual_dict = ast.literal_eval(collected_response)
                        data.append(actual_dict)
                        status.update(label="Report evaluation completed...", state="complete", expanded=False)
                    
                    except Exception as e:
                        st.error(e)
        
        except Exception as e:
            st.error(f"Error generating response: {e}")
        
        del st.session_state.msg_history

    if data:
        st.subheader(f":orange[Marks Summary]")
        df = process_data(data)
        st.dataframe(df)
