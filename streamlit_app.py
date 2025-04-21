import json
import pandas as pd
import traceback
import streamlit as st
import ast

from src.mcq_gen.utils import read_file, extract_mcqs_to_df, get_gemini_feedback
from src.mcq_gen.MCQ_Gen import generate_quiz

# Load response JSON
with open('resp.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("Auto MCQ Creator with Langchain and Gemini API")

# --- Form for uploading file and entering quiz settings ---
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    level = st.text_input("Complexity level of Questions", max_chars=20, placeholder="Easy")
    mode = st.radio("Choose mode", ["Download MCQs", "Take a Quiz"])
    button = st.form_submit_button("Create MCQs")

if button and uploaded_file and mcq_count and subject and level:
    with st.spinner("Generating MCQs..."):
        try:
            text = read_file(uploaded_file)
            response = generate_quiz(text, mcq_count, subject, level, RESPONSE_JSON)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error occurred during quiz generation.")
        else:
            quiz = response.get("updated_quiz")
            analysis = response.get("complexity_analysis")
            table_data = extract_mcqs_to_df(quiz)

            if not table_data:
                st.warning("No MCQs extracted.")
            else:
                df = pd.DataFrame(table_data)
                df.index += 1

                if mode == "Download MCQs":
                    st.table(df)
                    st.text_area("Review", analysis)

                    st.session_state.csv_data = df.to_csv(index=False)
                    st.session_state.txt_data = df.to_string(index=False)
                    st.session_state.pdf_data = f"Subject: {subject}\nLevel: {level}\n\n" + df.to_string(index=True)
                    st.session_state.mcq_generated = True

                elif mode == "Take a Quiz":
                    st.session_state.quiz_df = df
                    st.session_state.quiz_data = table_data
                    st.session_state.show_quiz = True
                    st.rerun()

# --- Quiz Mode ---
if st.session_state.get("show_quiz", False):
    df = st.session_state.get("quiz_df")
    quiz_data = st.session_state.get("quiz_data")
    if df is not None:
        st.header("📝 Quiz Time")
        user_answers = []
        correct_answers = df["correct"].tolist()
        score = 0
        wrong = []

        for idx, row in df.iterrows():
            st.subheader(f"Q{idx}: {row['mcq']}")

            # Convert string to dict if needed
            if isinstance(row["options"], str):
                options_dict = ast.literal_eval(row["options"])
            else:
                options_dict = row["options"]

            user_choice = st.radio(
                f"Your answer for Q{idx}:", 
                list(options_dict.keys()), 
                format_func=lambda x: f"{x}: {options_dict[x]}",
                key=f"q_{idx}"
            )
            user_answers.append(user_choice)

        if st.button("Submit Quiz"):
            for i, row in df.iterrows():
                correct = row["correct"]
                user = user_answers[i - 1]
                if user == correct:
                    score += 1
                else:
                    wrong.append((str(i), user, correct))

            st.success(f"🎉 You scored {score} out of {len(correct_answers)}.")
            st.session_state.show_quiz = False

            if wrong:
                st.header("🧠 Review Your Mistakes")

                for qid, user_ans, correct_ans in wrong:
                    q_index = int(qid) - 1
                    question_obj = quiz_data[q_index]

                    mcq_text = question_obj["mcq"]
                    options = question_obj["options"]

                    feedback = get_gemini_feedback(mcq_text, user_ans, correct_ans)

                    st.markdown(f"**Q{qid}: {mcq_text}**")
                    st.markdown(f"**Your answer:** {user_ans} - {options.get(user_ans, 'N/A')}")
                    st.markdown(f"**Correct answer:** {correct_ans} - {options.get(correct_ans, 'N/A')}")
                    st.markdown("📝 **Gemini's Feedback:**")
                    st.info(feedback)

# --- Download Section ---
if 'mcq_generated' in st.session_state and st.session_state.mcq_generated:
    st.subheader("📥 Download Your MCQs")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button("Download as CSV", data=st.session_state.csv_data, file_name="mcqs.csv", mime="text/csv")
    with col2:
        st.download_button("Download as TXT", data=st.session_state.txt_data, file_name="mcqs.txt", mime="text/plain")
    with col3:
        st.download_button("Download as PDF", data=st.session_state.pdf_data, file_name="mcqs.pdf", mime="application/pdf")
