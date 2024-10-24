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
    
def extract_images_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Dictionary to hold images for each page
            pages_images = {}

            # Extract images page by page
            for page_num, page in enumerate(pdf_reader.pages):
                images = page.extract_images()
                pages_images[page_num + 1] = images  # Page numbers start from 1
            return pages_images
    except Exception as e:
        print(f"Error extracting images from PDF: {e}")
        return None
