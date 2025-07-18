from main import *

if __name__ == "__main__":
    pdfs = extract_all_pdfs_text()
    ask_ollama(pdfs)