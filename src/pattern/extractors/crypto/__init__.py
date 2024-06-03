from .btc_wallet_extractor import CryptoBTCWalletExtractor
from .eth_wallet_extractor import CryptoETHWalletExtractor
from .xmr_wallet_extractor import CryptoXMRWalletExtractor

CRYPTO_EXTRACTORS = [CryptoBTCWalletExtractor,
                     CryptoETHWalletExtractor,
                     CryptoXMRWalletExtractor]
