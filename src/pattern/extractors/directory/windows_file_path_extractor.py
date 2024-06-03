from pathvalidate import is_valid_filepath
from ..base_extractor import BaseExtractor
from ..helper import validate_file_extension


class WindowsFilePathExtractor(BaseExtractor):
    """
    WindowsFilePathExtractor is a class that extracts file paths on the Windows platform and validates the file extension.

    Attributes:
        name (str): The name of the extractor.
        extraction_function (function): The function to extract file paths.
    """
    name = "pattern_directory_windows_with_file"
    extraction_function = lambda x: WindowsFilePathExtractor.is_valid_directory(x)

    @staticmethod
    def is_valid_directory(directory_path):
        """
        Custom extraction function to validate if the provided path is a valid Windows directory path.

        Args:
            directory_path (str): The path to be checked.

        Returns:
            bool: True if the path is a valid Windows directory path, False otherwise.
        """
        directory_path = directory_path.strip('"')
        drive_letters = ["{}:\\".format(letter) for letter in "CDEFGHIJKLMNO"] + ["{}:".format(letter) for letter in "CDEFGHIJKLMNO"] + ['..\\', '\\', '\\\\' ]
        flag = False
        for prefix in drive_letters:
            if directory_path.startswith(str(prefix)):
                flag = True
                break
        if flag:
            check = is_valid_filepath(directory_path, platform="Windows")
            if validate_file_extension(directory_path.split('.')[-1]) and check:
                return True
        return False

