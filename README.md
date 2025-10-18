# ChatBot_using_gemini

## Live Demo

[Click here to try the chatbot live](https://ai-chatbot-1-0.onrender.com/)

This is a small Flask app that forwards chat messages to the Groq API.

## Setup (Windows PowerShell)

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:

```
API_KEY=your_groq_api_key_here
```

4. Run the app:

```powershell
python app.py
```

## Push to GitHub

```powershell
git init
git add .
git commit -m "Initial commit"
# create a repo on GitHub and then:
git remote add origin https://github.com/<your-username>/<repo>.git
git branch -M main
git push -u origin main
```

Notes:
- `.env` is ignored by `.gitignore` to avoid leaking secrets.
- For production, consider using a proper WSGI server and securing your API key.
