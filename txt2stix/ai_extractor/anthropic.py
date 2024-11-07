
from txt2stix.ai_extractor.base import BaseAIExtractor
from llama_index.llms.anthropic import Anthropic


class AnthropicAIExtractor(BaseAIExtractor, provider="anthropic"):
    def __init__(self, model_name=None) -> None:
        self.llm = Anthropic(temperature=0.0, max_tokens=4096, system_prompt=self.system_prompt)
        super().__init__()

    def count_tokens(self, input_text):
        # return len(self.llm.tokenizer.encode(input_text))
        # TODO
        return 0