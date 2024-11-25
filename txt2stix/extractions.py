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


    def __init__(self, key, dct, include_path=None, test_cases: dict[str, list[str]]=None):
        super().__init__(dct)
        self.extraction_key = key
        self.slug = key
        if test_cases:
            self.prompt_negative_examples = test_cases.get('test_negative_examples', [])
            self.prompt_positive_examples = test_cases.get('test_positive_examples', [])
        if self.file and not Path(self.file).is_absolute() and include_path:
            self.file = Path(include_path) / self.file


    def load(self):
        if self.type == "lookup":
            self.lookups = set()
            file = Path(self.file)
            for line in file.read_text().splitlines():
                self.lookups.add(line.strip())

def parse_extraction_config(include_path: Path):
    config = {}
    test_cases = load_test_cases_config(include_path)
    for p in include_path.glob("extractions/*/config.yaml"):
        config.update(yaml.safe_load(p.open()))
    
    return {k: Extractor(k, v, include_path, test_cases=test_cases.get(v.get('test_cases'))) for k, v in config.items()}

def load_test_cases_config(include_path: Path) -> dict[str, dict[str, list[str]]]:
    config_file = include_path/'tests/test_cases.yaml'
    if not config_file.exists():
        return {}
    return yaml.safe_load(config_file.open())