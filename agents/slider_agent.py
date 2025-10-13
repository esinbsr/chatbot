from agents.base_agent import BaseAgent
from services.pptx_export import export_to_pptx

class SliderAgent(BaseAgent):

   def _parse_response_to_sections(self, response):
        sections = []
        for block in [b.strip() for b in response.split("\n\n") if b.strip()]:
            lines = block.splitlines()
            title = lines[0].strip() if lines else ""
            body_lines = [ln.strip() for ln in lines[1:]]
            sections.append({"title": title, "body": body_lines})
        return sections
      
   def generate_slides(self,input):
      prompt = f"{self.system_prompt}\n {input}"
      response = self.core.ask(prompt)
      #slides = self._parse_response_to_sections(response)
      export_to_pptx(response)
      return "présentation générée slides.pptx"
     