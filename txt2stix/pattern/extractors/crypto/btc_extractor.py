from validators import base58
from ..base_extractor import BaseExtractor
from base58 import b58decode


class CryptoBTCWalletExtractor(BaseExtractor):
    """
    A class for extracting Bitcoin (BTC) wallet addresses from text using regular expressions.

    """

    name = "pattern_cryptocurrency_btc_wallet"
    extraction_regex = "^(bc1|[13])[a-km-zA-HJ-NP-Z1-9]{25,34}$"

    @classmethod
    def filter_function(cls, value):
        try:
            b58decode(value).hex()
            return True
        except:
            return False

class CryptoBTCWalletTransactionExtractor(CryptoBTCWalletExtractor):
    """
    A class for extracting Bitcoin (BTC) wallet addresses along with the transactions on that account.
    
    """
    name = "pattern_cryptocurrency_btc_wallet_transaction"

class CryptoBTCTransactionExtractor(BaseExtractor):
    """
    A class for extracting Bitcoin (BTC) transaction hash from text using regular expressions.

    """

    name = "pattern_cryptocurrency_btc_transaction"
    extraction_regex = "^[a-fA-F0-9]{64}$"

