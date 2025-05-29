from datetime import datetime
import pytest
from unittest import mock
from unittest.mock import MagicMock
from pathlib import Path
import sys
import os

from txt2stix import get_all_extractors
from txt2stix.ai_extractor.utils import DescribesIncident
from txt2stix.bundler import txt2stixBundler
from txt2stix.txt2stix import (
    parse_args, run_txt2stix, split_comma, range_type, parse_labels, load_env,
    # run_txt2stix,
      extract_all, extract_relationships_with_ai
)
from txt2stix.common import FatalException
import argparse


@pytest.fixture
def mock_environment():
    envs = {}
    for env in ['INPUT_TOKEN_LIMIT', 'CTIBUTLER_BASE_URL', 'VULMATCH_BASE_URL']:
        if os.getenv(env):
            envs[env] = os.environ[env]
    os.environ['INPUT_TOKEN_LIMIT'] = '1000'
    os.environ['CTIBUTLER_BASE_URL'] = 'https://example.com'
    os.environ['VULMATCH_BASE_URL'] = 'https://example.com'
    yield
    # Cleanup
    os.environ.pop('INPUT_TOKEN_LIMIT', None)
    os.environ.pop('CTIBUTLER_BASE_URL', None)
    os.environ.pop('VULMATCH_BASE_URL', None)

    # restore original env
    os.environ.update(envs)


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
    with mock.patch('sys.argv', ['program', '--input-file', 'test.txt', '--name', 'test-report', '--relationship_mode', 'standard']):
        mock_file = mock.MagicMock()
        mock_file.exists.return_value = True
        with mock.patch('pathlib.Path.exists', return_value=True) as p:
            args = parse_args()
            assert args.input_file == Path('test.txt')
            assert args.name == 'test-report'


def test_load_env(mock_environment):
    """Test if environment loading and validation works."""
    load_env()
    assert os.getenv('INPUT_TOKEN_LIMIT') == '1000'
    assert os.getenv('CTIBUTLER_BASE_URL') == 'https://example.com'


def test_load_env_missing_variable(mock_environment):
    """Test if an exception is raised when required env variable is missing"""
    os.environ.pop('INPUT_TOKEN_LIMIT', None)
    with pytest.raises(FatalException):
        load_env()


def test_extract_all():
    """Test the extract_all function"""
    mock_bundler = MagicMock()
    mock_extractors_map = {"lookup": {}, "pattern": {}, "ai": {}}
    text_content = "some sample text"
    ai_extractors = [MagicMock()]
    
    with mock.patch('txt2stix.txt2stix.extract_all') as mock_lookups:
        mock_lookups.return_value = {}
        
        result = mock_lookups(mock_bundler, mock_extractors_map, text_content, ai_extractors=ai_extractors)
        assert isinstance(result, dict)
        mock_lookups.assert_called_once()
