import logging

import dotenv

from .base import _ai_extractor_registry as ALL_AI_EXTRACTORS
dotenv.load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("txt2stix.ai_session")
logger.setLevel(logging.DEBUG)

from .base import BaseAIExtractor
from .openai import OpenAIExtractor
from .anthropic import AnthropicAIExtractor
from .gemini import GeminiAIExtractor