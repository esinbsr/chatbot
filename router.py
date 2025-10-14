import yaml
from sentence_transformers import SentenceTransformer
import faiss

# Charger le yaml
with open("config/agents.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

agents = config["agents"]
agent_map = {agent["id"]: agent for agent in agents}

# Préparer embeddings + faiss
model = SentenceTransformer("all-MiniLM-L6-v2")

# Texte de chaque agent = keywords + role
agent_texts = [" ".join(agent.get("keywords", [])) + " " + agent.get("role", "") for agent in agents]
embeddings = model.encode(agent_texts, convert_to_numpy=True)

# Créer index faiss
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Normalisation simple
def normalize(text):
    return text.lower()

# Router hybride
def router(user_input):
    user_input_norm = normalize(user_input)

    # Matching rapide sur mots-clés
    for agent in agents:
        keywords = agent.get("keywords", [])
        if any(kw.lower() in user_input_norm for kw in keywords):
            print(f"[Router] Fast path mots-clés → Agent choisi : {agent['id']}")
            return agent["id"]

    # Fallback embeddings + faiss
    query_vec = model.encode([user_input_norm])
    D, I = index.search(query_vec, k=1)


    # Vérification du seuil pour éviter les réponses hors scope
    threshold = 0.6  # à ajuster selon mes tests
    if D[0][0] > threshold:
        print(f"[Router] Distance trop grande ({D[0][0]:.2f}) → Agent hors-scope")
        return "agent_test"  # agent spécial pour les questions interdites/hors scope
    else:
        chosen_agent = agents[I[0][0]]["id"]
        print(f"[Router] Fallback embeddings → Agent choisi : {chosen_agent}")
        return chosen_agent