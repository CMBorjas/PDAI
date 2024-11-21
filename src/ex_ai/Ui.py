import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pdf_extraction.extractor import extract_text_from_pdf
from text_analysis.txt_analysis import summarize_text, extract_keywords, categorize_text, extract_text_with_ocr
from docx import Document
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from shap_analysis.shap_utils import explain_model_with_shap


"""Updated v002"""
# Add the src directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load a smaller GPT-2 model and tokenizer to stay within memory limits
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  # Ensure the correct model identifier
model = GPT2LMHeadModel.from_pretrained(
    "gpt2", 
    torch_dtype=torch.float16,  # Use FP16 for reduced memory usage
    low_cpu_mem_usage=True  # Reduce memory during model initialization
)

# Global variables to store extracted text and file path
extracted_text = ""
pdf_file_path = ""
CORPUS_DIR = "PDAI/data/corpus"

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
            
            # Clear intermediate memory
            del extracted_text_dict
        else:
            messagebox.showerror("Extraction Failed", "Unable to extract text from the PDF.")
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file to extract.")

# Function to export the extracted text to a .txt file
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

# Function to export the extracted text to a .docx file
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

def extract_keywords_from_text():
    global extracted_text
    if extracted_text:
        keywords = extract_keywords(extracted_text)
        text_output.insert(tk.END, f"\n--- Keywords ---\n{', '.join(keywords)}\n")
    else:
        messagebox.showwarning("No Text for Keywords", "Please extract text from a PDF first.")

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

# Function to generate text using GPT-2 model
def generate_paragraph(prompt, max_length=150):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(
        input_ids, 
        max_length=max_length, 
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_p=0.95,
        temperature=0.7
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

def generate_paragraph_from_text():
    global extracted_text
    if extracted_text:
        paragraph = generate_paragraph(extracted_text)
        text_output.insert(tk.END, f"\n--- Generated Paragraph ---\n{paragraph}\n")
    else:
        messagebox.showwarning("No Text to Generate", "Please extract text from a PDF first.")

# SHAP Explanation Function
def explain_with_shap():
    global extracted_text
    if extracted_text:
        explain_model_with_shap(model, tokenizer, extracted_text)
    else:
        messagebox.showwarning("No Text for SHAP", "Please extract text from a PDF first.")

# Create the main window
root = tk.Tk()
root.title("PDF Text Extractor with NLP, OCR Tools, and Corpus Training")

# Create buttons for various functions
select_file_button = tk.Button(root, text="Select PDF", command=select_file_and_extract)
select_file_button.pack(pady=10)

# NLP action buttons
summarize_button = tk.Button(root, text="Summarize Text", command=summarize_extracted_text)
summarize_button.pack(pady=5)

# Keywords and categorization buttons
keywords_button = tk.Button(root, text="Extract Keywords", command=extract_keywords_from_text)
keywords_button.pack(pady=5)

# Categorization button
categorize_button = tk.Button(root, text="Categorize Text", command=categorize_extracted_text)
categorize_button.pack(pady=5)

# OCR button
ocr_button = tk.Button(root, text="Perform OCR", command=perform_ocr_extraction)
export_to_docx_button = tk.Button(root, text="Export to .docx", command=export_to_docx)
export_to_docx_button.pack(pady=10)

# Export to txt button
export_to_txt_button = tk.Button(root, text="Export to .txt", command=export_to_txt)
generate_button = tk.Button(root, text="Generate Paragraph", command=generate_paragraph_from_text)
shap_button = tk.Button(root, text="Explain with SHAP", command=explain_with_shap)
train_button = tk.Button(root, text="Train Model with Checkpointing", command=lambda: train_model_on_corpus(selected_file_paths))
resume_button = tk.Button(root, text="Resume Training", command=lambda: load_checkpoint("checkpoints/latest_checkpoint.pth"))

# Place buttons in a grid layout
buttons = [
    select_file_button, summarize_button, keywords_button, categorize_button,
    ocr_button, export_to_docx_button, export_to_txt_button, generate_button,
    shap_button, train_button, resume_button
]

for i, button in enumerate(buttons):
    button.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

# Configure the grid to allow resizing
for i in range(len(buttons)):
    root.grid_columnconfigure(i, weight=1)

# Text widget to display extracted text
text_output = tk.Text(root, height=20, width=80)
text_output.grid(row=1, column=0, columnspan=len(buttons), padx=5, pady=5, sticky="nsew")

# Run the Tkinter event loop
root.mainloop()
