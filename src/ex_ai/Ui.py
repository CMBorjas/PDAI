import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_extraction.extractor import extract_text_from_pdf  # Correct import path for running from src

# Function to handle file selection and text extraction
def select_file_and_extract():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        extracted_text = extract_text_from_pdf(file_path)
        if extracted_text:
            messagebox.showinfo("Extraction Success", "Text extracted successfully!")
            text_output.delete(1.0, tk.END)
            for page_num, page_text in extracted_text.items():
                text_output.insert(tk.END, f"--- Page {page_num} ---\n{page_text}\n\n")
        else:
            messagebox.showerror("Extraction Failed", "Unable to extract text from the PDF.")
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file to extract.")

# Create the main window
root = tk.Tk()
root.title("PDF Text Extractor")

select_file_button = tk.Button(root, text="Select PDF", command=select_file_and_extract)
select_file_button.pack(pady=10)

text_output = tk.Text(root, height=20, width=80)
text_output.pack(pady=10)

root.mainloop()
