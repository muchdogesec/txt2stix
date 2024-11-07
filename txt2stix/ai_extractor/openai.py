   
from txt2stix.ai_extractor.base import BaseAIExtractor
from llama_index.llms.openai import OpenAI


class OpenAIExtractor(BaseAIExtractor, provider="openai"):
    def __init__(self, model_name=None) -> None:
        self.llm = OpenAI(model_name=model_name, temperature=0.0, system_prompt=self.system_prompt)
        super().__init__()

    def count_tokens(self, text):
        return len(self.llm._tokenizer.encode(text))