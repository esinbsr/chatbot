from docx import Document

def export_to_word(text: str, filename: str = None):
    if filename is None:
       filename = "doc.docx"
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(filename)
