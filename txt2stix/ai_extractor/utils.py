import io
import json
import logging

import dotenv
import textwrap

import json_repair

from ..extractions import Extractor

from pydantic import BaseModel, Field, RootModel
from llama_index.core.output_parsers import PydanticOutputParser
from .data_models import Extraction, Relationship, ExtractionList, RelationshipList, DescribesIncident, AttackFlowItem, AttackFlowList

class ParserWithLogging(PydanticOutputParser):
    def parse(self, text: str):
        f = io.StringIO()
        print("\n"*5 + "=================start=================", file=f)
        print(text, file=f)
        print("=================close=================" + "\n"*5, file=f)
        logging.debug(f.getvalue())
        repaired_json = json_repair.repair_json(text)
        return super().parse(repaired_json)

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
