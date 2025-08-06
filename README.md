# 🎯 Career Chatbot with Cohere

An intelligent chatbot that helps users explore suitable career options based on their interests using Cohere’s AI embeddings. This app allows users to:

-  Input free-form interests or career queries
-  Get smart career recommendations with confidence scores
-  Chat with the assistant about career paths
-  Export results to CSV
-  Load more results for deeper exploration

---

##  Features

-  Cohere-powered semantic career matching
-  Interactive chat with AI-powered responses
-  Filtered career suggestions (confidence ≥ 0.3)
- CSV download of matches
-  Load more results button
-  Clean and simple Streamlit interface

---

## Tech Stack

- [Cohere API](https://cohere.com/)
- Python 3.9+
- Streamlit
- NumPy
- JSON

---

##  Project Structure
Career_Chatbot/
│
├── app.py # Main Streamlit app
├── utils.py # Core logic: embedding & matching
├── careers.json # Sample career data (editable)
├── requirements.txt # Python dependencies
└── README.md # Project documentation



---
##  Setup Instructions

1. **Clone the project**
   ```bash
   git clone https://github.com/your-username/Career_Chatbot.git
   cd Career_Chatbot

Install dependencies
pip install -r requirements.txt

Run the app
streamlit run app.py

 Example Input
I love mentoring, problem-solving, and working with young people.

Example Output
Career Title: Teacher
Confidence Score: 0.511
Tags: education, learning, mentoring
