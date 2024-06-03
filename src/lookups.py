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


def merge_lookups(extractors) -> list[tuple[str, Extractor]]:
    retval = []
    for ex in extractors:
        retval.extend(zip(ex.terms, [ex]*len(ex.terms)))
    return sorted(retval, key=lambda kv: len(kv[0]), reverse=True)

def find_all_lookup(terms_ex:list[tuple[str, Extractor]], input_str, start_id=0):
    seen_indexes = set()
    retval = {}
    for term, extractor in terms_ex:
        indexes = set(find_get_indexes_re(term, input_str))
        difference = list(indexes.difference(seen_indexes))
        seen_indexes.update(difference)
        if difference:
            retval[f"extraction_{start_id+len(retval)}"] = {"value": term, "start_index":difference, "stix_mapping": extractor.stix_mapping, "type": extractor.slug}
    return retval

def find_get_indexes(term, input_str):
    idx = -1
    while True:
        idx = input_str.find(term, idx+1)
        if idx == -1:
            break
        yield idx

def find_get_indexes_re(term, input_str):

    re_i = re.escape(term)
    rexp = []
    for right in [r"\s", r"\.", r",", r"!\s"]:
        rexp.append(r"\s"+ "(" + re_i +")" +right)
    for open, close in ['""', "[]", "()", "``", "''",]:
        rexp.append(re.escape(open)+ "(" + re_i +")" + re.escape(close))
    rexp = "|".join(rexp)
    r = re.compile(rexp)
    for match in r.finditer(input_str):
        left, right = match.span()
        yield left+1


def merge_whitelists(whitelist_extractors):
    terms = set()
    for extractor in whitelist_extractors:
        try:
            eterms = extractor.terms or Path(extractor.file).read_text().splitlines()
            terms.update(eterms)
        except Exception as e:
            raise FatalException(f"cannot load whitelist `{extractor.slug}`: {e}")
    return terms
    



if __name__ == "__main__":
    from .extractions import parse_extraction_config
    extractions = parse_extraction_config(Path(__file__).parent.parent/"extractions")
    # lookups = load_config()
    l1 = extractions['lookup_mitre_attack_ics_id']
    load_lookup(l1)
    ss = "'TA0108', 'TA0105', 'TA0110, 'TA0104', 'TA0101', 'TA0100', 'TA0103', 'TA0106', 'T0803', 'T0881', 'T0836', 'T0821'[]'TA0108', 'TA0105', 'TA0110', 'TA0104', 'TA0101',"
    print(list(find_get_indexes_re("TA0110", ss)))
    print(list(find_get_indexes("TA0110", ss)))
    print(find_all(l1, ss))
