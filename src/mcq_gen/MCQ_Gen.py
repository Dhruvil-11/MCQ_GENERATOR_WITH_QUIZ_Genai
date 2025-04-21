import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain



def load_template(file_path):
    """Utility function to read the combined template from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def generate_quiz(TEXT, NUMBER, SUBJECT, LEVEL, RESPONSE_JSON):
    # Load combined template from a .txt file
    combined_template = load_template('TEMPLATES.txt')

    # Split the combined template into parts for different purposes
    templates = combined_template.split('\n\n')

    # Define prompt templates using the split parts
    quiz_generation_prompt = PromptTemplate(
        input_variables=["text", "number", "subject", "level", "response_json"],
        template=templates[0]
    )

    quiz_evaluation_prompt = PromptTemplate(
        input_variables=["quiz"],
        template=templates[1]
    )

    complexity_analysis_prompt = PromptTemplate(
        input_variables=["updated_quiz", "subject"],
        template=templates[2]
    )

    # Read the API key
    with open('api_key.txt2', 'r') as file:
        KEY = file.read()

    os.environ["GOOGLE_API_KEY"] = KEY

    model_options = ["gemini-1.5-pro", "gemini-1.5-flash-8b"]
    for model in model_options:
        try:
            llm = ChatGoogleGenerativeAI(model=model)
            
            generate_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
            evaluate_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="updated_quiz", verbose=True)
            analysis_chain = LLMChain(llm=llm, prompt=complexity_analysis_prompt, output_key="complexity_analysis", verbose=True)

            gen_eval_analysis_chain = SequentialChain(
                chains=[generate_chain, evaluate_chain, analysis_chain],
                input_variables=["text", "number", "subject", "level", "response_json"],
                output_variables=["updated_quiz", "complexity_analysis"],
                verbose=True,
            )

            return gen_eval_analysis_chain({
                "text": TEXT,
                "number": NUMBER,
                "subject": SUBJECT,
                "level": LEVEL,
                "response_json": json.dumps(RESPONSE_JSON),
            })

        except Exception as e:
            print(f"Error with model {model}: {e}")
            print("Trying again with the next available model...")

    raise RuntimeError("All models failed to generate the quiz.")