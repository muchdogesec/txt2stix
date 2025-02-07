import logging
from typing import Type
from llama_index.core.program import LLMTextCompletionProgram

import textwrap
from llama_index.core import PromptTemplate
from llama_index.core.llms.llm import LLM

from txt2stix.ai_extractor.utils import DescribesIncident, ExtractionList, ParserWithLogging, RelationshipList, get_extractors_str
from llama_index.core.utils import get_tokenizer


_ai_extractor_registry: dict[str, 'Type[BaseAIExtractor]'] = {}
class BaseAIExtractor():
    system_prompt = (textwrap.dedent(
        """
        <persona>

            You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence provided in text files.

            You have a deep understanding of cybersecurity and threat intelligence concepts.

             IMPORTANT: You must always deliver your work as a computer-parsable output in JSON format. All output from you will be parsed with pydantic for further processing.
        
        </persona>
        """
    ))
    extraction_template = PromptTemplate(textwrap.dedent(
        """
        <persona>

            You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence provided in text files.

            You have a deep understanding of cybersecurity and threat intelligence concepts.

            IMPORTANT: You must always deliver your work as a computer-parsable output in JSON format. All output from you will be parsed with pydantic for further processing.
        
        </persona>

        <requirements>

            Using the report text printed between the `<document>` tags, you should extract the Indicators of Compromise (IoCs) and Tactics, Techniques, and Procedures (TTPs) being described in it.

            The document can contain the same IOC or TTP one or more times. Only create one record for each extraction -- the extractions must be unique!
            
            Only one JSON object should exist for each unique value.

        </requirements>

        <accuracy>

            Think about your answer first before you respond. The accuracy of your response is very important as this data will be used for operational purposes.

            If you don't know the answer, reply with success: false, do not ever try to make up an answer.

        </accuracy>

        <document>

        {input_file}
        
        </document>

        <extractors>
        
        {extractors}
        
        </extractors>

        <response>

            IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.

            Response MUST be in JSON format.
            
            Response MUST start with: {"success":
        </response>
        """
    ))

    relationship_template = PromptTemplate(textwrap.dedent(
        """
        <persona>

            You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence provided in text files.

            You have a deep understanding of cybersecurity and threat intelligence concepts.

            IMPORTANT: You must always deliver your work as a computer-parsable output in JSON format. All output from you will be parsed with pydantic for further processing.
        
        </persona>

        <requirements>

            The tag `<extractions>` contains all the observables and TTPs that were extracted from the document provided in `<document>`

            Please capture the relationships between the extractions and describe them using NLP techniques.

            A relationship MUST have different source_ref and target_ref

            Select an appropriate relationship_type from `<relationship_types>`.
            
            Only use `related-to` or any other vague `relationship_type` as a last resort. 
            
            The value of relationship_type MUST be clear, and it SHOULD NOT describe everything as related-to each other unless they are related in context of the `<document>

            IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.

        </requirements>

        <accuracy>

            Think about your answer first before you respond. The accuracy of your response is very important as this data will be used for operational purposes.

            If you don't know the answer, reply with success: false, do not ever try to make up an answer.

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

            IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.

            Response MUST be in JSON format.
            
            Response MUST start with: {"success":
        </response>
        """
        ))
    
    content_check_template = PromptTemplate(
        """
        <persona>

        You are a cyber security threat intelligence analyst.

        Your job is to review text from reports that describe threat intelligence.

        Examples include malware analysis, APT group reports, data breaches, vulnerabilities, and lists of indicators of compromise (e.g. IP addresses).

        Some of the documents you are given are not related to such topics. The first part of your job is to figure out wether a report contains threat intelligence.

        I need you to tell me if the text contains threat intelligence.

        </persona>

        <requirement>

        Using the MARKDOWN of the report provided in <document>
        IMPORTANT: the output should be structured as valid JSON.
        IMPORTANT: output should not be in markdown, it must be a plain JSON text without any code block
        IMPORTANT: do not include any comment in the output
        IMPORTANT: output must start with a `{` and end with a `}` and must not contain "```"

        </requirement>
                                
        <document>
        {context_str}
        </document>
        """
    )
    
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