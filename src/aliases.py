import yaml, csv
from pathlib import Path

from .common import FatalException

def load_alias(extractor):
    if extractor.aliases:
        return extractor.aliases
    csv.list_dialects()
    with Path(extractor.file).open() as f:
        f.readline() # skip header line
        reader = csv.reader(f, delimiter=',')
        extractor.aliases = {}
        for row in reader:
            if len(row) != 2:
                raise FatalException(f"Line must have exactly two values, found {len(row)} [{row}]")
            extractor.aliases[row[0]] = row[1]
        return extractor.aliases


def merge_aliases(extractors):
    terms = set()
    for ex in extractors:
        terms.update(ex.aliases.items())
    # sort by length in descending order, this helps by making sure "A and B" is aliased before of "A" or "B"    
    return sorted(terms, key=lambda kv: len(kv[0]), reverse=True)
