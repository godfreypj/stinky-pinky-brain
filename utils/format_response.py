import os
import json

import json


def format_response(ai_response):
    if not ai_response:
        return {
            "is_error": True,
            "error_message": "No AI Response found! Check main.py",
        }

    # Split the response into lines
    ai_response = (
        ai_response.replace("```json\n", "").replace("", "").replace("```", "")
    )

    # Parse the JSON response
    parsed_data = json.loads(ai_response)

    # Access the words and clues
    word1 = parsed_data["word1"]
    clue1 = parsed_data["clue1"]
    word2 = parsed_data["word2"]
    clue2 = parsed_data["clue2"]

    parsed_data = {"word1": word1, "clue1": clue1, "word2": word2, "clue2": clue2}

    return {"is_error": False, "data": parsed_data}
