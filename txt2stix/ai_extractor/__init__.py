import logging

import dotenv

from .base import _ai_extractor_registry as ALL_AI_EXTRACTORS

from .base import BaseAIExtractor
from .openai import OpenAIExtractor
from .anthropic import AnthropicAIExtractor
from .gemini import GeminiAIExtractor