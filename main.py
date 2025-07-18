from ollama import Client
import subprocess
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
    return all_texts



def ask_ollama(prompt: str) -> str:
    mainpromt = """Extrahiere wichtige Informationen aus folgendem 
    Stellenanzeige es soll sachen rausfiltern damit 
    man ihn einsortieren kann und gib sie als JSON aus der die values als liste ausgibt
    und falls es nicht angegeben ist schreib null und nicht angegeben
    gib nichts anderes als die JSON aus keinen zusätzlichen Text und halte dich kurz und knapp"""
    prompt1 = mainpromt + prompt
    try:
        result = subprocess.run(
            ['ollama', 'run', 'qwen3:1.7b', prompt1, "--think=false"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        print(output)
        output = json.loads(output)

        with open("daten.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
    
    except subprocess.CalledProcessError as e:
        return f"Fehler beim Aufruf von Ollama: {e}"






