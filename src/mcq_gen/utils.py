from PyPDF2 import PdfReader
import traceback
import re
import json
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDH6xjBdvs8TxshjRj_ragfCMwYd14O_wk")

# Load model
model = genai.GenerativeModel("gemini-1.5-pro")

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format, only PDF and text files supported")

def extract_mcqs_to_df(quiz_str):
    try:
        # Regular expression to extract MCQs, options, and answers
        pattern = r'"mcq": "(.*?)".*?"options": \{(.*?)\}.*?"correct": "(.*?)"'
        matches = re.findall(pattern, quiz_str, re.DOTALL)

        quiz_data = []
        for mcq, options_str, correct in matches:
            options_pattern = r'"([a-d])": "(.*?)"'
            options = re.findall(options_pattern, options_str)

            question = {
                "mcq": mcq.strip(),
                "options": {key: value.strip() for key, value in options},
                "correct": correct.strip(),
            }
            quiz_data.append(question)
        
        return quiz_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

def get_gemini_feedback(mcq, user_ans, correct_ans):
    prompt = f"""
You are an expert in machine learning.

Question: "{mcq}"
User's Answer: "{user_ans}"
Correct Answer: "{correct_ans}"

suggest what topic or concept they should review to improve their understanding.
Give a review topic only. Make sure response should be in the format of:
need to review topic: topic and concept name only. 
Web urls : best websites to learn that particular topic. Not more than 3 suggestions. 
"""

    response = model.generate_content(prompt)
    return response.text.strip()
