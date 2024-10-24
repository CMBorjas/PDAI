import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_extraction.extractor import extract_text_from_pdf  # Correct import path
import os

# Global variable to store extracted text and file path
extracted_text = ""
pdf_file_path = ""

# Function to handle file selection and text extraction
def select_file_and_extract():
    global extracted_text, pdf_file_path
    # Open file dialog to select a PDF
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if pdf_file_path:
        extracted_text_dict = extract_text_from_pdf(pdf_file_path)
        if extracted_text_dict:
            messagebox.showinfo("Extraction Success", "Text extracted successfully!")
            # Clear the text_output widget before inserting new text
            text_output.delete(1.0, tk.END)
            
            # Join all pages' text into a single string for saving to a .txt file
            extracted_text = ""
            for page_num, page_text in extracted_text_dict.items():
                extracted_text += f"--- Page {page_num} ---\n{page_text}\n\n"
                text_output.insert(tk.END, f"--- Page {page_num} ---\n{page_text}\n\n")
        else:
            messagebox.showerror("Extraction Failed", "Unable to extract text from the PDF.")
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file to extract.")

# Function to export the extracted text to a .txt file
def export_to_txt():
    global extracted_text, pdf_file_path # No choice but to use global variables
    if extracted_text and pdf_file_path:
        # Get the name of the original PDF without extension
        file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
        # Create file with the same name as the PDF
        txt_file_path = os.path.join(os.path.dirname(pdf_file_path), f"{file_name}.txt")
        try:
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(extracted_text)
            messagebox.showinfo("Export Success", f"Text exported successfully to {txt_file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export text: {e}")
    else:
        messagebox.showwarning("No Text to Export", "Please extract text from a PDF first.")

# Create the main window
root = tk.Tk()
root.title("PDF Text Extractor")

# Create a button to select a PDF file and extract its text
select_file_button = tk.Button(root, text="Select PDF", command=select_file_and_extract)
select_file_button.pack(pady=10)

# Create a button to export the extracted text to a .txt file
export_button = tk.Button(root, text="Export to .txt", command=export_to_txt)
export_button.pack(pady=10)

# Create a text widget to display extracted text, separated by pages
text_output = tk.Text(root, height=20, width=80)
text_output.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
