import logging
from typing import Type
from llama_index.core.program import LLMTextCompletionProgram

import textwrap
from llama_index.core import PromptTemplate
from llama_index.core.llms.llm import LLM

from txt2stix.ai_extractor.utils import ExtractionList, ParserWithLogging, RelationshipList, get_extractors_str
from llama_index.core.utils import get_tokenizer


_ai_extractor_registry: dict[str, 'Type[BaseAIExtractor]'] = {}
class BaseAIExtractor():
    system_prompt = (textwrap.dedent("""
    You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence.
    You have a deep understanding of cybersecurity concepts and threat intelligence.
    You are responsible for extracting observables and TTPs from documents provided, and understanding the relationships being described that link them.
    You are responsible for delivering computer-parsable output in JSON format. All output from you will be parsed with pydantic for further processing
    """))
    extraction_template = PromptTemplate(textwrap.dedent("""
        <persona>

        You are a cyber-security threat intelligence analyst responsible for analysing intelligence. You have a deep understanding of cybersecurity concepts and threat intelligence. You are responsible for extracting observables and TTPs from documents provided, and understanding the relationships being described that link them.

        </persona>

        <requirement>

        Using the file in `<document>`, you are to extract objects from the body of input (either plaintext or markdown), extractions must be unique!
        

        Only one JSON object should exist for each unique value.

        IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.

        </requirement>

        <accuracy>

        Think about your answer first before you respond.

        If you don't know the answer, reply with success: false, do not every try to make up an answer.

        </accuracy>

        <document>
        {input_file}
        </document>

        <extractors>
        {extractors}
        </extractors>

        <response>
        Response MUST be in JSON format
        Response MUST start with: {"success":
        </response>
    """))

    relationship_template = PromptTemplate(textwrap.dedent(
        """
        <persona>

        You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence. You have a deep understanding of cybersecurity concepts and threat intelligence. You are responsible for extracting observables and TTPs from documents provided, and understanding the relationships being described that link them.

        </persona>

        <requirement>
        The tag `<extractions>` contains all the observables and TTPs that were extracted from the document provided in `<document>`

        Please capture the relationships between the extractions and describe them using NLP techniques.

        A relationship MUST have different source_ref and target_ref

        Select an appropriate relationship_type from `<relationship_types>`.
        
        Only use `related-to` or any other vague `relationship_type` as a last resort. 
        The value of relationship_type MUST be clear, and it SHOULD NOT describe everything as related-to each other unless they are related in context of the `<document>

        IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.

        </requirement>

        <accuracy>

        Think about your answer first before you respond.

        If you don't know the answer, reply with `success: false`, do not every try to make up an answer.
        IMPORTANT: response must be a json and conform to the provided schema, it must not contain anything extra. 

        </accuracy>

        <document>
        {input_file}
        </document>

        <extractions>
        {extractions}
        </extractions>

        <relationship_types>
        {relationship_types}
        </relationship_types>

        <response>
        Response MUST be in JSON format
        Response MUST start with: {"success":
        </response>
        """
        ))
    
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

    def extract_relationships(self, input_text, extractions, relationship_types: list[str]) -> RelationshipList:
        return self._get_relationship_program()(relationship_types=relationship_types, input_file=input_text, extractions=extractions)
    
    def extract_objects(self, input_text, extractors) -> ExtractionList:
        return self._get_extraction_program()(extractors=get_extractors_str(extractors), input_file=input_text)
    
    def __init__(self, *args, **kwargs) -> None:
        pass

    def count_tokens(self, input_text):
        logging.info("unsupported model `%s`, estimating using llama-index's default tokenizer", self.extractor_name)
        return len(get_tokenizer()(input_text))
    
    def __init_subclass__(cls, /, provider, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.provider = provider
        _ai_extractor_registry[provider] = cls

    @property
    def extractor_name(self):
        return f"{self.provider}:{self.llm.model}"