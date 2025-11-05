from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from config.configuration import load_config
from backend.chatbot import ChatBot

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Load configuration
parameters = load_config()

# Initialize chatbot
chatbot = ChatBot(parameters)

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": f"Resume Chatbot API for {parameters['resume_owner_name']}",
        "version": "2.0-simplified"
    })

@app.route("/ask", methods=["POST"])
def ask():
    """
    Main endpoint to ask questions about the resume.
    
    Request body:
    {
        "question": "Your question here"
    }
    
    Response:
    {
        "answer": "The chatbot's response",
        "status": "success"
    }
    """
    try:
        # Get question from request
        data = request.json
        question = data.get("question", "").strip()
        
        # Validate question
        if not question:
            return jsonify({
                "error": "No question provided",
                "status": "error"
            }), 400
        
        # Generate response using chatbot
        # Note: conversation=[] means no history (stateless)
        response = chatbot.answer(
            query=question,
            conversation=[],
            fake_conversation=False
        )
        
        return jsonify({
            "answer": response["answer"],
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
