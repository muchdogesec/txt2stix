import io
import json
import logging

import dotenv
import textwrap

from ..extractions import Extractor

from pydantic import BaseModel, Field, RootModel
from llama_index.core.output_parsers import PydanticOutputParser

class Extraction(BaseModel):
    type : str = Field(description="is the extraction_key value shown in the list printed earlier in this prompt")
    id: str =  Field(description='is the id of the extraction of the format `"ai-%d" %(position in list)`, it should start from 1 (e.g `"ai-1", "ai-2", ..., "ai-n"`)')
    value: str  =  Field(description='is the value extracted from the text')
    original_text: str =  Field(description='is the original text the extraction was made from')
    # start_index: list[str|int] =  Field(description='a list of the index positions of the first character for each matching extraction. Some documents might capture many extractions where `key` and `value` are the same for many entries. This property allows the user to identify how many extractions happened, and where they are in the document.')

class Relationship(BaseModel):
    source_ref: str = Field(description='is the id for the source extraction for the relationship (e.g. extraction_1).')
    target_ref: str = Field(description='is the index for the target extraction for the relationship (e.g. extraction_2).')
    relationship_type: str = Field(description='is a description of the relationship between target and source.')

class ExtractionList(BaseModel):
    extractions: list[Extraction] = Field(default_factory=list)
    success: bool

class RelationshipList(BaseModel):
    relationships: list[Relationship] = Field(default_factory=list)
    success: bool

class DescribesIncident(BaseModel):
    describes_incident: bool = Field(description="does the <document> include malware analysis, APT group reports, data breaches and vulnerabilities?")
    explanation: str = Field(description="Two or three sentence summary of the incidents it describes OR summary of what it describes instead of an incident")
    incident_classification : list[str] = Field(description="All the valid incident classifications that describe this document/report")
    summary: str = Field(description="executive summary of the document containing no more than one paragraphs.")

class AttackFlowItem(BaseModel):
    position : int = Field(description="order of object starting at 0")
    attack_technique_id : str
    name: str
    description: str

class AttackFlowList(BaseModel):
    tactic_selection: list[tuple[str, str]] = Field(description="attack technique id to attack tactic id mapping using possible_tactics")
    # additional_tactic_mapping: list[tuple[str, str]] = Field(description="the rest of tactic_mapping")
    items : list[AttackFlowItem]
    success: bool = Field(description="determines if there's any valid flow in <extractions>")

    def model_post_init(self, context):
        return super().model_post_init(context)
    
    @property
    def tactic_mapping(self):
        return dict(self.tactic_selection)

class ParserWithLogging(PydanticOutputParser):
    def parse(self, text: str):
        f = io.StringIO()
        print("\n"*5 + "=================start=================", file=f)
        print(text, file=f)
        print("=================close=================" + "\n"*5, file=f)
        logging.debug(f.getvalue())
        return super().parse(text)

def get_extractors_str(extractors):
    extractor: Extractor = None
    buffer = io.StringIO()
    for extractor in extractors:
        print(f"<extractor name={repr(extractor.name)} extraction_key={repr(extractor.extraction_key)}>", file=buffer)
        print(f"- {extractor.prompt_base}", file=buffer)
        if extractor.prompt_helper:
            print(f"- {extractor.prompt_helper}", file=buffer)
        if extractor.prompt_conversion:
            print(f"- {extractor.prompt_conversion}", file=buffer)
        if extractor.prompt_positive_examples:
            print(f"- Here are some examples of what SHOULD be extracted for {extractor.name} extractions: {json.dumps(extractor.prompt_positive_examples)}", file=buffer)
        if extractor.prompt_negative_examples:
            print(f"- Here are some examples of what SHOULD NOT be extracted for {extractor.name} extractions: {json.dumps(extractor.prompt_negative_examples)}", file=buffer)
        print("</extractor>", file=buffer)
        print("\n"*2, file=buffer)

    logging.debug("========   extractors   ======")
    logging.debug(buffer.getvalue())
    logging.debug("======== extractors end ======")
    return buffer.getvalue()



if __name__ == '__main__':
    a = ExtractionList(extractions=[Extraction(type="yes", id="1", value="2", original_text="3")], success=True)
    print(a.model_dump())