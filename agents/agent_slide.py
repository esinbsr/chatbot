from agents.agent_ml import AGENT_CONFIG
from utils.pptx_handler import export_to_pptx

class SliderAgent(AGENT_CONFIG):
   def generate_slides(self,input):
      prompt = f"{self.system_prompt}\n {input}"
      response = self.core.ask(prompt)
      export_to_pptx(response)
      return response
     