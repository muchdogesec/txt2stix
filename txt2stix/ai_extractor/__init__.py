import logging

import dotenv

from .base import _ai_extractor_registry as ALL_AI_EXTRACTORS

from .base import BaseAIExtractor
class ModelError(Exception):
    pass

for path in ["openai", "anthropic", "gemini", "deepseek", "openrouter"]:
    try:
        __import__(__package__ + "." + path)
    except Exception as e:
        logging.warning("%s not supported, please install missing modules", path, exc_info=True)