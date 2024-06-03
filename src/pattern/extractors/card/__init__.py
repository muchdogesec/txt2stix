from .amex_card_extractor import AmexCardExtractor
from .diners_card_extractor import DinersCardExtractor
from .discover_card_extractor import BankCardDiscoverExtractor
from .jcb_card_extractor import JCBCardExtractor
from .master_card_extractor import MastercardCardExtractor
from .union_card_extractor import UnionPayCardExtractor
from .visa_card_extractor import VisaCardBaseExtractor

CARD_EXTRACTORS = [AmexCardExtractor,
                   DinersCardExtractor,
                   BankCardDiscoverExtractor,
                   JCBCardExtractor,
                   MastercardCardExtractor,
                   UnionPayCardExtractor,
                   VisaCardBaseExtractor]
