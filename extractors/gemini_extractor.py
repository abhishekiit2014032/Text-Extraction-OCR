import google.generativeai as genai
from PIL import Image
import json
from .base import BaseExtractor
import config

class GeminiExtractor(BaseExtractor):
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError("Gemini API key not provided in .env (GEMINI_API_KEY).")
        genai.configure(api_key=config.GEMINI_API_KEY)
        # Using Gemini 1.5 Flash as it is highly efficient and capable of reading documents
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def extract(self, image_path: str) -> dict:
        result = {
            "Seller Name": None,
            "Seller Tax ID": None,
            "Client Name": None,
            "Client Tax ID": None,
            "Invoice Number": None,
            "Invoice Date": None,
            "Net Worth": None,
            "VAT": None,
            "Gross Worth": None
        }
        
        prompt = """
        Analyze this invoice image carefully and extract the following fields. 
        Return ONLY a valid JSON object with exact keys:
        - "Seller Name"
        - "Seller Tax ID"
        - "Client Name"
        - "Client Tax ID"
        - "Invoice Number"
        - "Invoice Date"
        - "Net Worth"
        - "VAT"
        - "Gross Worth"
        
        If a field is missing, cannot be found, or is not applicable, set its value to null.
        Ensure your response is raw JSON without Markdown blocks like ```json ... ```. 
        Do not include any other text.
        """
        
        try:
            img = Image.open(image_path)
            response = self.model.generate_content([prompt, img])
            text = response.text.strip()
            
            # Defensive check against markdown blocks despite prompting
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            text = text.strip()
            
            data = json.loads(text)
            for key in result.keys():
                if key in data and data[key] is not None:
                    result[key] = str(data[key])
                    
        except Exception as e:
            print(f"Gemini Extraction Error for {image_path}: {e}")
            
        return result
