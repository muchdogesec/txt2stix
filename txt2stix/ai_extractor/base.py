import logging
from typing import Type
from llama_index.core.program import LLMTextCompletionProgram

import textwrap
from llama_index.core import PromptTemplate
from llama_index.core.llms.llm import LLM

from txt2stix.ai_extractor.prompts import DEFAULT_CONTENT_CHECKER_TEMPL, DEFAULT_EXTRACTION_TEMPL, DEFAULT_RELATIONSHIP_TEMPL, DEFAULT_SYSTEM_PROMPT, ATTACK_FLOW_PROMPT_TEMPL
from txt2stix.ai_extractor.utils import AttackFlowList, DescribesIncident, ExtractionList, ParserWithLogging, RelationshipList, get_extractors_str
from llama_index.core.utils import get_tokenizer


_ai_extractor_registry: dict[str, 'Type[BaseAIExtractor]'] = {}
class BaseAIExtractor():
    system_prompt = DEFAULT_SYSTEM_PROMPT
    
    extraction_template = DEFAULT_EXTRACTION_TEMPL

    relationship_template = DEFAULT_RELATIONSHIP_TEMPL

    content_check_template = DEFAULT_CONTENT_CHECKER_TEMPL

    def _get_extraction_program(self):
        return LLMTextCompletionProgram.from_defaults(
            output_parser=ParserWithLogging(ExtractionList),
            prompt=self.extraction_template,
            verbose=True,
            llm=self.llm,
        )
    
    def _get_relationship_program(self):
        return LLMTextCompletionProgram.from_defaults(
            output_parser=ParserWithLogging(RelationshipList),
            prompt=self.relationship_template,
            verbose=True,
            llm=self.llm,
        )
    
    def _get_content_checker_program(self):
        return LLMTextCompletionProgram.from_defaults(
            output_parser=ParserWithLogging(DescribesIncident),
            prompt=self.content_check_template,
            verbose=True,
            llm=self.llm,
        )
    
    def check_content(self, text) -> DescribesIncident:
        return self._get_content_checker_program()(context_str=text)
    
    def _get_attack_flow_program(self):
        return LLMTextCompletionProgram.from_defaults(
            output_parser=ParserWithLogging(AttackFlowList),
            prompt=ATTACK_FLOW_PROMPT_TEMPL,
            verbose=True,
            llm=self.llm,
        )
    
    def extract_attack_flow(self, input_text, extractions, relationships):
        return self._get_attack_flow_program()(document=input_text, extractions=extractions, relationships=relationships)

    def extract_relationships(self, input_text, extractions, relationship_types: list[str]) -> RelationshipList:
        return self._get_relationship_program()(relationship_types=relationship_types, input_file=input_text, extractions=extractions)
    
    def extract_objects(self, input_text, extractors) -> ExtractionList:
        return self._get_extraction_program()(extractors=get_extractors_str(extractors), input_file=input_text)
    
    def __init__(self, *args, **kwargs) -> None:
        pass

    def count_tokens(self, input_text):
        logging.info("unsupported model `%s`, estimating using llama-index's default tokenizer", self.extractor_name)
        return len(get_tokenizer()(input_text))
    
    def __init_subclass__(cls, /, provider, register=True, **kwargs):
        super().__init_subclass__(**kwargs)
        if register:
            cls.provider = provider
            _ai_extractor_registry[provider] = cls

    @property
    def extractor_name(self):
        return f"{self.provider}:{self.llm.model}"