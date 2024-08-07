import argparse, dotenv
from datetime import datetime
import glob
import uuid
import itertools
import fnmatch
import re
from pathlib import Path
import sys, os

from .utils import remove_data_images

from .common import UUID_NAMESPACE, FatalException

from .stix import txt2stixBundler, parse_stix, TLP_LEVEL
from .import extractions, aliases, lookups, pattern
from .ai_session import GenericAIExtractor, OpenAIAssistantExtractor, BaseAIExtractor
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

    return logging.root

def setLogFile(logger, file: Path):
    file.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving log to `{file.absolute()}`")
    handler = logging.FileHandler(file, "w")
    handler.formatter = logging.Formatter(fmt='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.info("=====================txt2stix======================")


MODULE_PATH = Path(__file__).parent.parent
INCLUDES_PATH = MODULE_PATH/"includes"
try:
    from . import includes
    INCLUDES_PATH = Path(includes.__file__).parent
except:
    pass

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

def parse_extractors_globbed(type, all_extractors, names):
    globbed_names = set()
    for name in names.split(","):
        matches = fnmatch.filter(all_extractors.keys(), name)
        if not matches:
            raise argparse.ArgumentTypeError(f'`{name}` has 0 matches')
        globbed_names.update(matches)
    filtered_extractors  = {}
    for extractor_name in globbed_names:
        try:
            extractor = all_extractors[extractor_name]
            extraction_processor  = filtered_extractors.get(extractor.type, {})
            if extractor.type in ["lookup", "whitelist"]:
                lookups.load_lookup(extractor)
            if extractor.type == "alias":
                aliases.load_alias(extractor)
            if extractor.type == "pattern":
                pattern.load_extractor(extractor)
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
    EXTRACTORS_PATH = INCLUDES_PATH/"extractions"
    all_extractors = extractions.parse_extraction_config(INCLUDES_PATH)
    
    parser = argparse.ArgumentParser(description="File Conversion Tool")

    inf_arg  = parser.add_argument("--input_file", "--input-file", required=True, help="The file to be converted. Must be .txt", type=Path)
    name_arg = parser.add_argument("--name", required=True, help="Name of the file, max 72 chars", default="stix-out")
    parser.add_argument("--created", required=False, default=datetime.now(), help="Allow user to optionally pass --created time in input, which will hardcode the time used in created times")
    parser.add_argument("--labels", type=parse_labels)
    parser.add_argument("--relationship_mode", choices=["ai", "standard"], required=True)
    parser.add_argument("--confidence", type=range_type(0,100), default=None, help="value between 0-100. Default if not passed is null.", metavar="[0-100]")
    parser.add_argument("--tlp_level", "--tlp-level", choices=TLP_LEVEL.levels().keys(), default="clear", help="TLP level, default is clear")
    parser.add_argument("--use_extractions", "--use-extractions", default={}, type=functools.partial(parse_extractors_globbed, "extractor", all_extractors),  help="Specify extraction types from the default/local extractions .yaml file", metavar="EXTRACTION1,EXTRACTION2")
    parser.add_argument("--use_identity", "--use-identity", help="Specify an identity file id (e.g., {\"type\":\"identity\",\"name\":\"demo\",\"identity_class\":\"system\"})", metavar="[stix2 identity json]", type=parse_stix)
    parser.add_argument("--use_aliases", "--use-aliases", type=functools.partial(parse_extractors_globbed, "alias", all_extractors), help="if you want to apply aliasing to the input doc (find and replace strings) you can pass their slug found in aliases/config.yaml (e.g. country_iso3_to_iso2). Default if not passed, no extractions applied.", default={}, metavar="ALIAS1,ALIAS2")
    parser.add_argument("--use_whitelist", type=functools.partial(parse_extractors_globbed, "whitelist", all_extractors), help="if you want to get the script to ignore certain values that might create extractions you can specify using whitelist/config.yaml (e.g. alexa_top_1000) related to the whitelist file you want to use. Default if not passed, no extractions applied.", default=[], metavar="whitelist1,whitelist2")

    args = parser.parse_args()
    if not args.input_file.exists():
        raise argparse.ArgumentError(inf_arg, "cannot open file")
    if len(args.name) > 72:
        raise argparse.ArgumentError(name_arg, "max 72 characters")

    #### process --use-extractions 
    for extraction_processor, extractors in args.use_extractions.items():
        args.use_extractions[extraction_processor] = extractors
    args.all_extractors  = all_extractors
    args.use_aliases = args.use_aliases.get("alias", {})
    return args

REQUIRED_ENV_VARIABLES = [
    "ARANGODB_HOST_URL",
    "ARANGODB_USERNAME",
    "ARANGODB_PASSWORD",
    "ARANGODB_DATABASE",
]
def load_env(input_length):
    dotenv.load_dotenv()
    for env in REQUIRED_ENV_VARIABLES:
        if not os.getenv(env):
            raise FatalException(f"env variable `{env}` required")
            
def extract_all(bundler: txt2stixBundler, extractors_map, aliased_input, ai_extractor: BaseAIExtractor=None):
    all_extracts = dict()
    if extractors_map.get("lookup"):
        try:
            lookup_extracts = lookups.extract_all(extractors_map["lookup"].values(), aliased_input)
            bundler.process_observables(lookup_extracts)
            all_extracts["lookup"] = lookup_extracts
        except BaseException as e:
            logging.exception("lookup extraction failed", exc_info=True)

    if extractors_map.get("pattern"):
        try:
            logging.info("using pattern extractors")
            pattern_extracts = pattern.extract_all(extractors_map["pattern"].values(), aliased_input)
            bundler.process_observables(pattern_extracts)
            all_extracts["pattern"] = pattern_extracts
        except BaseException as e:
            logging.exception("pattern extraction failed", exc_info=True)

    if extractors_map.get("ai"):
        logging.info("using ai extractors")
        if not ai_extractor:
            logging.error(f"use of ai extractors while {ai_extractor=}, skipping")
        else:
            try:
                ai_extractor.set_document(aliased_input)
                ai_extracts = ai_extractor.extract_objects(extractors_map["ai"].values())
                bundler.process_observables(ai_extracts)
                all_extracts["ai"] = ai_extracts
            except BaseException as e:
                logging.exception("AI extraction failed", exc_info=True)

    bundler.add_note(json.dumps(all_extracts), "Extractions")
    return all_extracts

def extract_relationships_with_ai(bundler: txt2stixBundler, aliased_input, all_extracts, ai_extractor_session: BaseAIExtractor):
    relationships = None
    try:
        ai_extractor_session.set_document(aliased_input)
        relationship_types = (INCLUDES_PATH/"helpers/stix_relationship_types.txt").read_text().splitlines()
        relationships = ai_extractor_session.extract_relationships(all_extracts, relationship_types)
        bundler.add_note(json.dumps(relationships), "Relationships")
        bundler.process_relationships(relationships)
    except BaseException as e:
        logging.exception("Relationship processing failed: %s", e)
    # convo_str = ai_extractor_session.get_conversation() if ai_extractor_session and ai_extractor_session.initialized else ""
    return relationships

def main():
    try:
        job_id = str(uuid.uuid4())
        logger = newLogger("txt2stix")
        setLogFile(logger, Path(f"logs/logs-{job_id}.log"))
        logger.info(f"Arguments: {json.dumps(sys.argv[1:])}")
        args = parse_args()
        
        input_text = remove_data_images(args.input_file.read_text())
        aliased_input = aliases.transform_all(args.use_aliases.values(), input_text)

        load_env(len(aliased_input))

        bundler = txt2stixBundler(args.name, args.use_identity, args.tlp_level, aliased_input, args.confidence, args.all_extractors, args.labels, created=args.created)
        bundler.add_note(json.dumps(sys.argv), "Config")
        convo_str = None

        bundler.whitelisted_values = args.use_whitelist
        ai_extractor_session = GenericAIExtractor.openai()
        if args.use_extractions.get("ai"):
            token_count = ai_extractor_session.calculate_token_count(aliased_input, ai_extractor_session.model)
            if  token_count > int(os.environ["INPUT_TOKEN_LIMIT"]):
                raise FatalException(f"input_file token count ({token_count}) exceeds INPUT_TOKEN_LIMIT ({os.environ['INPUT_TOKEN_LIMIT']})")
        all_extracts = extract_all(bundler, args.use_extractions, aliased_input, ai_extractor=ai_extractor_session)
 
        if args.relationship_mode == "ai" and sum(map(lambda x: len(x), all_extracts.values())):
            extract_relationships_with_ai(bundler, aliased_input, all_extracts, ai_extractor_session)
            
        convo_str = ai_extractor_session.get_conversation() if ai_extractor_session and ai_extractor_session.initialized else ""
            

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
