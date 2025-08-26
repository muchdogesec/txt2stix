   
import logging
import os
from txt2stix.ai_extractor.base import BaseAIExtractor
from llama_index.llms.openai import OpenAI


class OpenAIExtractor(BaseAIExtractor, provider="openai"):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault('temperature', float(os.environ.get('TEMPERATURE', 0.0)))
        self.llm = OpenAI(system_prompt=self.system_prompt, **kwargs)
        super().__init__()

    def count_tokens(self, text):
        try:
            return len(self.llm._tokenizer.encode(text))
        except Exception as e:
            logging.warning(e)
            return super().count_tokens(text)
    
