from datetime import datetime
import pytest
from unittest import mock
from unittest.mock import MagicMock
from pathlib import Path
import sys
import os

from txt2stix import get_all_extractors
from txt2stix.ai_extractor.utils import DescribesIncident
from txt2stix.stix import txt2stixBundler
from txt2stix.txt2stix import (
    parse_args, parse_extractors_globbed, parse_model, run_txt2stix, split_comma, range_type, parse_labels, load_env,
    # run_txt2stix,
      extract_all, extract_relationships_with_ai
)
from txt2stix.common import FatalException
import argparse

from txt2stix.ai_extractor.utils import (
    AttackFlowItem,
    AttackFlowList,
    DescribesIncident,
)


mock_bundler = txt2stixBundler(
    name="test_indicator.py",
    identity=None,
    tlp_level="red",
    description="",
    confidence=None,
    extractors=None,
    labels=None,
    created=datetime(2020, 1, 1),
)
all_extractors = get_all_extractors()

TEST_AI_MODEL = os.getenv('TEST_AI_MODEL')


@mock.patch('txt2stix.txt2stix.validate_token_count')
def test_content_check_param(mock_validate_token_count, subtests):
    """Test the run_txt2stix function"""
    preprocessed_text = "192.168.0.1"
    mock_validate_token_count.return_value = True
    mock_extractors_map = parse_extractors_globbed("extractor", all_extractors, "pattern_ipv4_address_only,pattern_domain_name_only")
    incident_classifications = ["Class 1", "Class 2", "class 3"]

    with subtests.test('check_content', describes_incident=False), mock.patch('txt2stix.ai_extractor.base.BaseAIExtractor.check_content') as mock_check_content:
        mock_check_content.return_value = DescribesIncident(describes_incident=False, explanation="some bs", incident_classification=[])
        data = run_txt2stix(mock_bundler, preprocessed_text, mock_extractors_map, ai_content_check_provider=parse_model(TEST_AI_MODEL))
        assert data.content_check.describes_incident == False
        assert data.extractions == None, "extraction should not happen when check_content.describes_incident is False"
        assert 'txt2stix:describes_incident:false' in mock_bundler.report.labels
        mock_check_content.assert_called_once()
        mock_validate_token_count.assert_called_once()

    mock_validate_token_count.reset_mock()

    
    with subtests.test('check_content', describes_incident=True),  mock.patch('txt2stix.ai_extractor.base.BaseAIExtractor.check_content') as mock_check_content:
        mock_check_content.return_value = DescribesIncident(describes_incident=True, explanation="some bs", incident_classification=incident_classifications)
        data = run_txt2stix(mock_bundler, preprocessed_text, mock_extractors_map, ai_content_check_provider=parse_model(TEST_AI_MODEL))
        assert data.content_check.describes_incident == True
        assert data.extractions, "extraction should happen when check_content.describes_incident is False"
        mock_check_content.assert_called_once()
        mock_validate_token_count.assert_called_once()
        assert 'txt2stix:describes_incident:true' in mock_bundler.report.labels
        for classification in incident_classifications:
            assert f'txt2stix:{classification}'.lower() in mock_bundler.report.labels

    mock_validate_token_count.reset_mock()
    
    with subtests.test('no_check_content'),  mock.patch('txt2stix.ai_extractor.base.BaseAIExtractor.check_content') as mock_check_content:
        mock_check_content.return_value = DescribesIncident(describes_incident=True, explanation="some bs", incident_classification=["yes"])
        data = run_txt2stix(mock_bundler, preprocessed_text, mock_extractors_map)
        assert data.content_check == None, "content_check should be nil"
        assert data.extractions, "extraction should happen when check_content is disabled"
        mock_check_content.assert_not_called()
        mock_validate_token_count.assert_not_called()

@mock.patch('txt2stix.ai_extractor.base.BaseAIExtractor.extract_attack_flow')
def test_attack_flow(mock_extract_attack_flow, subtests):
    preprocessed_text = "192.168.0.1"
    mock_extract_attack_flow.return_value =  AttackFlowList(success=False, items=[], matrix='enterprise')
    mock_extractors_map = parse_extractors_globbed("extractor", all_extractors, "pattern_ipv4_address_only,pattern_domain_name_only")

    with subtests.test('without_ai_create_attack_flow'):
        retval = run_txt2stix(mock_bundler, preprocessed_text, mock_extractors_map, ai_settings_relationships=parse_model(TEST_AI_MODEL))
        mock_extract_attack_flow.assert_not_called()
        assert retval.attack_flow == None, "attack_flow should not run"

    with subtests.test('with_ai_create_attack_flow'):
        retval = run_txt2stix(mock_bundler, preprocessed_text, mock_extractors_map, ai_create_attack_flow=True, ai_settings_relationships=parse_model(TEST_AI_MODEL))
        mock_extract_attack_flow.assert_called_once()
        assert retval.attack_flow, "attack_flow should run"



@mock.patch('txt2stix.txt2stix.extract_relationships_with_ai')
def test_relationship_mode(mock_extract_relationships_with_ai, subtests):
    mock_extractors_map = parse_extractors_globbed("extractor", all_extractors, "pattern_ipv4_address_only,pattern_domain_name_only")
    preprocessed_text = "192.168.0.1"
    mock_extract_relationships_with_ai.return_value =  []

    with subtests.test('mode_standard'):
        retval = run_txt2stix(mock_bundler, preprocessed_text, mock_extractors_map, ai_settings_relationships=parse_model(TEST_AI_MODEL), relationship_mode='standard')
        mock_extract_relationships_with_ai.assert_not_called()
        assert retval.relationships == None, "extract_relationships_with_ai should not run"

    with subtests.test('mode_ai'):
        retval = run_txt2stix(mock_bundler, preprocessed_text, mock_extractors_map, ai_settings_relationships=parse_model(TEST_AI_MODEL), relationship_mode='ai')
        mock_extract_relationships_with_ai.assert_called_once()
        assert retval.relationships != None, "extract_relationships_with_ai should run"


