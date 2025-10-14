def agent_test_function(bot_core, user_input, context="", agent_info=None):
    """
    Agent pour questions hors scope ou interdites.
    """
    print(f"[Agent] Appelé : {agent_info['id']} pour la question : {user_input}")
    return "Désolé, je ne peux pas répondre à cette question."