
import logging
import os
from txt2stix.ai_extractor.base import BaseAIExtractor
from llama_index.llms.anthropic import Anthropic


class AnthropicAIExtractor(BaseAIExtractor, provider="anthropic"):
    def __init__(self, model='claude-sonnet-4-0', **kwargs) -> None:
        kwargs.setdefault('temperature', float(os.environ.get('TEMPERATURE', 0.0)))
        self.llm = Anthropic(max_tokens=4096, model=model, system_prompt=self.system_prompt, **kwargs)
        super().__init__()