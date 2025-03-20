import pytest
from unittest.mock import patch, MagicMock
from txt2stix.lookups import (
    load_lookup, find_all, merge_lookups, extract_all, 
    find_get_indexes, find_get_indexes_re
)
from txt2stix.extractions import Extractor


# Mock data for extractor terms and input string
mock_input_str = "This is a test string with terms like term1, [term2], and term3. \nHere's an extra (term3)"
mock_extractor = Extractor('ex1', dct=dict(file='mock_terms.txt', stix_mapping="mapping", slug="test_slug"))
mock_extractor.terms = None
def make_extractor(file, terms=None, name=None, **kwargs):
    if not name:
        name = file
    ex = Extractor(name, dict(file=file, **kwargs))
    ex.terms = terms
    return ex
    


# Test for load_lookup()
def test_load_lookup_with_terms():
    mock_extractor.terms = {'term1', 'term2'}
    
    result = load_lookup(mock_extractor)
    assert result == {'term1', 'term2'}
    assert mock_extractor.terms == {'term1', 'term2'}


def test_load_lookup_from_file():
    with patch('txt2stix.lookups.Path.read_text', return_value="term1\nterm2\nterm3") as mock_read:
        mock_extractor.terms = None
        result = load_lookup(mock_extractor)
        assert result == {'term1', 'term2', 'term3'}
        mock_read.assert_called_once()


# Test for find_all()
def test_find_all():
    mock_extractor.terms = {'term1', 'term2'}
    with patch('txt2stix.lookups.find_get_indexes_re', return_value=[5, 15]) as mock_find:
        result = find_all(mock_extractor, mock_input_str, start_id=0)
        assert len(result) == 2
        assert {extraction['value'] for extraction in result.values()} == {"term1", "term2"}
        assert result["extraction_0"]["start_index"] == [5, 15]


# Test for merge_lookups()
def test_merge_lookups():
    extractor1 = make_extractor(file="file1.txt", stix_mapping="mapping1", slug="slug1", terms={"term1", "term2"})
    extractor2 = make_extractor(file="file2.txt", stix_mapping="mapping2", slug="slug2", terms={"term3", "term4"})
    
    result = merge_lookups([extractor1, extractor2])
    assert {r for r in result} == {("term1", extractor1.stix_mapping, extractor1.slug), ("term2", extractor1.stix_mapping, extractor1.slug), ("term3", extractor2.stix_mapping, extractor2.slug), ("term4", extractor2.stix_mapping, extractor2.slug)}


# Test for extract_all()
def test_extract_all():
    extractor1 = make_extractor(file="file1.txt", stix_mapping="mapping1", slug="slug1", terms={"term1", "term2"})
    extractor2 = make_extractor(file="file2.txt", stix_mapping="mapping2", slug="slug2", terms={"term3", "term4"})
    extractors = [extractor1, extractor2]
    
    result = extract_all(extractors, mock_input_str)
    assert len(result) == 3
    assert {r['value'] for r in result} == {"term1", "term2", "term3"}
    assert {tuple(r['start_index']) for r in result} == {(38,), (58, 83,), (46,)}


def test_find_get_indexes():
    result = list(find_get_indexes("term1", mock_input_str))
    assert result == [38]  # term1 occurs at index 25


def test_find_get_indexes_re():
    assert list(find_get_indexes_re("term1", "term1  term1")) == [0, 7]
    assert list(find_get_indexes_re("term1", "term1-2  term1")) == [9]
    assert list(find_get_indexes_re("term1", "term1  term12")) == [0]


def test_empty_input_string():
    result = list(find_get_indexes("term1", ""))
    assert result == []
    
    result_re = list(find_get_indexes_re("term1", ""))
    assert result_re == []


# Test for handling multiple terms and duplicates
def test_multiple_terms_in_string():
    input_str = "term1 term2 term1 term2 term3 term4 term1"
    
    result = extract_all([mock_extractor], input_str)
    assert len(result) == 2, result  # term1 occurs 3 times, term2 twice
    assert {(r['value'], tuple(r['start_index'])) for r in result} == {("term1", (0, 12, 36)), ("term2", (18, 6))}


