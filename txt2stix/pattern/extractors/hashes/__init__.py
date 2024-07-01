from .md5_extractor import FileHashMD5Extractor
from .sha1_extractor import FileHashSHA1Extractor
from .sha2_256_exactor import FileHashSHA2_256Extractor
from .sha2_512_exactor import FileHashSHA2_512Extractor
from .sha3_256_exactor import FileHashSHA3_256Extractor
from .sha3_512_exactor import FileHashSHA3_512Extractor
from .sha224_extractor import FileHashSHA224Extractor

SHA_EXTRACTORS = [FileHashMD5Extractor,
                  FileHashSHA1Extractor,
                  FileHashSHA224Extractor,
                  FileHashSHA2_256Extractor,
                  FileHashSHA2_512Extractor,
                  FileHashSHA3_256Extractor,
                  FileHashSHA3_512Extractor
                  ]
