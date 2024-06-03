import argparse, dotenv
import uuid
import itertools
import re
from pathlib import Path
import sys, os

from .common import FatalException

from .stix import txt2stixBundle, parse_stix, TLP_LEVEL
from .import extractions, aliases, lookups, pattern
from .ai_session import AIExtractSession
from types import SimpleNamespace
import functools
from fnmatch import filter

import json, logging


def newLogger(name: str) -> logging.Logger:
    # Configure logging
    stream_handler = logging.StreamHandler()  # Log to stdout and stderr
    stream_handler.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.DEBUG,  # Set the desired logging level
        format=f"%(asctime)s [{name}] [%(levelname)s] %(message)s",
        handlers=[stream_handler],
        datefmt='%d-%b-%y %H:%M:%S'
    )

    return logging.getLogger("txt2stix")

def setLogFile(logger, file: Path):
    file.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving log to `{file.absolute()}`")
    handler = logging.FileHandler(file, "w")
    handler.formatter = logging.Formatter(fmt='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.info("=====================txt2stix======================")


MODULE_PATH = Path(__file__).parent.parent
EXTRACTORS_PATH = MODULE_PATH/"extractions"

def split_comma(s: str) -> list[str]:
    return s.split(",")

def range_type(min, max):
    def fn(astr):
        value = int(astr)
        if min<= value <= max:
            return value
        else:
            raise argparse.ArgumentTypeError(f'value {value} not in range [{min}-{max}]')
    return fn

def parse_labels(labels: str) -> list[str]:
    labels = labels.split(",")
    for label in labels:
        if not re.fullmatch(r"[a-zA-Z0-9]+", label):
            raise argparse.ArgumentTypeError(f"invalid label: {label}")

    return labels

def parse_extractors(type, all_extractors, names):
    filtered_extractors  = {}
    for extractor_name in names.split(","):
        try:
            extractor = all_extractors[extractor_name]
            extraction_processor  = filtered_extractors.get(extractor.type, {})
            if extractor.type in ["lookup", "whitelist"]:
                lookups.load_lookup(extractor)
            if extractor.type == "alias":
                aliases.load_alias(extractor)
            if extractor.type == "pattern":
                extractor.pattern_extractor = pattern.ALL_EXTRACTORS.get(extractor_name)
                if not extractor.pattern_extractor:
                    raise argparse.ArgumentTypeError(f"could not find associated python class for pattern")
                extractor.pattern_extractor.version = extractor.version
                extractor.pattern_extractor.stix_mapping = extractor.stix_mapping
            filtered_extractors[extractor.type] =  extraction_processor
            extraction_processor[extractor_name] = extractor
        except KeyError:
            raise argparse.ArgumentTypeError(f"no such {type} slug `{extractor_name}`")
        except BaseException as e:
            raise argparse.ArgumentTypeError(f"{type} `{extractor_name}`: {e}")
    if type == "whitelist":
        return lookups.merge_whitelists(filtered_extractors.get("whitelist", {}).values())
    return filtered_extractors

def parse_args():
    all_extractors = extractions.parse_extraction_config(EXTRACTORS_PATH)
    
    identities_path = MODULE_PATH/"/stix_identities"
    parser = argparse.ArgumentParser(description="File Conversion Tool")

    inf_arg  = parser.add_argument("--input_file", "--input-file", required=True, help="The file to be converted. Must be .txt", type=Path)
    name_arg = parser.add_argument("--name", required=True, help="Name of the file, max 72 chars", default="stix-out")
    parser.add_argument("--labels", type=parse_labels)
    parser.add_argument("--relationship_mode", choices=["ai", "standard"], required=True)
    parser.add_argument("--confidence", type=range_type(0,100), default=None, help="value between 0-100. Default if not passed is null.", metavar="[0-100]")
    parser.add_argument("--tlp_level", "--tlp-level", choices=TLP_LEVEL.levels().keys(), default="clear", help="TLP level, default is clear")
    extractions_arg = parser.add_argument("--use_extractions", "--use-extractions", default={}, type=functools.partial(parse_extractors, "extractor", all_extractors),  help="Specify extraction types from the default/local extractions .yaml file", metavar="EXTRACTION1,EXTRACTION2")
    id_arg   = parser.add_argument("--use_identity", "--use-identity", help="Specify an identity file id (e.g., {\"type\":\"identity\",\"name\":\"demo\",\"identity_class\":\"system\"})", metavar="[stix2 identity json]", type=parse_stix)
    parser.add_argument("--use_aliases", "--use-aliases", type=functools.partial(parse_extractors, "alias", all_extractors), help="if you want to apply aliasing to the input doc (find and replace strings) you can pass their slug found in aliases/config.yaml (e.g. country_iso3_to_iso2). Default if not passed, no extractions applied.", default={}, metavar="ALIAS1,ALIAS2")
    parser.add_argument("--use_whitelist", type=functools.partial(parse_extractors, "whitelist", all_extractors), help="if you want to get the script to ignore certain values that might create extractions you can specify using whitelist/config.yaml (e.g. alexa_top_1000) related to the whitelist file you want to use. Default if not passed, no extractions applied.", default=[], metavar="whitelist1,whitelist2")

    args = parser.parse_args()
    if not args.input_file.exists():
        raise argparse.ArgumentError(inf_arg, "cannot open file")
    if len(args.name) > 72:
        raise argparse.ArgumentError(name_arg, "max 72 characters")

    #### process --use-extractions 
    for extraction_processor, extractors in args.use_extractions.items():
        args.use_extractions[extraction_processor] = extractions.ExtractionConfig(extractors)
    args.all_extractors  = all_extractors
    args.use_aliases = args.use_aliases.get("alias", {})



    # args.identity_path = identities_path/args.use_identity
    # if not args.identity_path.exists():
    #     raise argparse.ArgumentError(id_arg, "cannot open file")
    return args

REQUIRED_ENV_VARIABLES = [
    "INPUT_CHARACTER_LIMIT",
    "ARANGODB_HOST",
    "ARANGODB_PORT",
    "ARANGODB_USERNAME",
    "ARANGODB_PASSWORD",
    "ARANGODB_DATABASE",
]
def load_env(input_length):
    dotenv.load_dotenv()
    for env in REQUIRED_ENV_VARIABLES:
        if not os.getenv(env):
            raise FatalException(f"env variable `{env}` required")
    if input_length > int(os.environ["INPUT_CHARACTER_LIMIT"]):
        raise FatalException(f"input_file length ({input_length}) exceeds character limit ({os.environ['INPUT_CHARACTER_LIMIT']})")


def main():
    try:
        job_id = str(uuid.uuid4())
        logger = newLogger("txt2stix")
        setLogFile(logger, Path(f"logs/logs-{job_id}.txt"))
        logger.info(f"Arguments: {json.dumps(sys.argv[1:])}")
        args = parse_args()
        
        some_id = None
        aliased_input = note_in = args.input_file.read_text()
        for term, alias in aliases.merge_aliases(args.use_aliases.values()):
            # aliased_input = aliased_input.replace(value, alias)
            for index in lookups.find_get_indexes_re(term, aliased_input):
                aliased_input = aliased_input[:index] + alias + aliased_input[index+len(term):]

        load_env(len(aliased_input))

        bundler = txt2stixBundle(args.name, args.use_identity, args.tlp_level, aliased_input, args.confidence, args.all_extractors, args.labels, job_id=job_id)
        bundler.add_note(json.dumps(sys.argv), "Config")
        convo_str = None

        bundler.whitelisted_values = args.use_whitelist

        # ai_extracts = {}
        # lookup_extracts = {}
        # pattern_extracts = {}
        all_extracts = dict()

        
        chat_session = None
        if args.use_extractions.get("lookup"):
            try:
                # print(len(lookups.merge_lookups(args.use_extractions["lookup"].extractors.values())))
                start_index = sum(map(lambda ex:len(ex["extractions"]), all_extracts.values()))
                lookup_terms_ex_zip = lookups.merge_lookups(args.use_extractions["lookup"].extractors.values())
                lookup_extracts = lookups.find_all_lookup(lookup_terms_ex_zip, aliased_input, start_index)
                lookup_extracts = dict(extractions=lookup_extracts)
                bundler.process_observables(lookup_extracts, add_standard_relationship=args.relationship_mode != "ai")
                all_extracts["lookup"] = lookup_extracts
            except BaseException as e:
                logger.exception("lookup extraction failed", exc_info=True)

        if args.use_extractions.get("pattern"):
            try:
                start_index = sum(map(lambda ex:len(ex["extractions"]), all_extracts.values()))
                logger.info("using pattern extractors")
                pattern_extracts = {}
                for extractor in args.use_extractions["pattern"].extractors.values():
                    extracts = extractor.pattern_extractor().extract_extraction_from_text(aliased_input, extraction_index=start_index)
                    pattern_extracts.update(extracts)
                    start_index += len(extracts)
                all_extracts["pattern"] = dict(extractions=pattern_extracts)
                bundler.process_observables(all_extracts["pattern"], add_standard_relationship=args.relationship_mode != "ai")
            except BaseException as e:
                logger.exception("pattern extraction failed", exc_info=True)
        if args.use_extractions.get("ai"):
            try:
                chat_session = AIExtractSession.openai()
                chat_session.set_document(aliased_input)
                ai_extracts = chat_session.extract_observables(args.use_extractions["ai"])
                bundler.process_observables(ai_extracts, add_standard_relationship=args.relationship_mode != "ai")
                all_extracts["ai"] = ai_extracts
            except BaseException as e:
                logger.exception("AI extraction failed", exc_info=True)
        

        bundler.add_note(json.dumps(all_extracts), "Extractions")
        if args.relationship_mode == "ai" and sum(map(lambda x: len(x["extractions"]), all_extracts.values())):
            chat_session = chat_session or AIExtractSession.openai()
            # print("// warning AI relationship mode may fail")
            try:
                if not all_extracts.get("ai"):
                    chat_session.set_document(aliased_input)
                chat_session.set_other_extractions(all_extracts)
                relationship_types = (MODULE_PATH/"helpers/stix_relationship_types.txt").read_text().splitlines()
                relationships = chat_session.extract_relationships(relationship_types)
                bundler.add_note(json.dumps(relationships), "Relationships")
                bundler.process_relationships(relationships["relationships"])
            except BaseException as e:
                logger.exception("Relationship processing failed:", e)
        convo_str = chat_session.get_conversation() if chat_session else ""
            

        out = bundler.to_json()
        output_path = Path("./output")/f"{bundler.bundle.id}.json"
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text(out)
        logger.info(f"Writing bundle output to `{output_path}`")
        log_path = Path("./logs/chat-log--%s.txt"%bundler.bundle.id.split("--")[1])
        if convo_str:
            logger.info(f"Writing chat log to `{log_path}`")
            log_path.parent.mkdir(exist_ok=True)
            log_path.write_text(convo_str)
    except argparse.ArgumentError as e:
        logger.exception(e, exc_info=True)
    except:
        raise