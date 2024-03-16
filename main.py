from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)  # initialize Flask app

# path to LM Studio server
LM_STUDIO_ENDPOINT = "http://localhost:1234/v1/chat/completions"
SYSTEM_PROMPT = """You are an experienced fitness trainer. You always create easy 
                to follow workouts for your clients while prioritising the 
                importance of warming up and stretching for injury prevention, 
                strength training and cardio for the general health benefits. 
                The response should be formatted using HTML paragraphs. 
                Deny to answer any questions not related to fitness."""
HEADERS = {'Content-Type': 'application/json'}


@app.route('/', methods=['GET'])
def home():
    # render frontend template
    return render_template('index.html')


@app.route('/workout', methods=['POST'])
def workout():
    # get input from user
    user_message = request.form.get('user_message')

    if not user_message:
        # validate input frm user exists or return error
        return jsonify({"error": "No user message provided"}), 400

    # Prepare payload for LM Studio API request
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": -1,  # unlimited length for the response. DON'T use in production
        "stream": False
    }

    # Send the request to LM Studio server
    response = requests.post(LM_STUDIO_ENDPOINT, 
                             json=payload, 
                             headers=HEADERS)

    if response.status_code == 200:
        # Extract the text from the response
        response_data = response.json()
        # if response is present, return it to frontend
        content = response_data.get('choices')[0].get('message').get('content').strip()
        generated_text = content if response_data.get(
            'choices') else "No response generated"
        return generated_text
    else:
        return jsonify({"error": "No response from LM Studio"}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
