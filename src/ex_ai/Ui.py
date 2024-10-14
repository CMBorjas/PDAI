import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfFileReader(file)
            
            # Extract text from each page
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()
            return text
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
            text_output.insert(tk.END, extracted_text)
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

# Create a text widget to display extracted text
text_output = tk.Text(root, height=20, width=80)
text_output.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
