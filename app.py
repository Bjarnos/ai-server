import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://bjarnos.github.io"])

# Groq API config
dotenv.load_dotenv()
GROQ_API_KEY = os.environ.get('api_key')
GROQ_API_URL = 'https://api.groq.ai/v1/chat/completions'

# Function to interact with the Groq API
def get_groq_chat_response(messages):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "messages": messages,
        "model": "llama-3.1-8b-instant"  # You can modify the model name as needed
    }

    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        response_data = response.json()
        bot_response = response_data['choices'][0]['message']['content'] if response_data else "Sorry, I couldn't process your request."
        return bot_response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    messages = request.json.get('messages', [])  # Receive the current chat history as well

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Add user message to the history
    messages.append({"role": "user", "content": user_message})

    # Get AI response from Groq
    ai_response = get_groq_chat_response(messages)

    # Add AI response to the history
    messages.append({"role": "assistant", "content": ai_response})

    # Return the AI response and the updated history
    return jsonify({
        "response": ai_response,
        "messages": messages  # Returning updated history for the client to maintain
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
