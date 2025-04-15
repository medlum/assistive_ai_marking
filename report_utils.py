import zipfile
from pathlib import Path
import shutil
import re
import pandas as pd
import streamlit as st
from docx import Document
from pypdf import PdfReader


def extract_name_id(data):
     # Match "Name / Student ID" and capture the first non-empty line that follows it
    pattern = r"Name\s*/\s*Student ID\s*\n(?:\s*\n)*([A-Za-z \-']+\s*/?\s*[A-Za-z0-9]+)"
    match = re.search(pattern, data)
    if match:
        return match.group(1).strip()
    else:
        return "Name and student ID not found."
    

def extract_and_read_files(zip_path):

    extracted_data = {}
    data = ""

    # Define extraction path
    extract_folder = "extracted_files"
    if Path(extract_folder).exists():
        shutil.rmtree(extract_folder)

    # Extract ZIP file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

    for file in Path(extract_folder).iterdir(): 
            
        if file.suffix.lower() == ".docx":
            doc = Document(file)
            data = "\n".join([para.text for para in doc.paragraphs])
        
        elif file.suffix.lower() == ".pdf":    
            reader = PdfReader(file)
            for page in reader.pages:
                data += page.extract_text()

        else:
            st.error("Zip file not found")

        student_name_id = extract_name_id(data)

        if student_name_id not in extracted_data:
            # store values as a list with file extension and extracted data
            extracted_data[student_name_id] = [file.suffix.lower(), data]
           
    return extracted_data



def process_data(data):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    df['Total'] = df.select_dtypes(include='number').sum(axis=1)

    return df

system_message = """
1. Your primary task is to evaluate students' written assignments based on a structured marking rubric.  
2. Follow the instructions to mark:
    - Refer to the provided marking rubric to ensure accurate grading.
    - Assess each criterion separately, assigning marks accordingly.  
    - Mark the report with a high standard.
    - Do not assign more than the maximum mark in each marking criterion.
    - Provide a detail feedback by identifying specific strengths and weaknesses of the report, offering constructive criticism on areas needing improvement. 
    - Contextualize the feedback to the student's role and company he/she is interning. 
    - Provide reasons on the marks given for each criterion.
    - Tally the marks in each criterion.
    - Comment on why the marks are given for each criteria as part of the feedback.
    - Return the marks and feedback in a dictionary : 
      {
          'Student Name': str,
          'Content (30 marks)': float,
          'Organisation and Structure (10 marks)': float,
          'Referencing (10 marks)': float,
          'Feedback' : str
      }  
    - Use single quotation '' for strings in the dictionary.
    - Your answer should only contain the returned dictionary and nothing else. 
"""

# custom CSS for buttons
btn_css = """
<style>
    .stButton > button {
        color: #383736; 
        border: none; /* No border */
        padding: 5px 22px; /* Reduced top and bottom padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 8px !important;
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 30px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }
    .stButton > button:hover {
        color: #383736; 
        background-color: #c4c2c0; /* Darker green on hover */
    }
</style>
"""

image_css = """
<style>
.stImage img {
    border-radius: 50%;
    #border: 5px solid #f8fae6;
}
</style>

"""
