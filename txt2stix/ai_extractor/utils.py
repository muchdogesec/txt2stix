import io
import logging

import dotenv
import textwrap

from ..extractions import Extractor

from pydantic import BaseModel, Field
from llama_index.core.output_parsers import PydanticOutputParser


dotenv.load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("txt2stix.ai_extractor")
logger.setLevel(logging.DEBUG)

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
    extractions: list[Extraction]
    success: bool

class RelationshipList(BaseModel):
    relationships: list[Relationship]
    success: bool



class ParserWithLogging(PydanticOutputParser):
    def parse(self, text: str):
        f = io.StringIO()
        print("\n"*5 + "=================start=================", file=f)
        print(text, file=f)
        print("=================close=================" + "\n"*5, file=f)
        logging.info(f.getvalue())
        return super().parse(text)

def get_extractors_str(extractors):
    extractor: Extractor = None
    extractors_str = []
    for extractor in extractors:
        extractor_str = textwrap.dedent(
        f"""
        <extractor name={repr(extractor.name)} extraction_key={repr(extractor.extraction_key)}>
        - {extractor.prompt_base}
        - {extractor.prompt_conversion}
        </extractor>
        """
        )
        extractors_str.append(extractor_str)
    return "".join(extractors_str)



if __name__ == '__main__':
    a = ExtractionList(extractions=[Extraction(type="yes", id="1", value="2", original_text="3")], success=True)
    print(a.model_dump())