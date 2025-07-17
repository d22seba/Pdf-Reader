from ollama import Client
import json
import os
import pdfplumber
import re

client = Client()

def clean_text(text):
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def list_pdfs():
    pdfs = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdfs.append(os.path.join(root, file))
    return pdfs


def extract_text_from_pdf(pdf_path):

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_all_pdfs_text():
    pdfs = list_pdfs()
    all_texts = ""
    for pdf in pdfs:
        all_texts += extract_text_from_pdf(pdf) + "\n"
        all_texts = clean_text(all_texts)
    return list(all_texts)

def analyze_text_with_ollama(text):
    prompt = (
        "Extrahiere aus diesem Stellenanzeigen-Text die wichtigsten Jobinformationen "
    )

    response = client.chat(model="qwen:1.8b", messages=[
        {
            "role": "user",
            "content": prompt
        }
    ])

    print("🔵 Antwort von Ollama:")
    print(response["message"]["content"])
    
    try:
        return json.loads(response["message"]["content"])
    except json.JSONDecodeError:
        print("⚠️ Antwort war kein gültiges JSON.")
        return None




