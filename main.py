import os

import google.generativeai as genai
from flask import Flask, jsonify, render_template, request, send_from_directory
from utils.load_training_data import load_training_data
from utils.load_prompt import load_prompt
from utils.format_response import format_response
from utils.load_config import load_config
from flask_cors import CORS

# Load configuration
try:
    config = load_config()
    GEMINI_KEY = config["GEMINI_KEY"]
    MODEL = config["MODEL"]
    SP_CONTROL = config["SP_CONTROL"]
    PROJECT_ID = config["PROJECT_ID"]
except Exception as e:
    raise RuntimeError("Unable to load configuration", e)

app = Flask(__name__, template_folder="web")
CORS(app, resources={r"/*": {"origins": SP_CONTROL}})
genai.configure(api_key=GEMINI_KEY)

# Swagger
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/generate", methods=["GET"])
def generate_api():
    try:
        # Go get the training data
        training_data = load_training_data()
        if training_data.get("is_error", True):
            return jsonify({"error": training_data.get("error_message")}), 500

        # Add that to the prompt
        prompt = load_prompt(training_data.get("training_data"))
        if prompt.get("is_error", True):
            return jsonify({"error": prompt.get("error_message")}), 500

        # Give it to the robot
        model = genai.GenerativeModel(model_name=MODEL)

        # Get the response
        ai_response = ""
        for chunk in model.generate_content(prompt.get("prompt"), stream=True):
            ai_response += chunk.text

        # Parse it
        formatted_response = format_response(ai_response)
        if formatted_response.get("is_error", True):
            return jsonify({"error": formatted_response.get("error_message")}), 404

        # Access and return the parsed data
        actual_data = formatted_response.get("formatted_response")
        return jsonify({"text": actual_data}), 200, {"Content-Type": "application/json"}
    except Exception as e:
        print("JSON Parsing Error:", e)
        with app.app_context():
            return jsonify({"error": str(e)})


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("web", path)


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
