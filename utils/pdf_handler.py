from fpdf import FPDF
from pathlib import Path
from PyPDF2 import PdfReader

# export text to pdf
def export_to_pdf(text: str, filename: str = None):
    if filename is None:
       filename = "doc.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)

# read pdf
def read_pdf(doc_path:str) -> str:
    doc_path = Path(doc_path)
    if not doc_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {doc_path}")
    try:
        reader = PdfReader(doc_path)
        document = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                document += text
        return document
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la lecture du document : {e}") 