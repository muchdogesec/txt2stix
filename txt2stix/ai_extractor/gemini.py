   
import os
from txt2stix.ai_extractor.base import BaseAIExtractor
from llama_index.llms.google_genai import GoogleGenAI


class GeminiAIExtractor(BaseAIExtractor, provider="gemini"):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault('temperature', float(os.environ.get('TEMPERATURE', 0.0)))
        self.llm = GoogleGenAI(max_tokens=4096, **kwargs)
        super().__init__()

    def count_tokens(self, text):
        return self.llm._client.models.count_tokens(model=self.llm.model, contents=text).total_tokens
    
    @property
    def extractor_name(self):
        return f"{self.provider}:{self.llm.model}"