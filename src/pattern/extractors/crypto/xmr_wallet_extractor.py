from ..base_extractor import BaseExtractor


class CryptoXMRWalletExtractor(BaseExtractor):
    """
    A class for extracting Monero (XMR) wallet addresses from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "XMR Transaction".
        extraction_regex (str): The regular expression pattern used for extracting xmr-wallet addresses.
    """

    name = "pattern_cryptocurrency_xmr_wallet"
    extraction_regex = r"^[48][0-9A-HJ-NP-Za-km-z]{94}$"
