from flask import Flask, request, jsonify
from llama_wrapper import get_completion
from utils import handle_user_message

app = Flask(__name__)

@app.route('/')
def home():
    """Welcome message for the NP data API."""
    return "Welcome to the NP data API!"


@app.route('/chatbot', methods=['POST'])
def chatbot_api():
    user_message = request.get_json()['message']
    response = handle_user_message(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)