import argparse
import os
import random
from urllib.parse import urljoin
import requests
from stix2extensions.tools import creditcard2stix
from txt2stix.retriever import STIXObjectRetriever


def check_binlist():
    card = str(random.randrange(432101, 456789))
    api_key = os.getenv("BIN_LIST_API_KEY", "")
    return "authorized" if creditcard2stix.get_bin_data(card, api_key) else "unauthorized"


def check_llms():
    from txt2stix.txt2stix import parse_model

    auth_info = dict()
    for model_name in ["openai", "deepseek", "gemini", "openrouter", "anthropic"]:
        try:
            model = parse_model(model_name)
            auth_info[model_name] = model.check_credential()
        except argparse.ArgumentTypeError:
            auth_info[model_name] = "unsupported"
        except:
            auth_info[model_name] = "unauthorized"
    return auth_info


def check_ctibutler_vulmatch(service):
    retriever = STIXObjectRetriever(service)
    path = dict(
        ctibutler="v1/location/versions/available/",
        vulmatch="v1/cve/objects/vulnerability--f552f6f4-39da-48dc-8717-323772c99588/",
    )[service]
    try:
        resp = retriever.session.get(urljoin(retriever.api_root, path))
        match resp.status_code:
            case 401 | 403:
                return "unauthorized"
            case 200:
                return "authorized"
            case _:
                return "unknown"
    except:
        return "offline"

def check_btcscan():
    url = "https://btcscan.org/api/blocks/tip/height"
    try:
        resp = requests.get(url)
        match resp.status_code:
            case 401 | 403:
                return "unauthorized"
            case 200:
                return "authorized"
            case _:
                return "unknown"
    except:
        return "offline"

def check_statuses(test_llms=False):
    statuses = dict(
        ctibutler=check_ctibutler_vulmatch("ctibutler"),
        vulmatch=check_ctibutler_vulmatch("vulmatch"),
        binlist=check_binlist(),
        btcscan=check_btcscan(),
    )
    if test_llms:
        statuses.update(llms=check_llms())
    return statuses


def format_statuses(status_dict):
    def get_marker(status):
        """Return a checkmark, cross, or dash based on status."""
        match status.lower():
            case "authorized":
                return "✔"
            case "unauthorized":
                return "✖"
            case "unknown" | "offline" | "unsupported":
                return "–"
            case _:
                return "?"

    print("============= Service Statuses ===============")
    for key, value in status_dict.items():
        if key == "llms" and isinstance(value, dict):
            print(f"\n  {key.upper()}:")
            for llm_name, llm_status in value.items():
                marker = get_marker(llm_status)
                print(f"    {llm_name:<12}: {llm_status:<15} {marker}")
        else:
            marker = get_marker(value)
            print(f"  {key:<12}: {value:<15} {marker}")
