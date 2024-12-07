import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import dotenv

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://bjarnos.github.io"}})

# Load environment variables (from Koyeb)
dotenv.load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("api_key"),  # Secured
)

# Function to interact with the Groq API
def get_groq_chat_response(messages):
    try:
        # Send messages to Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"  # You can change the model
        )
        
        # Extract and return the assistant's response
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request. Please try again later."

# Define the chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    # Extract messages from the request body
    messages = request.json.get('messages', [])
    
    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    # Get and add the AI response from Groq
    ai_response = get_groq_chat_response(messages)
    messages.append({"role": "assistant", "content": ai_response})

    # Return the assistant's response and updated message history
    return jsonify({
        "response": ai_response,
        "messages": messages
    })

# Start the Flask server (handles http requests)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
