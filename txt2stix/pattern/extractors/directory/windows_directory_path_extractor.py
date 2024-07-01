from pathvalidate import is_valid_filepath
from ..base_extractor import BaseExtractor
from ..helper import validate_file_extension


class WindowDirectoryExtractor(BaseExtractor):
    """
    A class for extracting valid Windows-style directory paths from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "widows-directory".
        ignore_list (list): A list of strings to be ignored during extraction.
        extraction_function (function): The custom extraction function to validate and extract directory paths.
    """

    name = "pattern_directory_windows"
    extraction_function = lambda x: WindowDirectoryExtractor.is_valid_directory(x)

    @staticmethod
    def is_valid_directory(directory_path):
        """
        Custom extraction function to validate if the provided path is a valid Windows directory path.

        Args:
            directory_path (str): The path to be checked.

        Returns:
            bool: True if the path is a valid Windows directory path, False otherwise.
        """
        if directory_path == '\\' or directory_path == '\\\\':
            return False

        directory_path = directory_path.strip('"')
        drive_letters = ["{}:\\".format(letter) for letter in "CDEFGHIJKLMNO"] + ["{}:".format(letter) for letter in "CDEFGHIJKLMNO"] + ['..\\', '\\', '\\\\']
        flag = False
        for prefix in drive_letters:
            if directory_path.startswith(str(prefix)):
                flag = True
                break
        if flag:
            check = is_valid_filepath(directory_path, platform="Windows")
            if not validate_file_extension(directory_path.split('.')[-1]) and check:
                return check
        return False
