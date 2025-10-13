from chatbot.core import ChatbotCore
from docling.converting import converter

bot_core = ChatbotCore()
convert = converter()

while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = bot_core.chat(user_input)
        print(f"\nAI: {response}\n")

        # 🎯 → Ajoute ça ici
        try:
            filename = user_input[:30].replace(" ", "_").replace("?", "")
            converter.from_text(response, filename=filename)
            print(f"[✓] Réponse sauvegardée dans scratch/{filename}.md (+ json/yaml)")
        except Exception as e:
            print(f"[!] Erreur lors de la conversion du document : {e}")