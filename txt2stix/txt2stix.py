import argparse, dotenv
from datetime import datetime
import glob
import uuid
import itertools
import fnmatch
import re
from pathlib import Path
import sys, os

from pydantic import BaseModel

from txt2stix.ai_extractor.utils import DescribesIncident
from txt2stix.attack_flow import parse_flow


from .utils import Txt2StixData, remove_links

from .common import UUID_NAMESPACE, FatalException

from .stix import txt2stixBundler, parse_stix, TLP_LEVEL
from .import extractions, lookups, pattern
from types import SimpleNamespace
import functools
from fnmatch import filter
from .ai_extractor import ALL_AI_EXTRACTORS, BaseAIExtractor, ModelError
from stix2.serialization import serialize as stix2_serialize
from stix2 import Bundle

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
    return [ss for ss in s.split(",") if ss]

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
            if extractor.type in ["lookup"]:
                lookups.load_lookup(extractor)
            if extractor.type == "pattern":
                pattern.load_extractor(extractor)
            filtered_extractors[extractor.type] =  extraction_processor
            extraction_processor[extractor_name] = extractor
        except KeyError:
            raise argparse.ArgumentTypeError(f"no such {type} slug `{extractor_name}`")
        except BaseException as e:
            raise argparse.ArgumentTypeError(f"{type} `{extractor_name}`: {e}")
    return filtered_extractors

def parse_ref(value):
    m = re.compile(r'(.+?)=(.+)').match(value)
    if not m:
        raise argparse.ArgumentTypeError("must be in format key=value")
    return dict(source_name=m.group(1), external_id=m.group(2))

def parse_model(value: str):
    splits = value.split(':', 1)
    provider = splits[0]
    if provider not in ALL_AI_EXTRACTORS:
        raise argparse.ArgumentTypeError(f"invalid AI provider in `{value}`, must be one of {list(ALL_AI_EXTRACTORS)}")
    provider = ALL_AI_EXTRACTORS[provider]

    try:
        if len(splits) == 2:
            return provider(model=splits[1])
        return provider()
    except Exception as e:
        raise ModelError(f"Unable to initialize model `{value}`") from e

def parse_bool(value: str):
    value = value.lower()
    return value in ["yes", "y", "true", "1"]

def parse_args():
    EXTRACTORS_PATH = INCLUDES_PATH/"extractions"
    all_extractors = extractions.parse_extraction_config(INCLUDES_PATH)
    
    parser = argparse.ArgumentParser(description="File Conversion Tool")

    inf_arg  = parser.add_argument("--input_file", "--input-file", required=True, help="The file to be converted. Must be .txt", type=Path)
    parser.add_argument("--ai_content_check_provider", required=False, type=parse_model, help="Use an AI model to check wether the content of the file contains threat intelligence. Paticularly useful to weed out vendor marketing.")
    name_arg = parser.add_argument("--name", required=True, help="Name of the file, max 124 chars", default="stix-out")
    parser.add_argument("--created", required=False, default=datetime.now(), help="Allow user to optionally pass --created time in input, which will hardcode the time used in created times")
    parser.add_argument("--ai_settings_extractions", required=False, type=parse_model, help="(required if AI extraction enabled): passed in format provider:model e.g. openai:gpt4o. Can pass more than one value to get extractions from multiple providers.", metavar="provider[:model]", nargs='+')
    parser.add_argument("--ai_settings_relationships", required=False, type=parse_model, help="(required if AI relationship enabled): passed in format `provider:model`. Can only pass one model at this time.", metavar="provider[:model]")
    parser.add_argument("--labels", type=parse_labels)
    parser.add_argument("--relationship_mode", choices=["ai", "standard"], required=True)
    parser.add_argument("--report_id", type=uuid.UUID, required=False, help="id to use instead of automatically generated `{name}+{created}`", metavar="VALID_UUID")
    parser.add_argument("--confidence", type=range_type(0,100), default=None, help="value between 0-100. Default if not passed is null.", metavar="[0-100]")
    parser.add_argument("--tlp_level", "--tlp-level", choices=TLP_LEVEL.levels().keys(), default="clear", help="TLP level, default is clear")
    parser.add_argument("--use_extractions", "--use-extractions", default={}, type=functools.partial(parse_extractors_globbed, "extractor", all_extractors),  help="Specify extraction types from the default/local extractions .yaml file", metavar="EXTRACTION1,EXTRACTION2")
    parser.add_argument("--use_identity", "--use-identity", help="Specify an identity file id (e.g., {\"type\":\"identity\",\"name\":\"demo\",\"identity_class\":\"system\"})", metavar="[stix2 identity json]", type=parse_stix)
    parser.add_argument("--external_refs", type=parse_ref, help="pass additional `external_references` entry (or entries) to the report object created. e.g --external_ref author=dogesec link=https://dkjjadhdaj.net", default=[], metavar="{source_name}={external_id}", action="extend", nargs='+')
    parser.add_argument('--ignore_image_refs', default=True, type=parse_bool)
    parser.add_argument('--ignore_link_refs', default=True, type=parse_bool)
    parser.add_argument("--ignore_extraction_boundary", default=False, type=parse_bool, help="default if not passed is `false`, but if set to `true` will ignore boundary capture logic for extractions")
    parser.add_argument('--ai_create_attack_flow', default=False, action='store_true', help="create attack flow for attack objects in report/bundle")

    args = parser.parse_args()
    if not args.input_file.exists():
        raise argparse.ArgumentError(inf_arg, "cannot open file")
    if len(args.name) > 124:
        raise argparse.ArgumentError(name_arg, "max 124 characters")

    if args.relationship_mode == 'ai' and not args.ai_settings_relationships:
        parser.error("relationship_mode is set to AI, --ai_settings_relationships is required")

    if args.ai_create_attack_flow and not args.ai_settings_relationships:
        parser.error("--ai_create_attack_flow requires --ai_settings_relationships")
    #### process --use-extractions 
    if args.use_extractions.get('ai') and not args.ai_settings_extractions:
        parser.error("ai based extractors are passed, --ai_settings_extractions is required")

    args.all_extractors  = all_extractors
    return args

REQUIRED_ENV_VARIABLES = [
    "INPUT_TOKEN_LIMIT",
    "CTIBUTLER_BASE_URL",
    "VULMATCH_BASE_URL",
]
def load_env():
    for env in REQUIRED_ENV_VARIABLES:
        if not os.getenv(env):
            raise FatalException(f"env variable `{env}` required")


def log_notes(content, type):
    logging.debug(f" ========================= {type} ========================= ")
    logging.debug(f" ========================= {'+'*len(type)} ========================= ")
    logging.debug(json.dumps(content, sort_keys=True, indent=4))
    logging.debug(f" ========================= {'-'*len(type)} ========================= ")

def extract_all(bundler: txt2stixBundler, extractors_map, text_content, ai_extractors: list[BaseAIExtractor]=[], **kwargs):
    assert ai_extractors or not extractors_map.get("ai"), "There should be at least one AI extractor in ai_extractors"

    text_content = "\n"+text_content+"\n"
    all_extracts = dict()
    if extractors_map.get("lookup"):
        try:
            lookup_extracts = lookups.extract_all(extractors_map["lookup"].values(), text_content)
            bundler.process_observables(lookup_extracts)
            all_extracts["lookup"] = lookup_extracts
        except BaseException as e:
            logging.exception("lookup extraction failed", exc_info=True)

    if extractors_map.get("pattern"):
        try:
            logging.info("using pattern extractors")
            pattern_extracts = pattern.extract_all(extractors_map["pattern"].values(), text_content, ignore_extraction_boundary=kwargs.get('ignore_extraction_boundary', False))
            bundler.process_observables(pattern_extracts)
            all_extracts["pattern"] = pattern_extracts
        except BaseException as e:
            logging.exception("pattern extraction failed", exc_info=True)

    if extractors_map.get("ai"):
        logging.info("using ai extractors")

        for extractor in ai_extractors:
            logging.info("running extractor: %s", extractor.extractor_name)
            try:
                ai_extracts = extractor.extract_objects(text_content, extractors_map["ai"].values())
                ai_extracts = ai_extracts.model_dump().get('extractions', [])
                bundler.process_observables(ai_extracts)
                all_extracts[f"ai-{extractor.extractor_name}"] = ai_extracts
            except BaseException as e:
                logging.exception("AI extraction failed for %s", extractor.extractor_name, exc_info=True)

    log_notes(all_extracts, "Extractions")
    return all_extracts

def extract_relationships_with_ai(bundler: txt2stixBundler, text_content, all_extracts, ai_extractor_session: BaseAIExtractor):
    relationships = None
    try:
        all_extracts = list(itertools.chain(*all_extracts.values()))
        relationship_types = (INCLUDES_PATH/"helpers/stix_relationship_types.txt").read_text().splitlines()
        relationships = ai_extractor_session.extract_relationships(text_content, all_extracts, relationship_types)
        relationships = relationships.model_dump()
        log_notes(relationships, "Relationships")
        bundler.process_relationships(relationships['relationships'])
    except BaseException as e:
        logging.exception("Relationship processing failed: %s", e)
    return relationships

def validate_token_count(max_tokens, input, extractors: list[BaseAIExtractor]):
    logging.info('INPUT_TOKEN_LIMIT = %d', max_tokens)
    for extractor in extractors:
        token_count = _count_token(extractor, input)
        if  token_count > max_tokens:
            raise FatalException(f"{extractor.extractor_name}: input_file token count ({token_count}) exceeds INPUT_TOKEN_LIMIT ({max_tokens})")
    

@functools.lru_cache
def _count_token(extractor: BaseAIExtractor, input: str):
    return extractor.count_tokens(input)
        
def run_txt2stix(bundler: txt2stixBundler, preprocessed_text: str, extractors_map: dict,
                ai_content_check_provider=None,
                ai_create_attack_flow=None,
                input_token_limit=10,
                ai_settings_extractions=None,
                ai_settings_relationships=None,
                relationship_mode="standard",
                ignore_extraction_boundary=False,
                always_extract=False, # continue even if ai_content_check fails

                **kwargs
        ) -> Txt2StixData:
    should_extract = True
    retval = Txt2StixData.model_construct()
    retval.extractions = retval.attack_flow = retval.relationships = None
    if ai_content_check_provider:
        logging.info("checking content")
        model : BaseAIExtractor = ai_content_check_provider
        validate_token_count(input_token_limit, preprocessed_text, [model])
        retval.content_check = model.check_content(preprocessed_text)
        should_extract = retval.content_check.describes_incident
        logging.info("=== ai-check-content output ====")
        logging.info(retval.content_check.model_dump_json())
        for classification in retval.content_check.incident_classification:
            bundler.report.labels.append(f'txt2stix:{classification}'.lower())

    if should_extract or always_extract:
        if extractors_map.get("ai"):
            validate_token_count(input_token_limit, preprocessed_text, ai_settings_extractions)
        if relationship_mode == "ai":
            validate_token_count(input_token_limit, preprocessed_text, [ai_settings_relationships])

        retval.extractions = extract_all(bundler, extractors_map, preprocessed_text, ai_extractors=ai_settings_extractions, ignore_extraction_boundary=ignore_extraction_boundary)
        if relationship_mode == "ai" and sum(map(lambda x: len(x), retval.extractions.values())):
            retval.relationships = extract_relationships_with_ai(bundler, preprocessed_text, retval.extractions, ai_settings_relationships)
            
        if ai_create_attack_flow:
            logging.info("creating attack-flow bundle")
            ex: BaseAIExtractor = ai_settings_relationships
            retval.attack_flow = ex.extract_attack_flow(preprocessed_text, retval.extractions, retval.relationships)
            bundler.flow_objects = parse_flow(bundler.report, retval.attack_flow)

    return retval

def main():
    dotenv.load_dotenv()
    logger = newLogger("txt2stix")
    try:
        args = parse_args()
        job_id = args.report_id or str(uuid.uuid4())
        setLogFile(logger, Path(f"logs/logs-{job_id}.log"))
        logger.info(f"Arguments: {json.dumps(sys.argv[1:])}")

        
        input_text = args.input_file.read_text()
        preprocessed_text = remove_links(input_text, args.ignore_image_refs, args.ignore_link_refs)
        load_env()


        bundler = txt2stixBundler(args.name, args.use_identity, args.tlp_level, input_text, args.confidence, args.all_extractors, args.labels, created=args.created, report_id=args.report_id, external_references=args.external_refs)
        log_notes(sys.argv, "Config")
        convo_str = None

        data = run_txt2stix(
            bundler, preprocessed_text, args.use_extractions,
            input_token_limit=int(os.environ['INPUT_TOKEN_LIMIT']),
            **args.__dict__,
        )

        ## write outputs
        out = bundler.to_json()
        output_path = Path("./output")/f"{bundler.bundle.id}.json"
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text(out)
        logger.info(f"Wrote bundle output to `{output_path}`")
        data_path = Path(str(output_path).replace('bundle--', 'data--'))
        data_path.write_text(data.model_dump_json(indent=4))
        logger.info(f"Wrote data output to `{data_path}`")
    except argparse.ArgumentError as e:
        logger.exception(e, exc_info=True)
    except:
        raise
