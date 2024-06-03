from ..base_extractor import BaseExtractor


class CryptoETHWalletExtractor(BaseExtractor):
    """
    A class for extracting Ethereum (ETH) wallet addresses from text using regular expressions.

    Attributes:
        name (str): The name of the extractor, set to "eth-wallet".
        extraction_regex (str): The regular expression pattern used for extracting eth-wallet addresses.
    """

    name = "pattern_cryptocurrency_eth_wallet"
    extraction_regex = r'0x[a-fA-F0-9]{40}'