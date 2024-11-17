from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def train_model_on_corpus(file_paths):
    """
    Dummy function for training the model on corpus files.
    """
    print(f"Training on {len(file_paths)} files...")
    for file in file_paths:
        print(f"Processing: {file}")
    print("Training completed.")

def generate_text(prompt, max_length=150):
    """
    Generate text based on the given prompt using GPT-2.

    Parameters:
    prompt (str): Input text to guide the text generation.
    max_length (int): Maximum length of the generated text.

    Returns:
    str: Generated text.
    """
    # Encode the prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    # Generate text
    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_p=0.95,
        temperature=0.7,
    )

    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text
