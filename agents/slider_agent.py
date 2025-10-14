from agents.base_agent import BaseAgent
from utils.pptx_handler import export_to_pptx

class SliderAgent(BaseAgent):
   def generate_slides(self,input):
      prompt = f"{self.system_prompt}\n {input}"
      response = self.core.ask(prompt)
      export_to_pptx(response)
      return response
     