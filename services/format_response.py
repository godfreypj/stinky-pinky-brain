import os
import json

import json

def format_response(ai_response):
    """
    Parses AI response, extracting 'word1', 'clue1', 'word2', 'clue2' as JSON.

    Args:
        ai_response (str): Raw AI response.

    Returns:
        dict: 
            - is_error (bool): True if parsing failed.
            - error_message (str, optional): Error details if `is_error` is True.
            - formatted_response (dict, optional): Extracted data if successful.
    """
    if not ai_response or ai_response.strip() == "":
        return {
            "is_error": True,
            "error_message": "Error: No AI Response found! Check main.py",
        }

    # Split the response into lines
    ai_response = (
        ai_response.replace("```json\n", "").replace("", "").replace("```", "")
    )
    
    try:
        formatted_response = json.loads(ai_response)

        word1 = formatted_response["word1"]
        clue1 = formatted_response["clue1"]
        word2 = formatted_response["word2"]
        clue2 = formatted_response["clue2"]

        formatted_response = {"word1": word1, "clue1": clue1, "word2": word2, "clue2": clue2}

        return {"is_error": False, "formatted_response": formatted_response}

    except json.JSONDecodeError as e:
        return {
            "is_error": True,
            "error_message": f"Error parsing AI response: {e}"
        }