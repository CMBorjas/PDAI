import os
from tkinter import simpledialog, messagebox
from word_generation.text_generation import train_model_on_corpus

# Path to the corpus directory
CORPUS_DIR = "PDAI/data/corpus"

def query_and_train_model():
    # Check if the corpus directory exists
    if not os.path.exists(CORPUS_DIR):
        messagebox.showerror("Error", f"The directory '{CORPUS_DIR}' does not exist.")
        return

    # Get the list of files in the corpus directory
    corpus_files = [f for f in os.listdir(CORPUS_DIR) if os.path.isfile(os.path.join(CORPUS_DIR, f))]
    total_files = len(corpus_files)

    if total_files == 0:
        messagebox.showwarning("No Files Found", f"No files found in '{CORPUS_DIR}'.")
        return

    # Prompt the user to select how many files to load
    num_files_to_load = simpledialog.askinteger(
        "Select Corpus Files",
        f"There are {total_files} files in the corpus. How many would you like to load?",
        minvalue=1,
        maxvalue=total_files
    )

    if num_files_to_load is None:  # User canceled
        return

    # Load the selected number of files
    selected_files = corpus_files[:num_files_to_load]
    selected_file_paths = [os.path.join(CORPUS_DIR, f) for f in selected_files]

    # Train the model on the selected files
    train_model_on_corpus(selected_file_paths)
    messagebox.showinfo("Training Complete", f"Model trained on {num_files_to_load} corpus files.")
