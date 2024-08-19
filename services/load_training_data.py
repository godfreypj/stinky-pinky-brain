import os


def load_training_data():
    """
    Loads training data from .txt files in the 'data' directory.

    Returns:
        dict:
            - is_error (bool): True if an error occurred during loading.
            - error_message (str, optional): Error details if `is_error` is True.
            - training_data (str, optional): The concatenated content of .txt files if successful.

    Functionality:
        - Checks for the existence of the 'data' directory and .txt files within it.
        - Reads and concatenates the content of all .txt files in the 'data' directory.
    """
    data_dir = "data"
    training_data = ""

    if not os.path.exists(data_dir):
        return {
            "is_error": True,
            "error_message": f"Error: 'data' folder not found. Please provide training data in a 'data' folder."
        }

    txt_files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    if not txt_files:
        return {
            "is_error": True,
            "error_message": "Error: No .txt files found in 'data' folder. Please provide training data."
        }

    for txt_file in txt_files:
        file_path = os.path.join(data_dir, txt_file)
        with open(file_path, "r") as file:
            training_data += file.read()

    if training_data.strip() == "":
        return {
            "is_error": True,
            "error_message": "Error: Training data is empty. Please provide valid training data."
            }

    return {
        "is_error": False,
        "training_data": training_data
    }
