from pathlib import PurePosixPath, PureWindowsPath
import pytest
from unittest import mock
from txt2stix import get_all_extractors
from txt2stix.indicator import (
    build_observables,
    find_hash_type,
    parse_path,
    split_ip_port,
    get_country_code,
    get_iban_details,
    BadDataException,
)
from stix2 import HashConstant

from txt2stix.bundler import txt2stixBundler
from datetime import datetime

def dummy_bundler():
    return txt2stixBundler(
        name="test_indicator.py",
        identity=None,
        tlp_level="red",
        description="",
        confidence=None,
        extractors=None,
        labels=None,
        created=datetime(2020, 1, 1),
    )
# all_extractors = get_all_extractors()