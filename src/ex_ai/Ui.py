import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_extraction.extractor import extract_text_from_pdf
from text_analysis.txt_analysis import *
import os
from docx import Document
from transformers import GPT2LMHeadModel, GPT2Tokenizer
#import torch

# Global variable to store extracted text and file path
extracted_text = ""
pdf_file_path = ""
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Function to handle file selection and text extraction
def select_file_and_extract():
    global extracted_text, pdf_file_path
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if pdf_file_path:
        extracted_text_dict = extract_text_from_pdf(pdf_file_path)
        if extracted_text_dict:
            messagebox.showinfo("Extraction Success", "Text extracted successfully!")
            text_output.delete(1.0, tk.END)
            
            # Join all pages' text into a single string for further analysis
            extracted_text = ""
            for page_num, page_text in extracted_text_dict.items():
                extracted_text += f"--- Page {page_num} ---\n{page_text}\n\n"
                text_output.insert(tk.END, f"--- Page {page_num} ---\n{page_text}\n\n")
        else:
            messagebox.showerror("Extraction Failed", "Unable to extract text from the PDF.")
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file to extract.")

# Function to send the extracted text to a .txt file
def export_to_txt():
    global extracted_text, pdf_file_path
    if extracted_text and pdf_file_path:
        file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
        txt_file_path = os.path.join(os.path.dirname(pdf_file_path), f"{file_name}.txt")
        try:
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(extracted_text)
            messagebox.showinfo("Export Success", f"Text exported successfully to {txt_file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export text: {e}")
    else:
        messagebox.showwarning("No Text to Export", "Please extract text from a PDF first.")

# Function to send the extracted text to a .docx file
def export_to_docx():
    global extracted_text, pdf_file_path
    if extracted_text and pdf_file_path:
        file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
        docx_file_path = os.path.join(os.path.dirname(pdf_file_path), f"{file_name}.docx")
        try:
            doc = Document()
            doc.add_heading('Extracted Data', level=1)
            for page in extracted_text.split("\n\n"):
                doc.add_paragraph(page)
            doc.save(docx_file_path)
            messagebox.showinfo("Export Success", f"Text exported successfully to {docx_file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export text: {e}")
    else:
        messagebox.showwarning("No Text to Export", "Please extract text from a PDF first.")

# NLP Functions to analyze extracted text
def summarize_extracted_text():
    global extracted_text
    if extracted_text:
        summary = summarize_text(extracted_text)
        text_output.insert(tk.END, f"\n--- Summary ---\n{summary}\n")
    else:
        messagebox.showwarning("No Text to Summarize", "Please extract text from a PDF first.")

# function for keywords extraction
def extract_keywords_from_text():
    global extracted_text
    if extracted_text:
        keywords = extract_keywords(extracted_text)
        text_output.insert(tk.END, f"\n--- Keywords ---\n{', '.join(keywords)}\n")
    else:
        messagebox.showwarning("No Text for Keywords", "Please extract text from a PDF first.")

# function to categorize extracted text
def categorize_extracted_text():
    global extracted_text
    if extracted_text:
        categories = categorize_text(extracted_text)
        text_output.insert(tk.END, f"\n--- Categories ---\n{', '.join(categories)}\n")
    else:
        messagebox.showwarning("No Text to Categorize", "Please extract text from a PDF first.")

# OCR Button to handle OCR extraction
def perform_ocr_extraction():
    global pdf_file_path
    if pdf_file_path:
        ocr_text = extract_text_with_ocr(pdf_file_path)
        text_output.insert(tk.END, f"\n--- OCR Text ---\n{ocr_text}\n")
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file for OCR.")

# function to display tokenized text
def display_tokenized_text():
    global extracted_text
    if extracted_text:
        tokens = tokenize_text(extracted_text)
        text_output.insert(tk.END, f"\n--- Tokenized Text ---\n{', '.join(tokens)}\n")
    else:
        messagebox.showwarning("No Text to Tokenize", "Please extract text from a PDF first.")

# function to display extracted entities
def display_extracted_entities():
    global extracted_text
    if extracted_text:
        entities = extract_entities(extracted_text)
        text_output.insert(tk.END, f"\n--- Extracted Entities ---\n{', '.join(entities)}\n")
    else:
        messagebox.showwarning("No Text to Extract Entities", "Please extract text from a PDF first.")

# Function to generate text using GPT-2 model
def generate_paragraph(prompt, max_length=150):
    """
    Generate a paragraph based on the given prompt.

    Parameters:
    - prompt (str): The input text prompt for the model.
    - max_length (int): The maximum length of the generated text.

    Returns:
    - str: Generated paragraph as a string.
    """

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    """
    This code uses the generate method of the GPT-2 model to generate text based on the provided input IDs. The parameters used in the generate method are:

        input_ids: The encoded input prompt.
        max_length: The maximum length of the generated text.
        num_return_sequences: The number of sequences to generate.
        no_repeat_ngram_size: Prevents repeating n-grams of the specified size.
        top_p: Implements nucleus sampling, where only the most probable tokens with a cumulative probability above this threshold are considered.
        temperature: Controls the randomness of predictions by scaling the logits before applying softmax.
    """
    output = model.generate(
        input_ids, 
        max_length=max_length, 
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_p=0.95,
        temperature=0.7
    )
    
    # Decode the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Function to generate a paragraph from extracted text
def generate_paragraph_from_text():
    global extracted_text
    if extracted_text:
        paragraph = generate_paragraph(extracted_text)
        text_output.insert(tk.END, f"\n--- Generated Paragraph ---\n{paragraph}\n")
    else:
        messagebox.showwarning("No Text to Generate", "Please extract text from a PDF first.")

# Create the main window
root = tk.Tk()
root.title("PDF Text Extractor with NLP and OCR")

# Create buttons for selecting PDF and exporting text
select_file_button = tk.Button(root, text="Select PDF", command=select_file_and_extract)
summarize_button = tk.Button(root, text="Summarize Text", command=summarize_extracted_text)
keywords_button = tk.Button(root, text="Extract Keywords", command=extract_keywords_from_text)
categorize_button = tk.Button(root, text="Categorize Text", command=categorize_extracted_text)
ocr_button = tk.Button(root, text="Perform OCR", command=perform_ocr_extraction)
tokenize_button = tk.Button(root, text="Tokenize Text", command=display_tokenized_text)
entities_button = tk.Button(root, text="Extract Entities", command=display_extracted_entities)
export_to_docx_button = tk.Button(root, text="Export to .docx", command=export_to_docx)
export_to_txt_button = tk.Button(root, text="Export to .txt", command=export_to_txt)
generate_button = tk.Button(root, text="Generate Paragraph", command=generate_paragraph_from_text)

# Place buttons in a grid
buttons = [
    select_file_button, summarize_button, keywords_button, categorize_button,
    ocr_button, tokenize_button, entities_button, export_to_docx_button,
    export_to_txt_button, generate_button
]

for i, button in enumerate(buttons):
    button.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

# Configure the grid to allow wrapping
for i in range(len(buttons)):
    root.grid_columnconfigure(i, weight=1)

# Text widget to display extracted text, separated by pages
text_output = tk.Text(root, height=20, width=80)
text_output.grid(row=1, column=0, columnspan=len(buttons), padx=5, pady=5, sticky="nsew")

# Configure the grid to expand with the window
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the Tkinter event loop
root.mainloop()