from agents.base_agent import BaseAgent
from export.pdf_export import export_to_pdf
from export.word_export import export_to_word
from typing import List

class SummarizerAgent(BaseAgent):
    def summarize_documents(self, documents: List[str]) -> str:
        full_text = "\n\n".join(documents)
        prompt = f"{self.system_prompt}\nAnalyse et résume ce contenu :\n{full_text}"
        return self.core.ask(prompt)

    def generate_report(self, documents: List[str], sections=None) -> str:
        if sections is None:
            sections = ["Introduction", "Synthèse", "Conclusion"]

        full_text = "\n\n".join(documents)
        prompt = f"{self.system_prompt}\nAnalyse et résume ce contenu :\n{full_text}"
        summary = self.core.ask(prompt)

        report = "📘 Rapport de Synthèse\n\n"
        if "Introduction" in sections:
            report += "🔹 Introduction\nCe rapport présente une synthèse des documents analysés.\n\n"
        if "Synthèse" in sections:
            report += f"🔹 Synthèse\n{summary}\n\n"
        if "Conclusion" in sections:
            report += f"🔹 Conclusion\nCe résumé est généré automatiquement par l’agent {self.name}.\n"

        return report


    def export_report(self, report_text: str, format: str = "pdf", filename: str = None):
        if format == "pdf":
            export_to_pdf(report_text, filename)
        elif format == "word":
            export_to_word(report_text, filename)
        else:
            raise ValueError("Format non supporté : choisir 'pdf' ou 'word'")
