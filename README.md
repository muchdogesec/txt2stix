# txt2stix

## Overview

txt2stix is a Python script that is designed to identify and extract IoCs and TTPs from text files, identify the relationships between them, convert them to STIX 2.1 objects, and output as a STIX 2.1 bundle.

The general design goal of txt2stix was to keep it flexible, but simple, so that new extractions could be added or modified over time.

In short txt2stix;

1. takes a txt file input
2. rewrites file with enabled aliases
3. extracts observables for enabled extractions (and ignores any whitelisted values)
4. converts extracted observables to STIX 2.1 objects
5. generates the relationships between extracted observables
6. converts extracted relationships to STIX 2.1 SRO objects
7. outputs a STIX 2.1 bundle

## The problem

More-and-more organisations are standardising the way the represent threat intelligence using the STIX 2.1 data model.

As a result, an increasing number of SIEMs, SOARs, TIPs, etc. have native STIX 2.1 support.

However, authoring STIX 2.1 content can be laborious. I have seen analysts manually copy and paste data from reports, blogs, emails, and other sources into STIX 2.1 Objects.

In many cases these Observables (IOCs) can be automatically detected in plain text using defined patterns.

For example, an IPv4 observable has a specific pattern that can be identified using regular expressions. This regular expression will match an IPv4 observable;

```regex
^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$
```

Similarly, the following regular expression will capture URLs;

```regex
^(https?|ftp|file)://.+$
```

Both of these examples ([here](https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html) and [here](https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s01.html), respectively) are taken from the brilliant Regular Expressions Cookbook (2nd edition) by Jan Goyvaerts and Steven Levithan.

Now this isn't rocket science, and indeed there are already quite a few open source tools that contain regular expressions for extracting Observables in this way;

* [IoC extractor](https://github.com/ninoseki/ioc-extractor): An npm package for extracting common IoC (Indicator of Compromise)
* [IOC Finder](https://github.com/fhightower/ioc-finder): Simple, effective, and modular package for parsing Observables (indicators of compromise (IOCs), network data, and other, security related information) from text.
* [cacador](https://github.com/sroberts/cacador): Indicator Extractor
* [iocextract](https://github.com/InQuest/python-iocextract): Defanged Indicator of Compromise (IOC) Extractor.
* [Cyobstract](https://github.com/cmu-sei/cyobstract): A tool to extract structured cyber information from incident reports.

However, we wanted a more modularised extraction logic, especially to take advantage of the new accessibility of AI.

## Concepts

Here is an overview of how the txt2stix processes txt files into STIX 2.1 bundles:

<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVKEyFzB8=/?moveToViewport=-762,-540,2696,919&embedId=241901701201" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>

### Extractions

This is the logic that actually extracts the text from the input document.

txt2stix has 3 types of extracions;

1. AI: uses an LLM to extracts the data based on a prompt
	* when to use: contextual types data that can't be easily detected using patterns
	* when not to use: when costs are an issue, when user will not review output for errors
2. Pattern: all extractions will be performed by regular expressions (or via existing Python libraries).
	* when to use: for pattern based
	* when not to use: when costs are an issue, where user will not 
3. Lookups: file2txt will compare strings in input document against a list of strings in lookups
	* when to use: for specialist data not easily detected in patterns
	* when not to use: for large amounts of data (in the lookup)

### Relationships

This is how extractions are joined together using STIX SROs.

There are 2 relationship modes in txt2stix;

* `ai`: Rich relationships created by LLM between extractions.
* `standard`: Basic relationships created from extractions back to master Report object generated.

### Aliases

In many cases two extractions might be related to the same thing. For example, the extraction `USA` and `United States` and `United States of America` are all referring to the same thing.

Aliases normalise the input text before extractions happen so that the same extraction is used. e.g. changing `United States` -> `USA`.

### Whitelists

In many cases files will have IoC extractions that are not malicious. e.g. `google.com` (and thus they don't want them to appear in final bundle).

Whitelists provide a list of values to be compared to extractions. If a whitelist value matches an extraction, that extraction is removed and any relationships where is the `source_ref` or `target_ref` are also removed so that a user does not see them.

Design decision: This is done after extractions to save tokens with AI providers (otherwise might be easily passing 10000+ more tokens to the AI).

Note, whitelists are designed to be simplistic in txt2stix. If you want more advanced removal of potential benign extractions you should use another tool, like a Threat Intelligence Platform.

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

A quick note on OPEN_AI and ARANGODB variables....

`OPENAI_*` properties are required should you want to use AI based extractions or AI relationship mode. If left blank, you can use pattern extractions and standard relationship modes only.

`ARANGODB_*` properties are required if you want to use MITRE ATT&CK, MITRE CWE, MITRE CAPEC, NVD CPE, or NVD CVE extractions. You must define an ArangoDB instance with the required data in the expected format in order for these extraction types to work.

You can populate your own instance of ArangoDB with the required data by using the scripts in [stix2arango](https://github.com/muchdogesec/stix2arango)

**Make life simpler for yourself...**

If you do not want to backfill, maintain, or support your own ArangoDB STIX objects check out CTI Butler which provides a fully manage database of these objects you can use with txt2stix.

https://www.ctibutler.com/

### Usage

```shell
python3 txt2stix.py \
	--relationship_mode MODE \
	--input_file FILE.txt \
	--name NAME \
	--tlp_level TLP_LEVEL \
	--confidence CONFIDENCE_SCORE \
	--label label1,label2 \
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
* `--labels` (optional): comma seperated list of labels. Case-insensitive (will all be converted to lower-case). Allowed `a-z`, `0-9`. e.g.`label1,label2` would create 2 labels.
* `--tlp_level` (optional): Options are `clear`, `green`, `amber`, `amber_strict`, `red`. Default if not passed, is `clear`.
* `--confidence` (optional): value between 0-100. Default if not passed is null.
* `--use_identity` (optional): can pass a full STIX 2.1 identity object (make sure to properly escape). Will be validated by the STIX2 library.
* `--use_extractions` (required): if you only want to use certain extraction types, you can pass their slug found in either `ai/config.yaml`, `lookup/config.yaml` `regex/config.yaml` (e.g. `regex_ipv4_address_only`). Default if not passed, no extractions applied.
	* Important: if using any AI extractions, you must set an OpenAI API key in your `.env` file
	* Important: if you are using any MITRE ATT&CK, CAPEC, CWE or NVD CPE or CVE extractions you must set ArangoDB settings in your `.env` file
* `--use_aliases` (optional): if you want to apply aliasing to the input doc (find and replace strings) you can pass their slug found in `aliases/config.yaml` (e.g. `country_iso3_to_iso2`). Default if not passed, no extractions applied.
* `--use_whitelist` (optional): if you want to get the script to ignore certain values that might create extractions you can specify using `whitelist/config.yaml` (e.g. `alexa_top_1000`) related to the whitelist file you want to use. Default if not passed, no extractions applied.

## Adding new extractions/lookups/aliases

It is very likely you'll want to extend txt2stix to include new extractions, aliases, and/or lookups. The following is possible:

* Add a new lookup extraction: add your lookup to `lookups` as a `.txt` file. Lookups should be a list of items seperated by new lines to be searched for in documents. Once this is added, update `extactions/lookups/config.yaml` with a new record pointing to your lookup. You can now use this lookup time at script run-time.
* Add a new AI extraction: Edit `extactions/ai/config.yaml` with a new record for your extraction. You can craft the prompt used in the config to control how the LLM performs the extraction.
* Add a new alias: add a your alias to `aliases` as a `.csv` file. Alias files should have two columns `value,alias`, where `value` is the document in the original document to replace and `alias` is the value it should be replaced with.

Currently it is not possible to easily add any other types of extractions (without modifying the logic at a code level).

## Detailed documentation

If you would like to understand how txt2stix works in more detail, please refer to the documentation in `/doc`.

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

[AGPLv3](/LICENSE).
