import json
import os

import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory

API_KEY = os.environ.get('API_KEY', 'TODO')
genai.configure(api_key=API_KEY)

app = Flask(__name__)


@app.route("/api/generate", methods=["GET"])
def generate_api():
    if API_KEY == 'TODO':
        return jsonify({ "error": '''
            To get started, get an API key at
            https://g.co/ai/idxGetGeminiKey and enter it in
            .env
            '''.replace('\n', '') })
    try:
        with open('data/training_data_1.txt', 'r') as file:
            training_data = file.read()

        content = f"""
        Here are some examples of rhyming word pairs with clues:
        {training_data}
        Now, your task is to devise ONE sets of rhyming word pairs, each with a corresponding clue. 
        Provide the output in the following JSON format:
        "word1": "[Word]", "clue1": "[A concise, evocative clue related to Word 1]", 
        "word2": "[Word, rhyming with Word 1]", "clue2": "[A concise, evocative clue related to Word 2]"
        Guidelines:
        * The rhyming words should be thematically connected, adding an extra layer of intrigue.
        * Aim for words that are challenging to guess but not obscure. Think "satisfyingly tricky."
        * Prioritize cleverness and originality in both word choices and clues.
        """

        model_name = "gemini-1.5-pro"
        model = genai.GenerativeModel(model_name=model_name)
        full_response = ""
        for chunk in model.generate_content(content, stream=True):
            full_response += chunk.text
        
        # Parse the response into a structured format (you'll likely need to adjust this based on the exact format you want)

        # full_response = full_response.strip()

        full_response = full_response\
        .replace("```json\n", "")\
        .replace("","").replace("```", "")
        # Split the response into lines
        # Parse the JSON response
        parsed_data = json.loads(full_response)
        print("Parsed Data:", parsed_data)
        # print("Parsed data" +parsed_data)
        # Access the words and clues
        word1 = parsed_data["word1"]
        clue1 = parsed_data["clue1"]
        word2 = parsed_data["word2"]
        clue2 = parsed_data["clue2"]

        parsed_data = {
            "word1": word1,
            "clue1": clue1,
            "word2": word2,
            "clue2": clue2
        }

        return jsonify({"text": parsed_data}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print("JSON Parsing Error:", e)
        with app.app_context():
            return jsonify({ "error": str(e) })



@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))
