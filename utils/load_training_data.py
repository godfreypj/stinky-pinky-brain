import os

def load_training_data():
    data_dir = 'data'
    training_data = ""

    if not os.path.exists(data_dir):
        return "Error: 'data' folder not found. Please provide training data in a 'data' folder."

    txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    if not txt_files:
        return "Error: No .txt files found in 'data' folder. Please provide training data."

    for txt_file in txt_files:
        file_path = os.path.join(data_dir, txt_file)
        with open(file_path, 'r') as file:
            training_data += file.read()

    return training_data
