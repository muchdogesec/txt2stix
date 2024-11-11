   
import os
from txt2stix.ai_extractor.base import BaseAIExtractor
from llama_index.llms.gemini import Gemini


class GeminiAIExtractor(BaseAIExtractor, provider="gemini"):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault('temperature', float(os.environ.get('TEMPERATURE', 0.0)))
        self.llm = Gemini(max_tokens=4096, **kwargs)
        super().__init__()

    def count_tokens(self, text):
        return self.llm._model.count_tokens(text).total_tokens
    
    @property
    def extractor_name(self):
        return f"{self.provider}:{self.llm.model}"