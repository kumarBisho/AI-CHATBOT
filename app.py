import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

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


def generate_response(prompt, history=None):
    """Send a chat completion request to Groq API."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Ensure history is a list
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
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
    app.run(host='0.0.0.0', port=5000, debug=True)

