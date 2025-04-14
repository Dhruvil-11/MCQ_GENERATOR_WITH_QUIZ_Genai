# Automated MCQ Generation with LangChain 🔗 and Gemini API 🚀

This repository provides a streamlined solution for creating multiple-choice quizzes (MCQs) using advanced AI models and frameworks like **LangChain**. With an automated, chain-based workflow, users can generate, evaluate, and analyze quizzes tailored to specific subjects and difficulty levels.

---

## Features

### 1. **Quiz Generation 🧠**
- **Purpose:** Automatically generate MCQs based on input text.
- **Output:** JSON-formatted questions with options and answers.

### 2. **Quiz Evaluation ✍️**
- **Purpose:** Refine and optimize quizzes to meet desired standards.
- **Output:** Revised MCQs adjusted for the target audience.

### 3. **Complexity Analysis 🔍**
- **Purpose:** Assess question difficulty and provide a concise summary.
- **Output:** A brief analysis of quiz complexity.

### Sequential Workflow 🔄
- Combines the above steps using a **SequentialChain** from LangChain.
- Automates the end-to-end process from input to final output.

---

## Project Structure

```
Auto-MCQ-Creator-using-Langchain-and-Gemini-API-master/
├── assets/                # Contains demo video files
├── exp/                   # Experimental notebooks and data
├── logs/                  # Log files for debugging
├── src/                   # Source code for the project
│   ├── mcq_gen/           # Core MCQ generation modules
│   │   ├── MCQ_Gen.py     # Main script for generating MCQs
│   │   ├── logger.py      # Logging utilities
│   │   └── utils.py       # Helper functions
├── streamlit_app.py       # Streamlit-based user interface
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── setup.py               # Package setup script
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Basic understanding of Python and LangChain

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

### Running the Streamlit App
1. Launch the application:
   ```bash
   streamlit run streamlit_app.py
   ```
2. Open the provided URL in your browser to interact with the app.

---

## Usage

1. **Input**: Provide the source text, desired number of questions, subject, and difficulty level.
2. **Process**: The app executes a sequential workflow:
   - Generates questions.
   - Evaluates and refines them.
   - Analyzes their complexity.
3. **Output**: Download the final MCQs and complexity summary in JSON format.

---

## Live Demo

Check out the demo video in the `assets/` folder (`Live_Demo.mp4`) for a detailed walkthrough of the app's capabilities.

---

## Contributing

We welcome contributions! Here’s how you can help:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [LangChain](https://www.langchain.com/) for its robust framework.
- [Gemini API](https://www.example.com/gemini-api-docs) for its capabilities in NLP.

---

Enjoy creating intelligent, tailored quizzes with ease! 💡🎉

