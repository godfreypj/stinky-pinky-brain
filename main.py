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
            main.py
            '''.replace('\n', '') })
    try:
        with open('data/training_data_1.txt', 'r') as file:
            training_data = file.read()

        content = f"""
        Here are some examples of rhyming word pairs with clues:
        {training_data}
        Now, your task is to devise FOUR sets of rhyming word pairs, each with a corresponding clue. 
        Here's the structure for each set:
            Word 1: [Word]\n
            Clue 1: [A concise, evocative clue related to Word 1]\n
            Word 2: [Word, rhyming with Word 1]\n
            Clue 2: [A concise, evocative clue related to Word 2]\n\n
        Guidelines:
        * The rhyming words should be thematically connected, adding an extra layer of intrigue.
        * Aim for words that are challenging to guess but not obscure. Think "satisfyingly tricky."
        * Prioritize cleverness and originality in both word choices and clues.
        """

        model_name = "gemini-1.5-pro"
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(content, stream=True)
        def stream():
            for chunk in response:
                yield 'data: %s\n\n' % json.dumps({ "text": chunk.text })

        return stream(), {'Content-Type': 'text/event-stream'}

    except Exception as e:
        return jsonify({ "error": str(e) })


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))
