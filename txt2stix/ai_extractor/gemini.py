   
from txt2stix.ai_extractor.base import BaseAIExtractor
from llama_index.llms.gemini import Gemini


class GeminiAIExtractor(BaseAIExtractor, provider="gemini"):
    def __init__(self, model_name=None) -> None:
        self.llm = Gemini(temperature=0.0, max_tokens=4096, model_name=model_name)
        super().__init__()

    def count_tokens(self, text):
        return self.llm._model.count_tokens(text).total_tokens