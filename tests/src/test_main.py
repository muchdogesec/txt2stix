from datetime import datetime
import tempfile
from types import SimpleNamespace
import uuid
import pytest
from unittest import mock
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import os

from txt2stix.utils import RELATIONSHIP_TYPES, remove_links
from . import utils

from txt2stix import get_all_extractors
from txt2stix.ai_extractor.openai import OpenAIExtractor
from txt2stix.ai_extractor.utils import DescribesIncident
from txt2stix.bundler import txt2stixBundler
from txt2stix.txt2stix import (
    main,
    newLogger,
    parse_args,
    parse_bool,
    parse_extractors_globbed,
    parse_model,
    parse_ref,
    run_txt2stix,
    setLogFile,
    split_comma,
    range_type,
    parse_labels,
    load_env,
    # run_txt2stix,
    extract_all,
    extract_relationships_with_ai,
)
from txt2stix.common import FatalException
import argparse


@pytest.fixture
def mock_environment():
    envs = {}
    for env in ["INPUT_TOKEN_LIMIT", "CTIBUTLER_BASE_URL", "VULMATCH_BASE_URL"]:
        if os.getenv(env):
            envs[env] = os.environ[env]
    os.environ["INPUT_TOKEN_LIMIT"] = "1000"
    os.environ["CTIBUTLER_BASE_URL"] = "https://example.com"
    os.environ["VULMATCH_BASE_URL"] = "https://example.com"
    yield
    # Cleanup
    os.environ.pop("INPUT_TOKEN_LIMIT", None)
    os.environ.pop("CTIBUTLER_BASE_URL", None)
    os.environ.pop("VULMATCH_BASE_URL", None)

    # restore original env
    os.environ.update(envs)


def test_parse_ref():
    assert parse_ref("ref1=ref2d") == dict(source_name="ref1", external_id="ref2d")
    with pytest.raises(argparse.ArgumentTypeError):
        parse_ref("invalid ref")


def test_parse_model():
    assert isinstance(parse_model("openai"), OpenAIExtractor)
    with pytest.raises(argparse.ArgumentTypeError):
        parse_model("invalid:model")


def test_split_comma():
    assert split_comma("a,b,c") == ["a", "b", "c"]
    assert split_comma("a") == ["a"]
    assert split_comma("") == []


def test_range_type():
    range_fn = range_type(10, 20)
    assert range_fn("15") == 15
    with pytest.raises(argparse.ArgumentTypeError):
        range_fn("5")
    with pytest.raises(argparse.ArgumentTypeError):
        range_fn("25")


def test_parse_labels():
    assert parse_labels("label1,label2") == ["label1", "label2"]
    with pytest.raises(argparse.ArgumentTypeError):
        parse_labels("label1,label-2")


def test_parse_args():
    with mock.patch(
        "sys.argv",
        [
            "program",
            "--input-file",
            "test.txt",
            "--name",
            "test-report",
            "--relationship_mode",
            "standard",
        ],
    ):
        mock_file = mock.MagicMock()
        mock_file.exists.return_value = True
        with mock.patch("pathlib.Path.exists", return_value=True) as p:
            args = parse_args()
            assert args.input_file == Path("test.txt")
            assert args.name == "test-report"

def test_parse_args_fails(monkeypatch):
    tmp = tempfile.NamedTemporaryFile(prefix='test_parse_args_fails')
    monkeypatch.setattr(sys, 'argv', [
        "program",
        "--input-file",
        tmp.name,
        "--name",
        "a"*125,
        "--relationship_mode",
        "standard",
    ])
    with pytest.raises(argparse.ArgumentError, match='max 124 characters'):
        parse_args()

    monkeypatch.setattr(sys, 'argv', [
        "program",
        "--input-file",
        tmp.name,
        "--name",
        "a",
        "--relationship_mode",
        "ai",
    ])
    with pytest.raises(argparse.ArgumentError, match="relationship_mode is set to AI, --ai_settings_relationships is required"):
        parse_args()

    monkeypatch.setattr(sys, 'argv', [
        "program",
        "--input-file",
        tmp.name,
        "--name",
        "a",
        "--relationship_mode",
        "standard",
        "--ai_create_attack_flow",
    ])
    with pytest.raises(argparse.ArgumentError, match="argument --ai_create_attack_flow: --ai_settings_relationships must be set"):
        parse_args()


    monkeypatch.setattr(sys, 'argv', [
        "program",
        "--input-file",
        tmp.name,
        "--name",
        "a",
        "--relationship_mode",
        "standard",
        "--ai_create_attack_navigator_layer",
    ])
    with pytest.raises(argparse.ArgumentError, match="argument --ai_create_attack_navigator_layer: --ai_settings_relationships must be set"):
        parse_args()

    monkeypatch.setattr(sys, 'argv', [
        "program",
        "--input-file",
        tmp.name,
        "--name",
        "a",
        "--relationship_mode",
        "standard",
        "--use_extractions", "ai_ipv4_address_only",
    ])
    with pytest.raises(argparse.ArgumentError, match="ai based extractors are passed, --ai_settings_extractions is required"):
        parse_args()

def test_load_env(mock_environment):
    """Test if environment loading and validation works."""
    load_env()
    assert os.getenv("INPUT_TOKEN_LIMIT") == "1000"
    assert os.getenv("CTIBUTLER_BASE_URL") == "https://example.com"


def test_load_env_missing_variable(mock_environment):
    """Test if an exception is raised when required env variable is missing"""
    os.environ.pop("INPUT_TOKEN_LIMIT", None)
    with pytest.raises(FatalException):
        load_env()


def test_parse_extractors_globbed():
    abcd_pattern = SimpleNamespace(type="pattern")
    abcd_lookup = SimpleNamespace(type="lookup")
    efgh_lookup = SimpleNamespace(type="lookup")
    all_extractors = {
        "abcd_pattern": abcd_pattern,
        "abcd_lookup": abcd_lookup,
        "efgh_lookup": efgh_lookup,
        "null_extractor": None,
    }
    with (
        patch("txt2stix.pattern.load_extractor"),
        patch("txt2stix.lookups.load_lookup"),
    ):
        assert parse_extractors_globbed(
            "extractor", all_extractors, "abcd_pattern"
        ) == {'pattern': {'abcd_pattern': abcd_pattern}}

        assert parse_extractors_globbed(
            "extractor", all_extractors, "abcd_*"
        ) == {'pattern': {'abcd_pattern': abcd_pattern}, 'lookup': {'abcd_lookup': abcd_lookup}}

    with pytest.raises(argparse.ArgumentTypeError, match='`bad_pattern` has 0 matches'):
        parse_extractors_globbed(
            "extractor", all_extractors, "bad_pattern"
        )

    
    with pytest.raises(argparse.ArgumentTypeError, match="extractor `null_extractor`: 'NoneType' object has no attribute 'type'"):
        parse_extractors_globbed(
            "extractor", all_extractors, "null*"
        )

@pytest.mark.parametrize(
    ['string', 'expected'],
    [
        ('yes', True),
        ('YeS', True),
        ('y', True),
        ('Y', True),
        ('1', True),
        ('0', False),
        ('n', False),
        ('no', False),
        ('NO', False),
    ]
)
def test_parse_bool(string, expected):
    assert parse_bool(string) == expected

def test_extract_all():
    """Test the extract_all function"""
    mock_bundler = MagicMock()
    mock_extractors_map = {"lookup": {}, "pattern": {}, "ai": {}}
    text_content = "some sample text"
    ai_extractors = [MagicMock()]

    with mock.patch("txt2stix.txt2stix.extract_all") as mock_lookups:
        mock_lookups.return_value = {}

        result = mock_lookups(
            mock_bundler, mock_extractors_map, text_content, ai_extractors=ai_extractors
        )
        assert isinstance(result, dict)
        mock_lookups.assert_called_once()


def test_main_func():
    input_text = "fake input text"
    processed_text = "processed input text"
    with (
        mock.patch("txt2stix.txt2stix.parse_args") as mock_parse_args,
        mock.patch("txt2stix.txt2stix.setLogFile") as mock_set_log_file,
        mock.patch(
            "txt2stix.txt2stix.remove_links",
            wraps=remove_links,
            return_value=processed_text,
        ) as mock_remove_links,
        mock.patch("txt2stix.txt2stix.load_env") as mock_load_env_fn,
        mock.patch("txt2stix.txt2stix.txt2stixBundler") as mock_bundler_cls,
        mock.patch("txt2stix.txt2stix.run_txt2stix") as mock_run_txt2stix,
        mock.patch("txt2stix.txt2stix.Path.write_text") as mock_write_text,
    ):
        mock_parse_args.return_value.input_file.read_text.return_value = input_text
        main()

        mock_set_log_file.assert_called_once()
        mock_parse_args.assert_called_once()
        mock_run_txt2stix.assert_called_once_with(
            mock_bundler_cls.return_value,
            processed_text,
            mock_parse_args.return_value.use_extractions,
            input_token_limit=int(os.environ["INPUT_TOKEN_LIMIT"]),
            **mock_parse_args.return_value.__dict__,
        )
        mock_bundler_cls.return_value.to_json.assert_called()
        mock_write_text.assert_called()


def test_setLogFile():
    tmp = tempfile.NamedTemporaryFile(prefix='setlogfile')
    p = Path(tmp.name)
    logger = newLogger("txt2stix")
    setLogFile(logger, p)
    assert p.exists(), "log file should be created"

def named_ai_extractor_mock(name, retval):
    m = MagicMock()
    m.extractor_name = name
    m.extract_objects.return_value = retval
    return m

def test_extract_all():
    bundler = MagicMock()
    with( 
        patch('txt2stix.lookups.extract_all') as mock_lookup__extract_all,
        patch('txt2stix.pattern.extract_all') as mock_pattern__extract_all,
    ):
        mock_lookup__extract_all.return_value = ['lookup1', 'lookup2']
        mock_pattern__extract_all.return_value = ['pattern1', 'pattern2']

        ## test pattern and lookup
        all_extracts = extract_all(bundler, dict(lookup=dict(a=1), pattern=dict(b=2)), '')
        bundler.process_observables.assert_called()
        bundler.process_observables.assert_any_call(['lookup1', 'lookup2'])
        bundler.process_observables.assert_any_call(['pattern1', 'pattern2'])
        assert all_extracts == dict(lookup=['lookup1', 'lookup2'], pattern=['pattern1', 'pattern2'])

        # test pattern and ai
        ai_extractors = [
            named_ai_extractor_mock('ex1', ['ai0']),
            named_ai_extractor_mock('ai2', ['ai3', 'ai9']),
            MagicMock()
        ]
        ai_extractors[-1].extract_objects.side_effect = Exception
        all_extracts = extract_all(bundler, dict(lookup=dict(a=1), pattern=dict(b=2), ai=dict(c=1)), '', ai_extractors=ai_extractors)
        bundler.process_observables.assert_called()
        bundler.process_observables.assert_any_call(['lookup1', 'lookup2'])
        bundler.process_observables.assert_any_call(['pattern1', 'pattern2'])
        bundler.process_observables.assert_any_call(['ai0'])
        bundler.process_observables.assert_any_call(['ai3', 'ai9'])




def test_extract_relationships_with_ai():
    mock_bundler = MagicMock()
    text = "TEXT_CONTENT"
    all_extracts = {'lookup': [1, 2], 'ai': [3, 4]}
    mock_ai_session = MagicMock()
    mock_ai_session.extract_relationships.return_value.model_dump.return_value = {'relationships': [1, 2]}
    relationships = extract_relationships_with_ai(mock_bundler, text, all_extracts, mock_ai_session)
    mock_ai_session.extract_relationships.assert_called_once_with(text, [1, 2, 3, 4], RELATIONSHIP_TYPES)
    mock_ai_session.extract_relationships.return_value.model_dump.assert_called()
    assert relationships == mock_ai_session.extract_relationships.return_value.model_dump.return_value
    mock_bundler.process_relationships.assert_called_once_with([1, 2])

    mock_ai_session.extract_relationships.side_effect = Exception
    assert extract_relationships_with_ai(mock_bundler, text, all_extracts, mock_ai_session) == None


def test_check_credentials(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [
        "program",
        "--check_credentials"
    ])
    with pytest.raises(SystemExit):
        parse_args()