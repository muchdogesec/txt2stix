from ..base_extractor import BaseExtractor


class CryptoBTCWalletExtractor(BaseExtractor):
    """
    A class for extracting Bitcoin (BTC) wallet addresses from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "btc-wallet".
        extraction_regex (str): The regular expression pattern used for extracting BTC wallet addresses.
    """

    name = "pattern_cryptocurrency_btc_wallet"
    extraction_regex = "^(bc1|[13])[a-km-zA-HJ-NP-Z1-9]{25,34}$"
