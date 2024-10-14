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

# Path to the PDF file
pdf_path = '/mnt/data/armyofthedamned.pdf'

# Extract and print the text
pdf_text = extract_text_from_pdf(pdf_path)
if pdf_text:
    print(pdf_text[:500])  # Print
