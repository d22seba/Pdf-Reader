from main import *

if __name__ == "__main__":
    pdfs = extract_all_pdfs_text()
    analyze_text_with_ollama(pdfs)