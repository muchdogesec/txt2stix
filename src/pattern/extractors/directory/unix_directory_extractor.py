from ..base_extractor import BaseExtractor
from pathvalidate import is_valid_filepath


class UnixDirectoryExtractor(BaseExtractor):
    """
    A class for extracting valid Unix-style directory paths from text using a custom extraction function.

    Attributes:
        name (str): The name of the extractor, set to "unix-directory-path".
        extraction_function (function): The custom extraction function to validate and extract directory paths.
    """

    name = "pattern_directory_unix"
    extraction_function = lambda x: UnixDirectoryExtractor.is_valid_directory(x)

    @staticmethod
    def is_valid_directory(directory_path):
        """
        Custom extraction function to validate if the provided path is a valid Unix directory path.

        Args:
            directory_path (str): The path to be checked.

        Returns:
            bool: True if the path is a valid Unix directory path, False otherwise.
        """
        if "/" in directory_path and (directory_path[0] in ['.', '/', '~']):
            try:
                # Checking if it's a file path by splitting the path and checking the last component for a dot.
                file_name = directory_path.split('/')[-1]
                if "." in file_name:
                    return False
            except Exception as e:
                pass

            # Using pathvalidate library to check if the path is valid for Linux platform.
            check = is_valid_filepath(directory_path, platform="Linux")
            return check
        return False
