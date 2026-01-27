import argparse, dotenv
import contextlib
import shutil
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
from txt2stix import attack_flow, credential_checker


from .utils import RELATIONSHIP_TYPES, Txt2StixData, remove_links

from .common import UUID_NAMESPACE, FatalException

from .bundler import txt2stixBundler, parse_stix, TLP_LEVEL
from . import extractions, lookups, pattern
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
        datefmt="%d-%b-%y %H:%M:%S",
    )

    return logging.root


def setLogFile(logger, file: Path):
    file.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving log to `{file.absolute()}`")
    handler = logging.FileHandler(file, "w")
    handler.formatter = logging.Formatter(
        fmt="%(levelname)s %(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
    )
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.info("=====================txt2stix======================")


MODULE_PATH = Path(__file__).parent.parent
INCLUDES_PATH = MODULE_PATH / "includes"
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
        if min <= value <= max:
            return value
        else:
            raise argparse.ArgumentTypeError(
                f"value {value} not in range [{min}-{max}]"
            )

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
            raise argparse.ArgumentTypeError(f"`{name}` has 0 matches")
        globbed_names.update(matches)
    filtered_extractors = {}
    for extractor_name in globbed_names:
        try:
            extractor = all_extractors[extractor_name]
            extraction_processor = filtered_extractors.get(extractor.type, {})
            if extractor.type in ["lookup"]:
                lookups.load_lookup(extractor)
            if extractor.type == "pattern":
                pattern.load_extractor(extractor)
            filtered_extractors[extractor.type] = extraction_processor
            extraction_processor[extractor_name] = extractor
        except BaseException as e:
            raise argparse.ArgumentTypeError(f"{type} `{extractor_name}`: {e}")
    return filtered_extractors


def parse_ref(value):
    m = re.compile(r"(.+?)=(.+)").match(value)
    if not m:
        raise argparse.ArgumentTypeError("must be in format key=value")
    return dict(source_name=m.group(1), external_id=m.group(2))


def parse_model(value: str):
    splits = value.split(":", 1)
    provider = splits[0]
    if provider not in ALL_AI_EXTRACTORS:
        raise argparse.ArgumentTypeError(
            f"invalid AI provider in `{value}`, must be one of {list(ALL_AI_EXTRACTORS)}"
        )
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
    EXTRACTORS_PATH = INCLUDES_PATH / "extractions"
    all_extractors = extractions.parse_extraction_config(INCLUDES_PATH)

    parser = argparse.ArgumentParser(description="File Conversion Tool")
    parser.add_argument(
        "--check_credentials",
        "--check-credentials",
        action="store_true",
        help="Print the validity of the credentials and exit",
    )
    args, _ = parser.parse_known_args()
    if args.check_credentials:
        statuses = credential_checker.check_statuses(test_llms=True)
        credential_checker.format_statuses(statuses)
        sys.exit(0)

    inf_arg = parser.add_argument(
        "--input_file",
        "--input-file",
        required=True,
        help="The file to be converted. Must be .txt",
        type=Path,
    )
    parser.add_argument(
        "--ai_content_check_provider",
        required=False,
        type=parse_model,
        help="Use an AI model to check wether the content of the file contains threat intelligence. Paticularly useful to weed out vendor marketing.",
    )
    parser.add_argument(
        "--ai_extract_if_no_incidence",
        default=True,
        type=parse_bool,
        help="if content check decides the report is not related to cyber security intelligence (e.g. vendor marketing), then you can use this setting to decide wether or not script should proceed. Setting to `false` will stop processing. It is designed to save AI tokens processing unknown content at scale in an automated way.",
    )
    name_arg = parser.add_argument(
        "--name",
        required=True,
        help="Name of the file, max 124 chars",
        default="stix-out",
    )
    parser.add_argument(
        "--created",
        required=False,
        default=datetime.now(),
        help="Allow user to optionally pass --created time in input, which will hardcode the time used in created times",
    )
    parser.add_argument(
        "--ai_settings_extractions",
        required=False,
        type=parse_model,
        help="(required if AI extraction enabled): passed in format provider:model e.g. openai:gpt4o. Can pass more than one value to get extractions from multiple providers.",
        metavar="provider[:model]",
        nargs="+",
    )
    parser.add_argument(
        "--ai_settings_relationships",
        required=False,
        type=parse_model,
        help="(required if AI relationship enabled): passed in format `provider:model`. Can only pass one model at this time.",
        metavar="provider[:model]",
    )
    parser.add_argument("--labels", type=parse_labels)
    rmode_arg = parser.add_argument(
        "--relationship_mode", choices=["ai", "standard"], required=True
    )
    parser.add_argument(
        "--report_id",
        type=uuid.UUID,
        required=False,
        help="id to use instead of automatically generated `{name}+{created}`",
        metavar="VALID_UUID",
    )
    parser.add_argument(
        "--confidence",
        type=range_type(0, 100),
        default=None,
        help="value between 0-100. Default if not passed is null.",
        metavar="[0-100]",
    )
    parser.add_argument(
        "--tlp_level",
        "--tlp-level",
        choices=TLP_LEVEL.levels().keys(),
        default="clear",
        help="TLP level, default is clear",
    )
    extractions_arg = parser.add_argument(
        "--use_extractions",
        "--use-extractions",
        default={},
        type=functools.partial(parse_extractors_globbed, "extractor", all_extractors),
        help="Specify extraction types from the default/local extractions .yaml file",
        metavar="EXTRACTION1,EXTRACTION2",
    )
    parser.add_argument(
        "--use_identity",
        "--use-identity",
        help='Specify an identity file id (e.g., {"type":"identity","name":"demo","identity_class":"system"})',
        metavar="[stix2 identity json]",
        type=parse_stix,
    )
    parser.add_argument(
        "--external_refs",
        type=parse_ref,
        help="pass additional `external_references` entry (or entries) to the report object created. e.g --external_ref author=dogesec link=https://dkjjadhdaj.net",
        default=[],
        metavar="{source_name}={external_id}",
        action="extend",
        nargs="+",
    )
    parser.add_argument("--ignore_image_refs", default=True, type=parse_bool)
    parser.add_argument("--ignore_link_refs", default=True, type=parse_bool)
    parser.add_argument(
        "--ignore_extraction_boundary",
        default=False,
        type=parse_bool,
        help="default if not passed is `false`, but if set to `true` will ignore boundary capture logic for extractions",
    )
    aflow_arg = parser.add_argument(
        "--ai_create_attack_flow",
        default=False,
        action="store_true",
        help="create attack flow for attack objects in report/bundle",
    )

    anav_arg = parser.add_argument(
        "--ai_create_attack_navigator_layer",
        default=False,
        action="store_true",
        help="create attack flow for attack objects in report/bundle",
    )

    args = parser.parse_args()
    if not args.input_file.exists():
        raise argparse.ArgumentError(inf_arg, "cannot open file")
    if len(args.name) > 124:
        raise argparse.ArgumentError(name_arg, "max 124 characters")

    if args.relationship_mode == "ai" and not args.ai_settings_relationships:
        raise argparse.ArgumentError(
            rmode_arg,
            "relationship_mode is set to AI, --ai_settings_relationships is required",
        )

    if args.ai_create_attack_flow and not args.ai_settings_relationships:
        raise argparse.ArgumentError(
            aflow_arg, "--ai_settings_relationships must be set"
        )
    if args.ai_create_attack_navigator_layer and not args.ai_settings_relationships:
        raise argparse.ArgumentError(
            anav_arg, "--ai_settings_relationships must be set"
        )
    #### process --use-extractions
    if args.use_extractions.get("ai") and not args.ai_settings_extractions:
        raise argparse.ArgumentError(
            extractions_arg,
            "ai based extractors are passed, --ai_settings_extractions is required",
        )

    args.all_extractors = all_extractors
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
    logging.debug(
        f" ========================= {'+'*len(type)} ========================= "
    )
    logging.debug(json.dumps(content, sort_keys=True, indent=4))
    logging.debug(
        f" ========================= {'-'*len(type)} ========================= "
    )


def run_extractors(
    extractors_map, text_content, ai_extractors: list[BaseAIExtractor] = [], **kwargs
):
    """Run extraction calls (lookup, pattern, AI) and return a dict of all extracts.

    This function does NOT modify the bundler. Use `process_extracts` to
    feed the returned extracts into a bundler (or replay saved extracts).
    """
    assert ai_extractors or not extractors_map.get(
        "ai"
    ), "There should be at least one AI extractor in ai_extractors"

    text_content = "\n" + text_content + "\n"
    all_extracts = dict()
    if extractors_map.get("lookup"):
        try:
            lookup_extracts = lookups.extract_all(
                extractors_map["lookup"].values(), text_content
            )
            all_extracts["lookup"] = lookup_extracts
        except BaseException as e:
            logging.exception("lookup extraction failed", exc_info=True)

    if extractors_map.get("pattern"):
        try:
            logging.info("using pattern extractors")
            pattern_extracts = pattern.extract_all(
                extractors_map["pattern"].values(),
                text_content,
                ignore_extraction_boundary=kwargs.get(
                    "ignore_extraction_boundary", False
                ),
            )
            all_extracts["pattern"] = pattern_extracts
        except BaseException as e:
            logging.exception("pattern extraction failed", exc_info=True)

    if extractors_map.get("ai"):
        logging.info("using ai extractors")
        for extractor in ai_extractors:
            logging.info("running extractor: %s", extractor.extractor_name)
            try:
                ai_extracts = extractor.extract_objects(
                    text_content, extractors_map["ai"].values()
                )
                all_extracts[f"ai-{extractor.extractor_name}"] = ai_extracts
            except BaseException as e:
                logging.exception(
                    "AI extraction failed for %s",
                    extractor.extractor_name,
                    exc_info=True,
                )

    for i, ex in enumerate(itertools.chain(*all_extracts.values())):
        ex["id"] = "ex-" + str(i)
    return all_extracts


def process_extracts(bundler: txt2stixBundler, all_extracts: dict):
    """Process a previously-created `all_extracts` dict into the given bundler.

    This allows replaying saved extracts without invoking extractors again.
    """
    for key, extracts in (all_extracts or {}).items():
        try:
            bundler.process_observables(extracts)
        except BaseException:
            logging.exception("processing extracts failed for %s", key, exc_info=True)

    log_notes(all_extracts, "Extractions")


def extract_relationships(
    text_content, all_extracts, ai_extractor_session: BaseAIExtractor
):
    relationships = None
    try:
        # flatten extracts into a single list
        flattened = list(itertools.chain(*all_extracts.values()))
        rel = ai_extractor_session.extract_relationships(
            text_content, flattened, RELATIONSHIP_TYPES
        )
        relationships = rel.model_dump()
        log_notes(relationships, "Relationships")
    except BaseException as e:
        logging.exception("Relationship extraction failed: %s", e)
    return relationships


def validate_token_count(max_tokens, input, extractors: list[BaseAIExtractor]):
    logging.info("INPUT_TOKEN_LIMIT = %d", max_tokens)
    for extractor in extractors:
        token_count = _count_token(extractor, input)
        logging.info(
            f"{extractor.extractor_name}: input_file token count = {token_count}"
        )
        if token_count > max_tokens:
            raise FatalException(
                f"{extractor.extractor_name}: input_file token count ({token_count}) exceeds INPUT_TOKEN_LIMIT ({max_tokens})"
            )


@functools.lru_cache
def _count_token(extractor: BaseAIExtractor, input: str):
    return extractor.count_tokens(input)


def run_txt2stix(
    bundler: txt2stixBundler,
    preprocessed_text: str,
    extractors_map: dict,
    ai_content_check_provider=None,
    ai_create_attack_flow=None,
    ai_create_attack_navigator_layer=None,
    input_token_limit=10,
    ai_settings_extractions=None,
    ai_settings_relationships=None,
    relationship_mode="standard",
    ignore_extraction_boundary=False,
    ai_extract_if_no_incidence=True,  # continue even if ai_content_check fails
    txt2stix_data: Txt2StixData = None,
    **kwargs,
) -> Txt2StixData:
    # First, perform extraction-phase (LLM and extractor calls). This does not
    # modify the provided bundler so the results can be saved and replayed.
    # skip extraction phase if txt2stix_data is passed
    if not txt2stix_data:
        logging.info("=== Extraction Phase ===")
        txt2stix_data = extraction_phase(
            preprocessed_text,
            extractors_map,
            ai_content_check_provider=ai_content_check_provider,
            input_token_limit=input_token_limit,
            ai_settings_extractions=ai_settings_extractions,
            ai_settings_relationships=ai_settings_relationships,
            relationship_mode=relationship_mode,
            ignore_extraction_boundary=ignore_extraction_boundary,
            ai_extract_if_no_incidence=ai_extract_if_no_incidence,
        )
    else:
        logging.info("=== Skipping Extraction Phase (replaying saved data) ===")

    # Then, process the extracted data into the bundler (no LLM calls).
    processing_phase(
        bundler,
        preprocessed_text,
        txt2stix_data,
        ai_create_attack_flow=ai_create_attack_flow,
        ai_create_attack_navigator_layer=ai_create_attack_navigator_layer,
        ai_settings_relationships=ai_settings_relationships,
        ai_content_check_provider=ai_content_check_provider,
    )
    return txt2stix_data


def extraction_phase(
    preprocessed_text: str,
    extractors_map: dict,
    ai_content_check_provider=None,
    input_token_limit=10,
    ai_settings_extractions=None,
    ai_settings_relationships=None,
    relationship_mode="standard",
    ignore_extraction_boundary=False,
    ai_extract_if_no_incidence=True,
    **kwargs,
) -> Txt2StixData:
    """Perform token validation and run extractors/AI models. Does NOT modify a bundler."""
    should_extract = True
    txt2stix_data = Txt2StixData.model_construct()
    txt2stix_data.extractions = txt2stix_data.attack_flow = (
        txt2stix_data.relationships
    ) = None

    if ai_content_check_provider:
        logging.info("checking content")
        model: BaseAIExtractor = ai_content_check_provider
        validate_token_count(input_token_limit, preprocessed_text, [model])
        txt2stix_data.content_check = model.check_content(preprocessed_text)
        should_extract = txt2stix_data.content_check.describes_incident
        logging.info("=== ai-check-content output ====")
        logging.info(txt2stix_data.content_check.model_dump_json())

    if should_extract or ai_extract_if_no_incidence:
        if extractors_map.get("ai"):
            validate_token_count(
                input_token_limit, preprocessed_text, ai_settings_extractions
            )
        if relationship_mode == "ai":
            validate_token_count(
                input_token_limit, preprocessed_text, [ai_settings_relationships]
            )

        txt2stix_data.extractions = run_extractors(
            extractors_map,
            preprocessed_text,
            ai_extractors=ai_settings_extractions,
            ignore_extraction_boundary=ignore_extraction_boundary,
        )

        if (
            relationship_mode == "ai"
            and txt2stix_data.extractions
            and sum(map(lambda x: len(x), txt2stix_data.extractions.values()))
        ):
            txt2stix_data.relationships = extract_relationships(
                preprocessed_text, txt2stix_data.extractions, ai_settings_relationships
            )
    return txt2stix_data


def processing_phase(
    bundler: txt2stixBundler,
    preprocessed_text: str,
    data: Txt2StixData,
    ai_create_attack_flow=False,
    ai_create_attack_navigator_layer=False,
    ai_settings_relationships=None,
    ai_content_check_provider=None,
):
    """Process extracted `data` into the given `bundler` without invoking LLMs."""
    for d in itertools.chain([], *data.extractions.values()):
        d.pop("error", None)
    try:
        if data.content_check:
            cc = data.content_check
            provider_name = str(ai_content_check_provider)
            bundler.report.external_references.append(
                dict(
                    source_name="txt2stix_describes_incident",
                    description=str(cc.describes_incident).lower(),
                    external_id=provider_name,
                )
            )
            for classification in cc.incident_classification:
                bundler.report.labels.append(f"classification.{classification}".lower())
            bundler.add_summary(cc.summary, provider_name)
    except BaseException:
        logging.exception("applying content_check to bundler failed", exc_info=True)

    # process extracts into bundler
    process_extracts(bundler, data.extractions)

    # process relationships into bundler
    try:
        if data.relationships:
            bundler.process_relationships(data.relationships.get("relationships", []))
    except BaseException:
        logging.exception("processing relationships failed", exc_info=True)

    # generate attack flow / navigator layer now that bundler has been populated
    try:
        if ai_create_attack_flow or ai_create_attack_navigator_layer:
            data.attack_flow, data.navigator_layer = (
                attack_flow.extract_attack_flow_and_navigator(
                    bundler,
                    preprocessed_text,
                    ai_create_attack_flow,
                    ai_create_attack_navigator_layer,
                    ai_settings_relationships,
                    flow=data.attack_flow,
                )
            )
    except BaseException:
        logging.exception("attack flow / navigator generation failed", exc_info=True)


def main():
    dotenv.load_dotenv()
    logger = newLogger("txt2stix")
    try:
        args = parse_args()
        job_id = args.report_id or str(uuid.uuid4())
        setLogFile(logger, Path(f"logs/logs-{job_id}.log"))
        logger.info(f"Arguments: {json.dumps(sys.argv[1:])}")

        input_text = args.input_file.read_text()
        preprocessed_text = remove_links(
            input_text, args.ignore_image_refs, args.ignore_link_refs
        )
        load_env()

        bundler = txt2stixBundler(
            args.name,
            args.use_identity,
            args.tlp_level,
            input_text,
            args.confidence,
            args.all_extractors,
            args.labels,
            created=args.created,
            report_id=args.report_id,
            external_references=args.external_refs,
        )
        log_notes(sys.argv, "Config")

        data = run_txt2stix(
            bundler,
            preprocessed_text,
            args.use_extractions,
            input_token_limit=int(os.environ["INPUT_TOKEN_LIMIT"]),
            **args.__dict__,
        )

        ## write outputs
        out = bundler.to_json()
        output_dir = Path("./output") / str(bundler.uuid)
        with contextlib.suppress(BaseException):
            shutil.rmtree(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        output_path = output_dir / f"{bundler.bundle.id}.json"
        output_path.write_text(out)
        logger.info(f"Wrote bundle output to `{output_path}`")
        data_path = output_dir / f"data--{bundler.uuid}.json"
        data_path.write_text(data.model_dump_json(indent=4))
        logger.info(f"Wrote data output to `{data_path}`")
        for nav_layer in data.navigator_layer or []:
            nav_path = (
                output_dir / f"navigator-{nav_layer['domain']}----{bundler.uuid}.json"
            )
            nav_path.write_text(json.dumps(nav_layer, indent=4))
            logger.info(f"Wrote navigator output to `{nav_path}`")
    except argparse.ArgumentError as e:
        logger.exception(e, exc_info=True)
    except:
        raise
