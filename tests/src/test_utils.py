import pytest
from unittest.mock import patch, MagicMock
from txt2stix.utils import remove_links, read_included_file, validate_tld, validate_reg_key, validate_file_mimetype, Txt2StixData
import tldextract


# Mock Data for testing
mock_text = """
[Link Text](https://example.com)
![Image](https://example.com/image.png)
Some text content.
"""

def test_remove_links_images_only():
    result = remove_links(mock_text, remove_images=True, remove_anchors=False)
    assert "(https://example.com)" in result
    assert "https://example.com/image.png" not in result
    assert "Some text content" in result


def test_remove_links_anchors_only():
    result = remove_links(mock_text, remove_images=False, remove_anchors=True)
    assert "(https://example.com)" not in result
    assert "https://example.com/image.png" in result
    assert "Some text content" in result


def test_remove_links_anchors_and_images():
    result = remove_links(mock_text, remove_images=True, remove_anchors=True)
    assert "https://example.com" not in result
    assert "https://example.com/image.png" not in result
    assert "Some text content" in result



@pytest.mark.parametrize("domain, expected", [
    ("example.com", True),
    ("example.co.uk", True),
    ("example.xyz", True),
    ("invalid_domain", False),
    ("invalid_domain.dd", False),
    ("invalid_domain.txt", False),
    ("UPPER_CASE.NET", True),
])
def test_validate_tld(domain, expected):
    result = validate_tld(domain)
    assert result == expected


@pytest.mark.parametrize("reg_key, expected", [
    ("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft", True),
    ("HKCU\\Software\\Windows", True),
    ("INVALID_KEY\\SOME\\PATH", False)
])
def test_validate_reg_key(reg_key, expected):
    result = validate_reg_key(reg_key)
    assert result == expected


@pytest.mark.parametrize("file_name, expected", [
    ("file.csv", 'text/csv'),
    ("file.exe", 'application/x-msdownload'),
    ("file.txt", 'text/plain'),
    ("file.pdf", 'application/pdf'),
    ("file.pdfw", None),
    ("file.net", None),
])
def test_validate_file_mimetype(file_name, expected):
    result = validate_file_mimetype(file_name)
    assert result == expected
