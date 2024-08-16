# Stinky Pinky Brain

## 🧠 Overview
This application is the brain for the Stinky Pinky Word game powered by a large language model. It provides an API endpoint to generate word pairs and clues for the game.

## 🙇‍♂️ Generate Request:
The frontend of the game sends a request to the `api/generate` endpoint. The application then:

### 1. Loads Training Data
> Training data must be provided in the form of .txt files in the `data` folder.

### 2. Loads a Prompt
> A prompt must be provided in the form of a .txt file in the `data` folder. The desired format for the response is added

### 3. LLM Interaction
> The combined data is sent to the specified LLM to generate a response.

### 4. Response Parsing
> The LLM's response - expected to be in JSON format - is parsed to extract word pairs and clues. The extracted data is returned to the frontend in JSON format.

## 💿 Project IDX
This project is designed to work within the Google Project IDX environment. The `.nix` file provides the necessary configuration and dependencies for the applications environment.

## 🗒️ Configuration
The `.env` file contains the following environment variables:
API Key: Obtain a Gemini API key and set it in the .env file:
```bash
GEMINI_KEY = 'YOUR_GEMINI_KEY'
MODEL = 'YOUR_MODEL'
```

## 🦒 Getting Started
The `.nix` file will not only install the `requirements.txt` but boot up the application as well.
If the app is killed, restart with:

```bash
./devserver.sh 5000
```

## 📄 License
This project is licensed under the so and so License.
