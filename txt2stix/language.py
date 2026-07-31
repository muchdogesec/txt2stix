import py3langid


def detect_language(text: str) -> str:
    """Detect the ISO 639-1 language code of `text` using py3langid."""
    lang, _ = py3langid.classify(text)
    return lang
