from typing import Any
import yaml
from pathlib import Path
from .common import NamedDict

class Extractor(NamedDict):
    extraction_key = None
    name = None
    type: str = None
    description = None
    created = None
    modified = None
    created_by = None
    version = None
    prompt_base = None
    prompt_helper = None
    prompt_extraction_processing = None
    prompt_positive_examples = None
    prompt_negative_examples = None
    stix_mapping = None
    prompt_extraction_extra = None


    def __init__(self, key, dct):
        super().__init__(dct)
        self.extraction_key = key
        self.slug = key
   
    def load(self):
        if self.type == "lookup":
            self.lookups = set()
            file = Path(self.file)
            for line in file.read_text().splitlines():
                self.lookups.add(line.strip())


class ExtractionConfig:
    def __init__(self, raw_dct):
        self.extractors = {}
        self.raw = raw_dct
        self.process_prompts()
    
    def __getitem__(self, key):
        if not key:
            return None
        keys = key.split(".")
        obj = self.extractors
        for key in keys:
            if key.isdigit():
                key = int(key)
            obj = obj[key]
        if isinstance(obj, str):
            return obj.format_map(self.extractors)
        return obj

    def process_prompts(self):
        for k, v in self.raw.items():
            if not isinstance(v, dict):
                continue
            self.extractors[k] = Extractor(k, v)

def parse_extraction_config(path: Path):
    config = {}
    for p in path.glob("*/config.yaml"):
        config.update(yaml.safe_load(p.open()))
    return ExtractionConfig(config)

# f = parse_extraction_config(Path("extractions/default.yaml"))
# print(f["ipv4_address_only.prompt_helper"], f["ipv4_address_only.extraction_key"])
