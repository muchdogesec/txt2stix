from .asn_extractor import ASNExtractor
from .cpe_extractor import CPEExtractor
from .cve_extractor import CVEExtractor
from .email_extractor import EmailAddressExtractor
from .filename_extractor import FileNameExtractor
from .iban_extractor import IBANExtractor
from .mac_address_extractor import MacAddressExtractor
from .phonenumber_extractor import PhoneNumberExtractor
from .user_agent_extractor import UserAgentBaseExtractor
from .windows_registry_key_extractor import WindowsRegistryKeyExtractor

OTHER_EXTRACTORS = [ASNExtractor,
                    CPEExtractor,
                    CVEExtractor,
                    EmailAddressExtractor,
                    FileNameExtractor,
                    IBANExtractor,
                    MacAddressExtractor,
                    PhoneNumberExtractor,
                    UserAgentBaseExtractor,
                    WindowsRegistryKeyExtractor
                    ]
