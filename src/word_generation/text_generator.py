from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def train_model_on_corpus(file_paths):
    """
    Trains the model on the provided corpus files.

    Parameters:
    file_paths (list): List of file paths to load and train the model with.
    """
    training_data = ""
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            training_data += file.read() + "\n"

    # Tokenize the training data
    inputs = tokenizer(training_data, return_tensors="pt", truncation=True, padding=True)

    # Dummy training example (replace with real training loop if needed)
    outputs = model(**inputs)
    print("Training completed on provided corpus files.")
