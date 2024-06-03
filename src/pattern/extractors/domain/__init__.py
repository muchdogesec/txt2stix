from .domain_extractor import DomainNameExtractor
from .sub_domain_extractor import SubDomainExtractor
from .hostname_extractor import HostnameBaseExtractor

DOMAIN_EXTRACTORS = [DomainNameExtractor,
                     SubDomainExtractor,
                     HostnameBaseExtractor
                     ]
