from flask import Flask, request, jsonify
from llama_wrapper import get_completion
from utils import handle_user_message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chatbot', methods=['POST'])
def chatbot_api():
    user_message = request.get_json()['message']
    response = handle_user_message(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)