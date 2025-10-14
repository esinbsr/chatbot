def identify_use_case(bot_core, user_input, context="", agent_info=None):
    print(f"[Agent] Appelé : {agent_info['id']} pour la question : {user_input}")
    prompt = f"""
Tu es {agent_info['id']} : {agent_info['role']}.
Objectif : {agent_info['goal']}
Style : {agent_info['style']}

Question : {user_input}

Réponse :
"""
    response = bot_core.ask(prompt, context=context)
    return response
