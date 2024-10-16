import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

# Function to extract text from a PDF file and separate it by pages
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Dictionary to hold text for each page
            pages_text = {}

            # Extract text page by page
            for page_num, page in enumerate(pdf_reader.pages):
                pages_text[page_num + 1] = page.extract_text()  # Page numbers start from 1
            return pages_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

# Function to handle file selection and text extraction
def select_file_and_extract():
    # Open file dialog to select a PDF
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        extracted_text = extract_text_from_pdf(file_path)
        if extracted_text:
            messagebox.showinfo("Extraction Success", "Text extracted successfully!")
            # Clear the text_output widget before inserting new text
            text_output.delete(1.0, tk.END)
            
            # Display the text separated by pages
            for page_num, page_text in extracted_text.items():
                text_output.insert(tk.END, f"--- Page {page_num} ---\n{page_text}\n\n")
        else:
            messagebox.showerror("Extraction Failed", "Unable to extract text from the PDF.")
    else:
        messagebox.showwarning("No File Selected", "Please select a PDF file to extract.")

# Create the main window
root = tk.Tk()
root.title("PDF Text Extractor")

# Create a button to select a PDF file and extract its text
select_file_button = tk.Button(root, text="Select PDF", command=select_file_and_extract)
select_file_button.pack(pady=10)

# Create a text widget to display extracted text, separated by pages
text_output = tk.Text(root, height=20, width=80)
text_output.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
