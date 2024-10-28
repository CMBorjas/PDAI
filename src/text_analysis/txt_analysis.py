import spacy
from nltk import FreqDist
from nltk.corpus import stopwords
import pytesseract
from PIL import Image
import pdf2image

# Load NLP model and stop words
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

# Function to summarize text
def summarize_text(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    summary = ' '.join(sentences[:min(len(sentences), 5)])  # Extract the first 5 sentences for simplicity
    return summary

# Function to extract keywords
def extract_keywords(text, num_keywords=10):
    words = [token.text.lower() for token in nlp(text) if token.is_alpha and token.text.lower() not in stop_words]
    freq_dist = FreqDist(words)
    keywords = [word for word, freq in freq_dist.most_common(num_keywords)]
    return keywords

# Function to categorize text based on specific terms
def categorize_text(text):
    categories = {
        "AC": "Armor Class",
        "HP": "Hit Points",
        "STR": "Strength",
        "DEX": "Dexterity",
        "CON": "Constitution",
        "INT": "Intelligence",
        "WIS": "Wisdom",
        "CHA": "Charisma",
        "DM": "Dungeon Master",
        "PC": "Player Character",
        "NPC": "Non-Player Character",
        "CR": "Challenge Rating",
        "XP": "Experience Points",
        "DC": "Difficulty Class",
        "AoE": "Area of Effect",
        "THAC0": "To Hit Armor Class 0",
        "d20": "20-sided die",
        "initiative": "the order in which characters act in combat",
        "spell": "a magical effect",
        "cantrip": "a low-level spell that can be cast at will",
    }
    
    text = text.lower()
    matched_categories = {category for category, keywords in categories.items() if any(word in text for word in keywords)}
    return list(matched_categories) if matched_categories else ["Uncategorized"]

# Function to perform OCR on PDF pages
def extract_text_with_ocr(pdf_path):
    pages = pdf2image.convert_from_path(pdf_path)
    ocr_text = ""
    for page_num, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        ocr_text += f"--- Page {page_num + 1} OCR Text ---\n{text}\n\n"
    return ocr_text
