import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

from PyPDF2 import PdfReader
import pandas as pd
import numpy as np

load_dotenv()

app = Flask(__name__)

# ✅ Load Groq API key
GROQ_API_KEY = os.getenv("API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Set 'API_KEY' in .env file.")

# ✅ Groq-compatible model (works!)
GROQ_MODEL = "llama-3.3-70b-versatile"

# ✅ Groq endpoint
API_URL = "https://api.groq.com/openai/v1/chat/completions"
# API_URL = "https://console.groq.com/docs/deprecations"


# In-memory storage for uploaded file text
uploaded_text = ""

def extract_file_text(file):
    filename = file.filename.lower()
    text = ""
    if filename.endswith('.pdf'):
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif filename.endswith('.txt'):
        text = file.read().decode('utf-8')
    elif filename.endswith('.csv'):
        df = pd.read_csv(file)
        text = df.to_string()
    else:
        raise ValueError("Unsupported file type. Please upload a PDF, TXT, or CSV file.")
    return text

@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_text
    file = request.files.get('file')
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    try:
        uploaded_text = extract_file_text(file)
        return jsonify({
            "message": "File uploaded and text extracted successfully.",
            "extracted_text": uploaded_text[:500]  # Return first 500 characters as a sample
        }), 200
    except ValueError as ve:
        return jsonify({
            "error": str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"An error occurred while processing the file: {str(e)}"
        }), 500
        



def generate_response(prompt, history=None):
    """Send a chat completion request to Groq API."""
    global uploaded_text
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = "You are a helpful AI assistant."
    if uploaded_text:
        system_prompt += f" Use the following context from the uploaded document to answer questions:\n{uploaded_text}"

    # Ensure history is a list
    messages = [{"role": "system", "content": system_prompt}]
    if history and isinstance(history, list):
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # 🔍 Log response if something goes wrong
    if response.status_code != 200:
        print("Groq API error:", response.status_code, response.text)
        response.raise_for_status()

    # response= response+'\n'
    data = response.json()
    return data["choices"][0]["message"]["content"]


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question")
    history = data.get("history", [])

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = generate_response(question, history)
        return jsonify({"answer": answer})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"Groq API error: {e.response.text}"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    # this is for hosting on cloud server
    app.run(host='0.0.0.0', port=5000, debug=True)
    # this is for local hosting
    # app.run(port=8080, debug=True)

