from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

def get_bot_response(message):
    response = ollama.chat(model='qwen:0.5b', messages=[{'role': 'user', 'content': message}])
    return response['message']['content']

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = get_bot_response(prompt)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
