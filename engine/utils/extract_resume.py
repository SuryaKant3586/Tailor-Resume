import os
import docx2txt
from pdfminer.high_level import extract_text

import logging
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def extract_text_from_pdf(file):
    return extract_text(file)

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_file(file):
    logging.info("\t\tExtracting text from resume file...")

    if file.type == "application/pdf":
        logging.info("\t\t Extrating text from pdf file...")
        text = extract_text_from_pdf(file)
        return text
    
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        logging.info("\t\t Extrating text from docx file...")
        text = extract_text_from_docx(file)
        return text
    
    elif file.type == "application/json":
        logging.info("\t\t Extracting text from JSON file...")
        return file.getvalue().decode("utf-8")
    
    elif file.type == "text/plain":  # Corrected MIME type for plain text files
        logging.info("\t\t Extracting text from TXT file...")
        return file.getvalue().decode("utf-8")
    
    else:
        logging.error(f"Error: Unsupported file format '{file.type}'.")
        return None
