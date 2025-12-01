from txt2stix import extractions
from .bundler import txt2stixBundler
from pathlib import Path

INCLUDES_PATH = None
def get_include_path():
    global INCLUDES_PATH
    
    if INCLUDES_PATH:
        return INCLUDES_PATH
    
    from pathlib import Path
    MODULE_PATH = Path(__file__).parent.parent
    INCLUDES_PATH = MODULE_PATH/"includes"
    try:
        from . import includes
        INCLUDES_PATH = Path(includes.__file__).parent
    except:
        pass
    return INCLUDES_PATH

def set_include_path(path):
    global INCLUDES_PATH
    INCLUDES_PATH = path

def get_all_extractors(include_path=None):
    return extractions.parse_extraction_config(include_path or get_include_path())


__all__ = [
    'txt2stixBundler', 'extract_all', 'get_include_path'
]