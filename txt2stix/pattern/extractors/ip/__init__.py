from .ipv4_extractor import IPv4Extractor
from .ipv4_port_extractor import IPv4WithPortExtractor
from .ipv4_cidr_extractor import IPv4WithCIDRExtractor
from .ipv6_extractor import IPv6Extractor
from .ipv6_port_extractor import IPv6WithPortExtractor
from .ipv6_cidr_extractor import IPv6WithCIDRExtractor

IP_EXTRACTORS = [IPv4Extractor,
                 IPv4WithPortExtractor,
                 IPv4WithCIDRExtractor,
                 IPv6Extractor,
                 IPv6WithPortExtractor,
                 IPv6WithCIDRExtractor,
                 ]
