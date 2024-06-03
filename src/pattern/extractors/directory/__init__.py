from .unix_directory_extractor import UnixDirectoryExtractor
from .unix_file_path_extractor import UnixFilePathExtractor
from .windows_directory_path_extractor import WindowDirectoryExtractor
from .windows_file_path_extractor import WindowsFilePathExtractor

DIRECTORY_EXTRACTORS = [UnixDirectoryExtractor,
                        UnixFilePathExtractor,
                        WindowDirectoryExtractor,
                        WindowsFilePathExtractor
                        ]
