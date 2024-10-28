# txt2stix

## Overview

![txt2stix](docs/txt2stix.png)

txt2stix is a Python script that is designed to identify and extract IoCs and TTPs from text files, identify the relationships between them, convert them to STIX 2.1 objects, and output as a STIX 2.1 bundle.

The general design goal of txt2stix was to keep it flexible, but simple, so that new extractions could be added or modified over time.

In short txt2stix;

1. takes a txt file input
2. (optional) rewrites file with enabled aliases
3. extracts observables for enabled extractions (ai, pattern, or lookup)
4. (optional) removes any extractions that match whitelists
5. converts extracted observables to STIX 2.1 objects
6. generates the relationships between extracted observables (ai, standard)
7. converts extracted relationships to STIX 2.1 SRO objects
8. outputs a STIX 2.1 bundle

## tl;dr

[![txt2stix](https://img.youtube.com/vi/TWVGCou9oGk/0.jpg)](https://www.youtube.com/watch?v=TWVGCou9oGk)

[Watch the demo](https://www.youtube.com/watch?v=TWVGCou9oGk).

## Usage

### Setup

Install the required dependencies using:

```shell
# clone the latest code
git clone https://github.com/muchdogesec/txt2stix
cd txt2stix
# create a venv
python3 -m venv txt2stix-venv
source txt2stix-venv/bin/activate
# install requirements
pip3 install -r requirements.txt
```

Now copy the `.env` file to set your config:

```shell
cp .env.sample .env
```

You can new set the correct values in `.env`.

### Usage

```shell
python3 txt2stix.py \
	--relationship_mode MODE \
	--input_file FILE.txt \
	--name NAME \
	--tlp_level TLP_LEVEL \
	--confidence CONFIDENCE_SCORE \
	--labels label1,label2 \
	--created DATE \
	--use_identity \{IDENTITY JSON\} \
	--use_extractions EXTRACTION1,EXTRACTION2 \
	--use_aliases ALIAS1,ALIAS2 \
	--use_whitelist WHITELIST1,WHITELIST2
```

* `--relationship_mode` (required): either.
	* `ai`: AI provider must be enabled. extractions performed by either regex or AI for extractions user selected. Rich relationships created from AI provider from extractions.
	* `standard`: extractions performed by either regex or AI (AI provider must be enabled) for extractions user selected. Basic relationships created from extractions back to master Report object generated.
* `--input_file` (required): the file to be converted. Must be `.txt`
* `--name` (required): name of file, max 72 chars. Will be used in the STIX Report Object created.
* `--report_id` (optional): Sometimes it is required to control the id of the `report` object generated. You can therefore pass a valid UUIDv4 in this field to be assigned to the report. e.g. passing `2611965-930e-43db-8b95-30a1e119d7e2` would create a STIX object id `report--2611965-930e-43db-8b95-30a1e119d7e2`. If this argument is not passed, the UUID will be randomly generated.
* `--tlp_level` (optional): Options are `clear`, `green`, `amber`, `amber_strict`, `red`. Default if not passed, is `clear`.
* `--confidence` (optional): value between 0-100. Default if not passed is null.
* `--labels` (optional): comma seperated list of labels. Case-insensitive (will all be converted to lower-case). Allowed `a-z`, `0-9`. e.g.`label1,label2` would create 2 labels.
* `--created` (optional): by default all object `created` times will take the time the script was run. If you want to explicitly set these times you can do so using this flag. Pass the value in the format `YYYY-MM-DDTHH:MM:SS.sssZ` e.g. `2020-01-01T00:00:00.000Z`
* `--use_identity` (optional): can pass a full STIX 2.1 identity object (make sure to properly escape). Will be validated by the STIX2 library.
* `--use_extractions` (required): if you only want to use certain extraction types, you can pass their slug found in either `ai/config.yaml`, `lookup/config.yaml` `regex/config.yaml` (e.g. `regex_ipv4_address_only`). Default if not passed, no extractions applied.
	* Important: if using any AI extractions, you must set an OpenAI API key in your `.env` file
	* Important: if you are using any MITRE ATT&CK, CAPEC, CWE you must set `CTIBUTLER` or NVD CPE, CVE extractions you must set `VULMATCH` settings in your `.env` file
* `--use_aliases` (optional): if you want to apply aliasing to the input doc (find and replace strings) you can pass their slug found in `aliases/config.yaml` (e.g. `country_iso3_to_iso2`). Default if not passed, no extractions applied.
* `--use_whitelist` (optional): if you want to get the script to ignore certain values that might create extractions you can specify using `whitelist/config.yaml` (e.g. `alexa_top_1000`) related to the whitelist file you want to use. Default if not passed, no extractions applied.

## Adding new extractions/lookups/aliases

It is very likely you'll want to extend txt2stix to include new extractions, aliases, and/or lookups. The following is possible:

* Add a new lookup extraction: add your lookup to `lookups` as a `.txt` file. Lookups should be a list of items seperated by new lines to be searched for in documents. Once this is added, update `extactions/lookups/config.yaml` with a new record pointing to your lookup. You can now use this lookup time at script run-time.
* Add a new AI extraction: Edit `extactions/ai/config.yaml` with a new record for your extraction. You can craft the prompt used in the config to control how the LLM performs the extraction.
* Add a new alias: add a your alias to `aliases` as a `.csv` file. Alias files should have two columns `value,alias`, where `value` is the document in the original document to replace and `alias` is the value it should be replaced with.

Currently it is not possible to easily add any other types of extractions (without modifying the logic at a code level).

## Detailed documentation

If you would like to understand how txt2stix works in more detail, please refer to the documentation in `/docs/README.md`.

This documentation is paticularly helpful to read for those of you wanting to add your own custom extractions.

## Useful supporting tools

* [Python Validators](https://validators.readthedocs.io/en/latest/#)
* [STIX 2](https://pypi.org/project/stix2/): APIs for serializing and de-serializing STIX2 JSON content
* [STIX 2 Pattern Validator](https://pypi.org/project/stix2-patterns/): a tool for checking the syntax of the Cyber Threat Intelligence (CTI) STIX Pattern expressions
* [MISP Warning Lists](https://github.com/MISP/misp-warninglists): Warning lists to inform users of MISP about potential false-positives or other information in indicators
* [STIX Viewer](https://github.com/traut/stixview): Quickly load bundles produced from your report

## Support

[Minimal support provided via the DOGESEC community](https://community.dogesec.com/).

## License

[Apache 2.0](/LICENSE).