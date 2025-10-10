class BaseAgent:
    def __init__(self, name, core, system_prompt=None):
        self.name = name
        self.core = core
        self.system_prompt = system_prompt

    def generate(self, user_input, context=""):
        return self.core.ask(user_input, context=context, system_prompt=self.system_prompt)

