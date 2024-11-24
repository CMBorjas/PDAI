import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Define optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

# Directory to save checkpoints
CHECKPOINT_DIR = "checkpoints"

if not os.path.exists(CHECKPOINT_DIR):
    os.makedirs(CHECKPOINT_DIR)

def save_checkpoint(model, optimizer, epoch, file_path):
    """
    Save the training state to a checkpoint file.
    """
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "epoch": epoch,
    }
    torch.save(checkpoint, file_path)
    print(f"Checkpoint saved to {file_path}")

def load_checkpoint(file_path):
    """
    Load the training state from a checkpoint file.
    """
    checkpoint = torch.load(file_path)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint["epoch"]
    print(f"Checkpoint loaded from {file_path}, starting at epoch {epoch}")
    return epoch

def train_model_on_corpus(file_paths, num_epochs=5, checkpoint_interval=1):
    """
    Train the GPT-2 model on the provided corpus files with checkpointing.

    Parameters:
    - file_paths: List of file paths to the training corpus.
    - num_epochs: Number of epochs for training.
    - checkpoint_interval: Save checkpoint every `checkpoint_interval` epochs.
    """
    # Load checkpoint if it exists
    latest_checkpoint = os.path.join(CHECKPOINT_DIR, "latest_checkpoint.pth")
    start_epoch = 0
    if os.path.exists(latest_checkpoint):
        start_epoch = load_checkpoint(latest_checkpoint)

    # Training loop
    model.train()
    for epoch in range(start_epoch, num_epochs):
        for file_path in file_paths:
            try:
                # Read file with error handling for invalid encoding
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()

                # Tokenize and prepare input
                inputs = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=512)

                # Forward pass
                outputs = model(inputs, labels=inputs)
                loss = outputs.loss

                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                print(f"Epoch {epoch + 1}/{num_epochs}, File: {file_path}, Loss: {loss.item()}")

            except Exception as e:
                # Handle file reading errors gracefully
                print(f"Error processing file {file_path}: {e}")

        # Save checkpoint periodically
        if (epoch + 1) % checkpoint_interval == 0:
            save_checkpoint(model, optimizer, epoch + 1, latest_checkpoint)

    # Final checkpoint after training
    save_checkpoint(model, optimizer, num_epochs, latest_checkpoint)
    print("Training complete.")

def generate_text(prompt, max_length=150):
    """
    Generate text using the GPT-2 model.

    Parameters:
    - prompt: The initial text prompt for generation.
    - max_length: Maximum length of the generated text.

    Returns:
    - The generated text as a string.
    """
    model.eval()

    # Tokenize the input prompt
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
