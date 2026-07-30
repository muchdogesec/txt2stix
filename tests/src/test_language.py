import pytest

from txt2stix.language import detect_language

TEXTS = [
    ("en", "This is a report describing a malware campaign targeting financial institutions."),
    ("fr", "Ceci est un rapport décrivant une campagne de logiciels malveillants ciblant des institutions financières."),
    ("de", "Dies ist ein Bericht über eine Malware-Kampagne, die auf Finanzinstitute abzielt."),
    ("es", "Este es un informe que describe una campaña de malware dirigida a instituciones financieras."),
    ("ja", "これは金融機関を標的としたマルウェアキャンペーンを説明する報告書です。"),
]


@pytest.mark.parametrize(("expected_lang", "text"), TEXTS)
def test_detect_language(expected_lang, text):
    assert detect_language(text) == expected_lang


def test_detect_language_returns_string():
    assert isinstance(detect_language("Some plain English text."), str)
