from pathvalidate import is_valid_filepath

from ..base_extractor import BaseExtractor
from ..helper import validate_file_extension


class UnixFilePathExtractor(BaseExtractor):
    """
    A class for extracting valid Unix-style file paths from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "unix-file-directory".
        ignore_list (list): A list of strings to be ignored during extraction.
        extraction_function (function): The custom extraction function to validate and extract file paths.
    """

    name = "pattern_directory_unix_file"
    ignore_list = ["http://", "https://", "http[:]//", "http[://"]
    extraction_function = lambda x: UnixFilePathExtractor.is_valid_directory(x)

    @staticmethod
    def is_valid_directory(directory_path):
        """
        Custom extraction function to validate if the provided path is a valid Unix file path.

        Args:
            directory_path (str): The path to be checked.

        Returns:
            bool: True if the path is a valid Unix file path, False otherwise.
        """
        if "/" in directory_path and (directory_path[0] in ['.', '/', '~']) and "\\" not in directory_path:
            # Using pathvalidate library to check if the path is valid for Linux platform.
            check = is_valid_filepath(directory_path, platform="Linux")
            if check:
                try:
                    # Checking if it's a file path by splitting the path and checking the last component for a dot.
                    file_name = directory_path.split('/')[-1]
                    extension = file_name.split('.')[-1]
                    if validate_file_extension(extension):
                        return True
                except Exception as e:
                    return False
        return False
