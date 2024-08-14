import os

import google.generativeai as genai
from google.cloud import secretmanager
from flask import Flask, jsonify, render_template, request, send_from_directory
from utils.load_training_data import load_training_data
from utils.load_prompt import load_prompt
from utils.format_response import format_response
from flask_cors import CORS

# Load environment variables from .env file
GEMINI_KEY = os.environ.get('GEMINI_KEY', None) 
MODEL = os.environ.get("MODEL", "gemini-1.5-flash")
SP_CONTROL = os.environ.get("SP_CONTROL", None)
PROJECT_ENV = os.environ.get("PROJECT_ENV", None)

if PROJECT_ENV != "local":
    try:
        client = secretmanager.SecretManagerServiceClient()
        print(f"PROJECT_ENV: {PROJECT_ENV}")
        name = f"projects/{PROJECT_ENV}/secrets/GEMINI_KEY/versions/latest"
        response = client.access_secret_version(request={"name": name})
        GEMINI_KEY = response.payload.data.decode("UTF-8")
    except Exception as e:
        return jsonify({"error": f"Error accessing Secret Manager: {e}"}), 500

genai.configure(api_key=GEMINI_KEY)

app = Flask(__name__, template_folder="web")
CORS(app, resources={r"/*": {"origins": SP_CONTROL}})


# Swagger
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/generate", methods=["GET"])
def generate_api():
    if SP_CONTROL is None:
        return (
            jsonify(
                {
                    "error": """
            Unable to find Stinky Pinky Control in env.
            """.replace(
                        "\n", ""
                    )
                }
            ),
            400,
        )
    try:
        # Go get the training data
        training_data = load_training_data()
        if training_data.startswith("Error:"):
            return jsonify({"error": training_data}), 500

        # Add that to the prompt
        content = load_prompt(training_data)
        if content.startswith("Error:"):
            return jsonify({"error": content}), 500

        # Give it to the robot
        model = genai.GenerativeModel(model_name=MODEL)

        # Get the response
        ai_response = ""
        for chunk in model.generate_content(content, stream=True):
            ai_response += chunk.text

        # Parse it
        parsed_data = format_response(ai_response)
        if parsed_data.get("is_error", False):
            return jsonify({"error": parsed_data.get("error_message")}), 404

        # Access and return the parsed data
        actual_data = parsed_data.get("data")
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
