import os


def load_prompt(training_data):
    data_dir = "data"
    prompt = ""

    if not os.path.exists(data_dir):
        return {
            "is_error": True,
            "error_message": "Error: 'data' folder not found. Please provide training data in a 'data' folder.",
        }

    prompt_file = [f for f in os.listdir(data_dir) if f == "prompt.txt"]
    if not prompt_file:
        return {
            "is_error": True,
            "error_message": f"Error: No prompt found. Please provide a 'prompt.txt' file in the 'data' folder.",
        }

    prompt_file = open(os.path.join(data_dir, prompt_file[0]), "r")

    for line in prompt_file:
        prompt += line

    if prompt.strip() == "":
        return {
            "is_error": True,
            "error_message": f"Error: Prompt is empty. Please provide a non-empty 'prompt.txt' file in the 'data' folder.",
        }

    # Add the training data
    prompt += f"""
        Here are some examples:
        {training_data}
        """

    # Add the desired response format
    prompt += f"""
    Provide the output in the following JSON format:
    "word1": "[Word]"
    "clue1": "[Clue related to Word 1]"
    "word2": "[Word, rhyming with Word 1]"'
    "clue2": "[Clue related to Word 2]"
    """
    return {
            "is_error": False,
            "prompt": prompt,
        }
        
