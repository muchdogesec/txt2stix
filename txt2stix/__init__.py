from txt2stix import extractions
from pathlib import Path

from .utils import get_include_path, set_include_path, INCLUDE_PATH

def get_all_extractors(include_path=None):
    return extractions.parse_extraction_config(include_path or get_include_path())


def __getattr__(name):
    if name == "INCLUDES_PATH":
        from . import utils
        return utils.INCLUDES_PATH
    # Metadata consumers should not import the extraction engine.
    if name == "txt2stixBundler":
        from .bundler import txt2stixBundler
        globals()[name] = txt2stixBundler
        return txt2stixBundler
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'txt2stixBundler', 'extract_all', 'get_include_path'
]
