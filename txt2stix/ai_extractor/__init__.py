from collections.abc import Mapping
from importlib import import_module
import typing

if typing.TYPE_CHECKING:
    from txt2stix.ai_extractor.base import BaseAIExtractor

class ModelError(Exception):
    pass

class UnknownAIProviderError(ModelError):
    def __init__(self, provider, available_providers):
        super().__init__(f"Unknown AI provider: {provider!r}. Available providers: {list(available_providers)}")
        self.provider = provider
        self.available_providers = available_providers

class AIProviderLoadError(ModelError):
    def __init__(self, provider, original_exception):
        super().__init__(f"Failed to load AI provider module: {provider!r}")
        self.provider = provider
        self.original_exception = original_exception

class AIProviderInitializationError(ModelError):
    def __init__(self, provider, original_exception):
        super().__init__(f"Failed to initialize AI provider: {provider!r}")
        self.provider = provider
        self.original_exception = original_exception


class LazyExtractorRegistry(Mapping):
    _PROVIDER_MODULES = ["openai", "anthropic", "gemini", "deepseek", "openrouter"]
    def __init__(self):
        self._providers = {provider: "." + provider for provider in self._PROVIDER_MODULES}
        self._loaded = {}

    def __getitem__(self, provider) -> 'BaseAIExtractor':
        from .base import _ai_extractor_registry
        if provider not in self._loaded:
            try:
                module_path = self._providers[provider]
            except KeyError:
                raise UnknownAIProviderError(provider, self._providers) from None

            try:
                import_module(module_path, package=__package__)
                self._loaded[provider] = _ai_extractor_registry[provider]
            except Exception as e:
                raise AIProviderLoadError(provider, e) from e

        return self._loaded[provider]

    def __contains__(self, provider):
        # Mapping.__contains__ calls __getitem__, which would load the provider.
        return provider in self._providers

    def __iter__(self):
        return iter(self._providers)

    def __len__(self):
        return len(self._providers)


ALL_AI_EXTRACTORS = LazyExtractorRegistry()

def validate_model_spec(value: str):
    """Validate stored configuration without constructing an AI client.

    Provider dependencies, credentials, and runtime settings are checked when
    parse_model initializes the provider in a processing worker.
    """
    if not isinstance(value, str) or not value:
        raise ModelError("An AI provider is required")
    provider, separator, model = value.partition(":")
    if provider not in ALL_AI_EXTRACTORS:
        raise UnknownAIProviderError(provider, ALL_AI_EXTRACTORS)
    if separator and not model.strip():
        raise ModelError("An explicit model name must not be empty")
    return value


def __getattr__(name):
    if name == "BaseAIExtractor":
        from .base import BaseAIExtractor
        return BaseAIExtractor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def parse_model(value: str):
    splits = value.split(":", 1)
    provider = splits[0]
    provider = ALL_AI_EXTRACTORS[provider]
    try:
        if len(splits) == 2:
            return provider(model=splits[1])
        return provider()
    except Exception as e:
        raise AIProviderInitializationError(provider, e) from e
