import uuid
import yaml
from .common import FatalException, NamedDict
from .extractions import Extractor

import yaml, re
import csv
from pathlib import Path


def load_lookup(extractor):
    if extractor.terms:
        return extractor.terms
    extractor.terms = set(Path(extractor.file).read_text().splitlines())
    return extractor.terms

def find_all(extractor, input_str, start_id=0):
    retval = {}
    for term in extractor.terms:
        indexes = find_get_indexes_re(term, input_str)
        observed = {"value": term, "start_index":[], "stix_mapping": extractor.stix_mapping, "type": extractor.slug}
        for index in indexes:
            observed["start_index"].append(index)
        if observed.get("start_index"):
            retval[f"extraction_{start_id+len(retval)}"] = observed
    return retval


def merge_lookups(extractors: list[Extractor]) -> list[tuple[str, str, str]]:
    retval = []
    for ex in extractors:
        load_lookup(ex)
        retval.extend([(term, ex.stix_mapping, ex.slug) for term in ex.terms])
    return sorted(retval, key=lambda kv: len(kv[0]), reverse=True)

def extract_all(extractors, input_str):
    terms_ex:list[tuple[str, str, str]] = merge_lookups(extractors)
    seen_indexes = set()
    retval = []
    for term, stix_mapping, slug in terms_ex:
        indexes = set(find_get_indexes_re(term, input_str))
        difference = list(indexes.difference(seen_indexes))
        seen_indexes.update(difference)
        if difference:
            retval.append({"value": term, "start_index":difference, "stix_mapping": stix_mapping, "type": slug})
    return retval

def find_get_indexes(term, input_str):
    idx = -1
    while True:
        idx = input_str.find(term, idx+1)
        if idx == -1:
            break
        yield idx

def find_get_indexes_re(term, input_str):
    input_str = " "+input_str+" "
    re_i = re.escape(term)
    rexp = []
    for right in [r"\s", r"\.", r",", r"!\s"]:
        rexp.append(r"\s"+ "(" + re_i +")" +right)
    for open, close in ['""', "[]", "()", "``", "''",]:
        rexp.append(re.escape(open)+ "(" + re_i +")" + re.escape(close))
    rexp = "|".join(rexp)
    r = re.compile(rexp, flags=re.IGNORECASE)
    for match in r.finditer(input_str):
        left, right = match.span()
        yield left
