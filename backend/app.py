from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_bot_response  # ✅ changed from chatbot_flask to chatbot

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"response": "No message received."}), 400

    print("User:", user_message)
    bot_reply = get_bot_response(user_message)
    print("GroSafe:", bot_reply)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
