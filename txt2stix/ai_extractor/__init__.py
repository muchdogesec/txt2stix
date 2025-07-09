import logging
import warnings

import dotenv

from .base import _ai_extractor_registry as ALL_AI_EXTRACTORS

from .base import BaseAIExtractor
class ModelError(Exception):
    pass

for path in ["openai", "anthropic", "gemini", "deepseek", "openrouter"]:
    try:
        __import__(__package__ + "." + path)
    except Exception as e:
        pass