from agents.base_agent import BaseAgent
from services.pdf_export import export_to_pdf
from services.word_export import export_to_word
from typing import List

class SummarizerAgent(BaseAgent):
    
    def generate_report(self, documents: List[str],input, sections : str=None):
        if sections is None:
            sections = ["Introduction", "Synthèse", "Conclusion"]

        full_text = "\n\n".join(documents)
        prompt = f"{self.system_prompt}\n {input} :\n{full_text}"
        summary = self.core.ask(prompt)

        report = "📘 Rapport de Synthèse\n\n"
        if "Introduction" in sections:
            report += "🔹 Ce rapport présente une synthèse des documents analysés.\n\n"
        if "Synthèse" in sections:
            report += f"🔹 Synthèse\n{summary}\n\n"
        if "Conclusion" in sections:
            report += f"🔹 Ce résumé est généré automatiquement par l’agent {self.name}.\n"

        return report

    def export_report(self, report_text: str, format: str = "pdf", filename: str = None):
        if format == "pdf":
            export_to_pdf(report_text, filename)
        elif format == "word":
            export_to_word(report_text, filename)
        else:
            raise ValueError("Format non supporté : choisir 'pdf' ou 'word'")
