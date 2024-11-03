# PDAI

## Requirements
- **Anaconda(Lastest version)**: Create an environment and run the setup.py in the root directory of the repository.

## 1. Detailed Breakdown

### Root Files

- **README.md**: Provide an overview of the project, the main goals, and installation instructions. Each team member should contribute to this file.
- **requirements.txt**: List all required Python packages.
- **.gitignore**: Specify files that should be ignored by Git (e.g., .env, virtual environments, output files).
- **CONTRIBUTING.md**: Guidelines for how group members and contributors should work on the project.
- **LICENSE**: Choose an appropriate license for your project.

### /docs/ Directory

Contains all relevant documentation like the project design, architecture, explainability methods, etc.

- **index.md**: Overview of the explainable AI aspects, methods used (e.g., SHAP or LIME), and implementation details.

### /src/ Directory

The source code will be divided into clear modules, with each module potentially assigned to one person.

- **pdf_extraction/**: Handles extracting text from PDFs.
  - **pdf_extractor.py**: Functions for extracting text from PDF files.
- **text_analysis/**: Performs NLP on the extracted text and prepares the data for story generation.
  - **nlp_processor.py**: Tokenization, entity recognition, keyword extraction.
- **word_generation/**: Generates Word documents.
  - **docx_generator.py**: Functions for writing content to .docx files using python-docx.
- **explainable_ai/**: Manages the explainability aspects of the project, such as visualizing model predictions, explaining PDF text extraction, and displaying the impact of key terms on generated outputs.
  - **explainability.py**: Explainable AI methods (LIME, SHAP) for PDF extraction and text generation.

Each module can be assigned to a different team member, with clear tasks to work on.

### /tests/ Directory

This folder holds unit tests for each module.

- **test_pdf_extraction.py**: Tests for the pdf_extraction module.
- **test_text_analysis.py**: Tests for the NLP processing functions.
- **test_word_generation.py**: Tests for the Word document generation.
- **test_explainable_ai.py**: Tests for the explainability methods.

### /data/ Directory

- **sample_pdfs/**: A collection of PDFs for testing the extraction pipeline.
- **output_docs/**: Stores the generated Word documents for reference.

## 2. Projects for the Team

Each person can take responsibility for one or more modules:

- **Person 1**: PDF Text Extraction (pdf_extraction)
  - TODO: Extract text from PDFs, integrate OCR if needed for scanned PDFs.
- **Person 2**: Text Analysis (text_analysis)
  - TODO: Use NLP techniques to process extracted text, implement tokenization, entity extraction, etc.
- **Person 3**: Word Document Generation (word_generation)
  - TODO: Create Word documents from processed text and support customization options.
- **Person 4**: Explainability (explainable_ai)
  - TODO: Implement explainability techniques (SHAP, LIME) and visualize decision-making in text extraction and generation.

Each member will contribute to the testing and documentation for their assigned module.

## 4. Branching and Workflow (GitHub)

- Use feature branches for each team member:
  - `feature/pdf-extraction`
  - `feature/text-analysis`
  - `feature/word-generation`
  - `feature/explainability`
- Merge code into a development branch after reviewing pull requests.
- Use the main branch for the final, tested version of the project.


## 5. How to Lauch (Tenative)

  - Dowload Anaconda
  - Create an environment for this application
  - Activate you environment
  - Change your directory to the appropriate folder
  - Enter the following command in your Anaconda environment 
    - \"python -m ex_ai.Ui"
  - Click on \"Select a Pdf file"
  - Wait for extraction.
  - Click on export txt file
  - File should be in the same directory as the original pdf file
  - Give yourself a yodahigh five.