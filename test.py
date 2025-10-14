from router import AgentRouter  
from pathlib import Path
from PyPDF2 import PdfReader

# Initialiser le routeur avec le fichier de config
router = AgentRouter(config_path="config/agents.yaml")

# Charger ton document DevOps
'''
doc_path = Path("C:/Users/Utilisateur/Downloads/CahierDesCharges.pdf")
reader = PdfReader(doc_path)

document = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        document += text

# Génerer le rapport via l’agent de synthèse
report = router.agents["SummarizerBot"].generate_report([document],"analyse ce document et génère moi un rapport qui résume tous les points abordés et génère moi un fichier .docx qui contient ce rapport")

# Afficher le rapport
print(report)
'''
# Exporter si besoin
#router.agents["SummarizerBot"].export_report(report, format="word", filename="rapport")
slides = router.agents["SliderBot"].generate_slides("Génère moi une présentation de 8 slides claires sur les bases de données SQL déstinée aux développeurs de mon entreprise ")

print(slides)