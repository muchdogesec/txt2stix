from ..base_extractor import BaseExtractor


class UserAgentBaseExtractor(BaseExtractor):
    """
    A class for extracting user agent strings from text using a regular expression.

    Attributes:
        name (str): The name of the extractor, set to "user_agent".
        platforms (str): The regex pattern to match the user agent platform name.
        user_agent_details (str): The regex pattern to match additional user agent details within parentheses.
        user_agent (str): The regex pattern to match the entire user agent string.
        extraction_regex (str): The regular expression pattern used for extracting user agent strings from the text.
    """

    name = "pattern_user_agent"
    platforms = r"([a-zA-Z]+)"
    user_agent_details = r"\([\w;\s\,.:-]+\)"
    user_agent = rf"((User-Agent: )|(user-agent: ))?Mozilla/5.0([ ](({user_agent_details})|(({platforms}/)[^\s\"\',]+)))+"
    extraction_regex = r"Mozilla\/\d+\.\d+(\s+\([^\)]+\))?"
