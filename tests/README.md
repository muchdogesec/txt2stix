
Generate test cases

```shell
python3 tests/scripts/generate_simple_extraction_test_cases_txt_files.py
```

Create secrets 

```
## This section is required
CTIBUTLER_BASE_URL=
CTIBUTLER_API_KEY=
VULMATCH_BASE_URL=
VULMATCH_API_KEY=
TEST_AI_MODEL=#e.g openai:gpt-4o
INPUT_TOKEN_LIMIT=1000

## One of the following is required (must match TEST_AI_MODEL)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
OPENROUTER_API_KEY=
```