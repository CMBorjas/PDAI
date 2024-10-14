from setuptools import setup, find_packages

# Load the README content for the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pdf_extractor_ai",                 # Replace with your project name
    version="1.0.0",
    author="Christian Kingsley",
    author_email="c.mandujano.borjas@gmail.com",
    description="A PDF extractor with Explainable AI and Word document generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #TODO:url="{placeholder}",  # Replace with your repo
    packages=find_packages(),                # Automatically discover packages in src
    install_requires=[
        "PyPDF2>=3.0.0",                     # Dependency for PDF extraction
        "python-docx>=0.8.11",               # To generate Word documents
        "tkinter",                           # For the UI (Tkinter is built-in for most Python installs)
        "spacy>=3.0.0",                      # For NLP analysis
        "lime>=0.2.0.1",                     # For Explainable AI
    ],
    entry_points={
        'console_scripts': [
            'pdf-extractor=src.pdf_extractor:main',  # Define a CLI entry point if needed
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",   # Choose your preferred license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
