import streamlit as st
# import os
# from PIL import Image
import PyPDF2 as pdf
import google.generativeai as genai

GOOGLE_API = 'AIzaSyCdP-mKZjOqClld2oMq_LA3oIFIiOeOi6U'

genai.configure(api_key=GOOGLE_API)


def getGeminiResponse(input_prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_prompt)
    return response.text


def inputPdftext(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text


st.title("Application Tracking System")
st.subheader("Improve your resume with ATS system by Google Gemini Pro")
jd = st.text_area("Enter your job Description")
uploaded_file = st.file_uploader(
    "Upload your Resume in PDF format",
    type='pdf'
    )

button = st.button("submit")

if button:
    if uploaded_file is not None:
        text = inputPdftext(uploaded_file)

        input_prompt = f"""
            Hey Act Like a skilled or very experience ATS
            (Application Tracking System). Your task is to evaluate the resume
            based on the given job description. You must consider the job
            market is very competitive and you should provide best assistance
            for improving thr resumes. Assign the percentage Matching based
            on Jd and the missing keywords with high accuracy.
            resume:{text}
            description:{jd}

            I want the response in one single string having the structure and
            with proper structure
            {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
        """

        response = getGeminiResponse(input_prompt)
        st.write(response)
