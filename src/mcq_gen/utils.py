from PyPDF2 import PdfReader
import traceback
import re
import json
import google.generativeai as genai

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

        # Find all matches
        matches = re.findall(pattern, quiz_str, re.DOTALL)

        # Process each match
        quiz_data = []
        for mcq, options_str, correct in matches:
            # Extract individual options
            options_pattern = r'"([a-d])": "(.*?)"'
            options = re.findall(options_pattern, options_str)

            # Create a dictionary for the question
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


def review_incorrect_answers(user_answers, quiz_data):
    review = {"wrong_answers": []}

    for qid, user_ans in user_answers.items():
        correct_ans = quiz_data[qid]['correct']
        if user_ans != correct_ans:
            review["wrong_answers"].append({
                "question_no": qid,
                "your_answer": user_ans,
                "correct_answer": correct_ans,
                "explanation": generate_explanation(qid, quiz_data),
                "suggest_review": suggest_topic(qid, quiz_data)
            })
    return review

def generate_explanation(qid, quiz_data):
    mcq = quiz_data[qid]['mcq']
    if "classification" in mcq.lower():
        return "Classification assigns inputs to categories using labeled data."
    elif "foundation" in mcq.lower():
        return "Training data forms the base for any ML model to learn from."
    elif "type of ML" in mcq.lower() or "category" in mcq.lower():
        return "Common ML categories include Supervised, Unsupervised, and Reinforcement."
    return "Review the concepts discussed in this question."

def suggest_topic(qid, quiz_data):
    mcq = quiz_data[qid]['mcq']
    if "classification" in mcq.lower():
        return "Supervised Learning - Classification"
    elif "foundation" in mcq.lower():
        return "Basics of Machine Learning"
    elif "category" in mcq.lower() or "type of ML" in mcq.lower():
        return "Types of Machine Learning"
    return "General ML Concepts"


# for review |||||||||||||



# Configure Gemini API
genai.configure(api_key="AIzaSyDH6xjBdvs8TxshjRj_ragfCMwYd14O_wk")

# Load model
model = genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_feedback(mcq, user_ans, correct_ans):
    prompt = f"""
You are an expert in machine learning.

Question: "{mcq}"
User's Answer: "{user_ans}"
Correct Answer: "{correct_ans}"

Explain why the user's answer is incorrect. Also, suggest what topic or concept they should review to improve their understanding.
Give a short explanation and a review topic.
"""

    response = model.generate_content(prompt)
    return response.text.strip()
def review_incorrect_answers(user_answers, quiz_data):
    review = {"wrong_answers": []}

    for qid, user_ans in user_answers.items():
        correct_ans = quiz_data[qid]['correct']
        if user_ans != correct_ans:
            feedback = get_gemini_feedback(
                quiz_data[qid]['mcq'],
                user_ans,
                correct_ans
            )
            explanation, suggest_review = feedback.split("\n", 1) if "\n" in feedback else (feedback, "")
            review["wrong_answers"].append({
                "question_no": qid,
                "your_answer": user_ans,
                "correct_answer": correct_ans,
                "explanation": explanation.strip(),
                "suggest_review": suggest_review.strip()
            })
    return review
