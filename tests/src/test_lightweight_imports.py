import os
import subprocess
import sys
import textwrap


def run_clean(code):
    subprocess.run([sys.executable, '-c', textwrap.dedent(code)], check=True,
                   timeout=120, env=os.environ.copy())


def test_metadata_and_model_validation_do_not_import_processing_dependencies():
    run_clean('''
        import sys
        import txt2stix
        from txt2stix.ai_extractor import ALL_AI_EXTRACTORS, ModelError, validate_model_spec

        assert txt2stix.get_all_extractors()['pattern_ipv4_address_only'].type == 'pattern'
        for provider in ('openai', 'anthropic', 'gemini', 'deepseek', 'openrouter'):
            assert provider in ALL_AI_EXTRACTORS
            assert validate_model_spec(provider) == provider
            spec = provider + ':custom/model:variant'
            assert validate_model_spec(spec) == spec
        assert 'unknown' not in ALL_AI_EXTRACTORS
        for invalid in ('', 'unknown:model', 'openai:', 'openai:   ', None):
            try:
                validate_model_spec(invalid)
            except ModelError:
                pass
            else:
                raise AssertionError(invalid)

        forbidden = ('txt2stix.bundler', 'txt2stix.indicator', 'txt2stix.txt2stix',
                     'txt2stix.pattern', 'llama_index', 'transformers', 'pandas',
                     'openai', 'google.genai', 'phonenumbers.geodata')
        loaded = [name for name in sys.modules if any(name == p or name.startswith(p + '.') for p in forbidden)]
        assert not loaded, loaded
    ''')


def test_base_class_and_language_imports_are_lightweight():
    run_clean('''
        import sys
        from txt2stix.ai_extractor import BaseAIExtractor
        from txt2stix.ai_extractor import prompts
        from txt2stix.language import detect_language

        assert BaseAIExtractor.system_prompt == prompts.DEFAULT_SYSTEM_PROMPT
        for prefix in ('llama_index', 'py3langid', 'numpy'):
            assert not any(n == prefix or n.startswith(prefix + '.') for n in sys.modules)

        from llama_index.core import PromptTemplate, ChatPromptTemplate
        for attr, name in (
            ('extraction_template', 'DEFAULT_EXTRACTION_TEMPL'),
            ('relationship_template', 'DEFAULT_RELATIONSHIP_TEMPL'),
            ('content_check_template', 'DEFAULT_CONTENT_CHECKER_WITH_SUMMARY_TEMPL'),
        ):
            template = getattr(prompts, name)
            assert isinstance(template, PromptTemplate)
            assert getattr(BaseAIExtractor, attr) is template
            assert getattr(BaseAIExtractor(), attr) is template
            assert template.template == getattr(prompts, '_' + name + '_DATA')
        chat = prompts.ATTACK_FLOW_PROMPT_TEMPL
        assert isinstance(chat, ChatPromptTemplate)
        assert [(m.role.value, m.content) for m in chat.message_templates] == prompts._ATTACK_FLOW_PROMPT_TEMPL_DATA
        instance = BaseAIExtractor()
        override = PromptTemplate('custom {text}')
        instance.extraction_template = override
        assert instance.extraction_template is override
        class Custom(BaseAIExtractor, provider='custom', register=False):
            extraction_template = override
        assert Custom().extraction_template is override
        assert 'py3langid' not in sys.modules
        assert detect_language('This is a report describing a malware campaign targeting financial institutions.') == 'en'
        assert 'py3langid' in sys.modules
    ''')


def test_lazy_public_exports_and_phone_country_lookup_remain_compatible():
    run_clean('''
        import sys
        from txt2stix import txt2stixBundler
        from txt2stix.bundler import txt2stixBundler as direct
        from txt2stix.ai_extractor import BaseAIExtractor
        from txt2stix.ai_extractor.base import BaseAIExtractor as direct_base
        from txt2stix.indicator import get_country_code

        assert txt2stixBundler is direct
        assert BaseAIExtractor is direct_base
        assert get_country_code('+14155552671') == 'US'
        assert get_country_code('+2349012345678') == 'NG'
        assert 'phonenumbers.geocoder' not in sys.modules
        assert 'phonenumbers.geodata' not in sys.modules
    ''')


def test_legacy_model_parser_and_include_configuration():
    run_clean('''
        import argparse
        from pathlib import Path
        from unittest.mock import patch
        import txt2stix
        from txt2stix.ai_extractor import ModelError
        from txt2stix import txt2stix as engine
        from txt2stix.ai_extractor.utils import DescribesIncident
        from txt2stix.ai_extractor.data_models import DescribesIncident as moved

        assert DescribesIncident is moved
        assert engine.Txt2StixData is not None
        assert engine.INCLUDES_PATH.exists()
        original = txt2stix.get_include_path()
        txt2stix.set_include_path(Path('/custom/includes'))
        assert txt2stix.get_include_path() == Path('/custom/includes')
        assert txt2stix.INCLUDES_PATH == Path('/custom/includes')
        txt2stix.set_include_path(original)
        class Provider:
            def __init__(self, model=None):
                self.model = model
        with patch.object(engine, 'ALL_AI_EXTRACTORS', {'example': Provider}):
            assert engine.parse_model('example:custom:model').model == 'custom:model'
            try:
                engine.parse_model('unknown')
            except argparse.ArgumentTypeError:
                pass
            else:
                raise AssertionError('Unknown provider accepted')
        def broken():
            raise RuntimeError('missing credentials')
        with patch.object(engine, 'ALL_AI_EXTRACTORS', {'broken': broken}):
            try:
                engine.parse_model('broken')
            except ModelError:
                pass
            else:
                raise AssertionError('Model initialization error not preserved')
    ''')
