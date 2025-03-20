import re
from ..base_extractor import BaseExtractor


class WindowsRegistryKeyExtractor(BaseExtractor):
    """
    A class for extracting valid Windows Registry keys from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "windows_registry_key".
        valid_root_keys (str): The valid root keys of the Windows Registry.
        extraction_regex (str): The regular expression pattern used for extracting Windows Registry keys from the text.
    """

    name = "pattern_windows_registry_key"
    valid_root_keys = ['HKEY_CLASSES_ROOT', 'HKCR', 'HKEY_CURRENT_USER', 'HKCU', 'HKEY_LOCAL_MACHINE', 'HKLM', 'HKEY_USERS', 'HKU', 'HKEY_CURRENT_CONFIG', 'HKCC', 'HKEY_PERFORMANCE_DATA', 'HKEY_DYN_DATA']
    prefix_regex = r'(?:' + '|'.join(re.escape(item) for item in valid_root_keys) + r')'
    extraction_regex = rf'\b({prefix_regex}[\\\w]+)\b'
