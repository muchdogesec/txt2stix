# Extractions Types

## Aliases

In many cases two extractions in the same text document might be related to the same thing.

For example, the extraction `USA` and `United States` and `United States of America` are all referring to the same thing.

To account for this, aliases can be used. Aliases are applied before extractions. Essentially the first step of processing is to replace the alias values, with the desired value.

To demonstrate, lets say the alias config file (in `aliases/`) looks like so;

```yaml
country_iso3_to_iso2:
  name: Turns Country ISO2 values into ISO3
  description:
  created: 2020-01-01
  modified:  2020-01-01
  created_by: signalscorps
  version: 1.0.0
  file: /aliases/default/country_iso3_alias.csv
```

This aliases uses the alias file `country_iso3_alias.csv`.

The contents of an alias file has two columns, `value` and `alias`

```csv
value,alias
AFG,AF
ALA,AX
ALB,AL
DZA,DZ
```

This will turn all references of AFG in the input document to AF in the version of the text document sent for extractions/relationship generation.

## Extractions

After aliasing has been applied, extractions happen. There are 3 types of extractions in txt2stix.

1. Pattern
2. Lookup 
3. AI

Regardless of type, all extractions create an extraction json in the format;

```json
{"ai":{"extractions":{"extraction_0":{"type":"<extraction_key>","value":"<extracted_value>","original_text":"<original_text>","start_index":["start_index_n"]},"extraction_n":{"type":"<extraction_key>","value":"<extracted_value>","original_text":"<original_text>","start_index":["start_index_n"]}}},"lookup":{"extractions":{"extraction_n":{"type":"<extraction_key>","value":"<extracted_value>","original_text":"<original_text>","start_index":["start_index_n"]}}},"pattern":{"extractions":{"extraction_n":{"type":"<extraction_key>","value":"<extracted_value>","original_text":"<original_text>","start_index":["start_index_n"]}}}}
```

Where:

* `type`: is the extraction_key value shown in the list printed earlier in this prompt
* `value`: is the value extracted from the text
* `original_text`: is the original text the extraction was made from. Most useful in AI mode where values can be modified
* `start_index`: a list of the index positions of the first character for each matching extraction. Some documents might capture many extractions where `key` and `value` are the same for many entries. This property allows the user to identify how many extractions happened, and where they are in the document.

Note, the `extraction_N` numbers are always unique (even between modes `ai`, `pattern` and `lookup` objects). Put another way, the dock will never contain 2 identical values for `extraction_N` (which is important because of relationship generation).

Below are the extraction types...

### 1. Pattern Extraction type

Pattern extraction type works by using regex patterns to extract data from the inputted document.

To avoid reinventing the wheel, txt2stix doesn't reinvent the wheel where a Python library already exists to do the same job.

### 2. Lookup Extraction type

Lookup extraction type searches an input document from a list of strings defined in a file (the lookup).

#### A note on extraction logic for Pattern, Lookup extraction types and aliasing

When searching in written reports, extractions/aliasing is not always obvious to a machine (when pattern matching).

e.g. lets say `MITRE ATT&CK` was in a report, and country code alpha2 extraction was on (IT and AT might be extracted incorrectly as countries).

It is also common for extractions to be wrapped in punctuation, as follows;

```txt
Just 198.0.103.12:8000 in a sentence.
An IP (198.0.103.12:9000) can be in parentheses.
Here is a sentence. 198.0.103.12:8000, and the IP is followed by a comma.
Here is a sentence, 198.0.103.12:8000. That sentence ended with a full stop.
Sometime markdown `198.0.103.12:8000` is also used.
```

To make it clear, the above formats will all extract. The logic for txt2stix extractions is as follows;

* all extractions with whitespace on either side should extract
    * e.g. `Just 198.0.103.12:8000 in a sentence.`
* all extractions in parenthesis or square brackets `[]` or back ticks ```` or quotes `""` `''` either side should extract
    * e.g. `An IP (198.0.103.12:9000) can be in parentheses.`
    * e.g. `Sometime markdown `198.0.103.12:8000` is also used.`
* all extractions starting with a whitespace prepended by `, ` or `. ` or `! `  characters should extract
    * e.g. `Here is a sentence, 198.0.103.12:8000. That sentence ended with a full stop.`

As you can see, this logic would avoid the issue shown in the `MITRE ATT&CK` example.

Design decision: this does not apply to AI mode extractions (but still applies for aliasing before extractions) because assumption is AI model is smart enough to deal with extracting data in a more intelligent manner.

### 3. AI

AI extractions work by analysing the users text file input and extracting date (keywords / phrases from it).

#### A note on modularisation of AI mode

Whilst the txt2stix MVP is designed for OpenAI, it is not coupled to it.

In future it is likely other modules (other LLMs) will be available to use with txt2stix.

### Data input

When considering a users text inputs, it is very important to be aware of GPT tokens.

Tokens are shared between prompt and completion. For example, if your prompt is 28,000 tokens using GPT-4, your completion can be 4,768 tokens at most (gpt-4-32k) support 32,768 tokens max).

[Currently a user can only use the gpt-4-32k typel](https://platform.openai.com/docs/typels/gpt-4).

We enforce input limits (that can be changed at any time) in the `.env` file under `INPUT_CHARACHTER_LIMIT=`. Default is 32,0000.

### Prompt engineering

In the `extractions/ai/` directory is a file called `config.yaml`

For AI extractions there are a few special properties used to engineer the prompt for an extractions

In the context of the extraction the key properties are:

* `prompt_base` (required): the base prompt that will be used to perform the extraction.
* `prompt_conversion` (optional): can be used to fine tune the extraction and modify the output of the extraction

Both values will be used to create the prompt (if they exist).

#### Prompt 1

This simply provides an instruction to the AI to remember the text. It includes a full copy of the txt file uploaded by the user AFTER any aliases have been applied.

It asks the AI to provide a one word response, either "successful" or "unsuccessful". If unsuccessful returned the script will fail with an error. If successful, the script will continue.

#### Prompt 2

Assuming the word "successful" is returned from prompt 1, a second prompt will be constructed using the `prompt_base` and `prompt_conversion` settings for the `ai` type extractions a user has enabled.

The script asks the AI to produce ONLY a structured extractions JSON output containing information about each extraction detected. 

## Mixing of extraction types

It is completely possible for a user to pass a mix of extraction type modes;

e.g. `--use_extractions lookup_country_alpha2,pattern_ipv4_address_only,ai_directory_unix`

Ultimately extraction mode is run in sequence, e.g. for the above

1. only lookup type extractions run on text
2. only pattern type extractions run on text
3. only ai type extractions passed to AI and run on text

At the end of this process, 3 extractions json documents will exist. These are then concatenated into a single extractions JSON before being passed onto the next step, generate relationship JSON.

# Commons

Much of the core logic for txt2stix is the same regardless of extractions used. This page describes the commonalities for all inputs and extractions.

## TLPs SMOs

At script run time user can set `tlp_level`; either white, green, amber or red.

Each mode maps to a STIX marking definition object;

* Clear: `marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487`
* Green: `marking-definition--bab4a63c-aed9-4cf5-a766-dfca5abac2bb`
* Amber: `marking-definition--55d920b0-5e8b-4f79-9ee9-91f868d9b421`
* Amber+Strict: `marking-definition--939a9414-2ddd-4d32-a0cd-375ea402b003`
* Red: `marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1`

Depending on the value set by user, the generated STIX objects will contain a `marking-definition--` reference in the `object_marking_refs` field to the corresponding TLP level.

## Marking definitions

All objects created by txt2stix also have a standard marking definition in the `object_marking_refs` property.

The default STIX 2.1 marking definition for txt2stix is always used and imported from https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/marking-definition/txt2stix.json

This object will be printed in the final bundle, and in all objects generated by txt2stix in the `object_marking_refs` property.

## Identities (`identity`) SDOs

txt2stix assigns a `created_by_ref` property to all SDOs and SROs it creates to their `created_by_ref` field.

The default STIX 2.1 identity for txt2stix is imported from https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/identity/txt2stix.json

This object will be printed in the final bundle, and the ID will be used for all `created_by_ref` generated by txt2stix.

Often a user will want to use a custom ID of their own to generate objects. They can do this using the `use_identity` flag in the CLI.

Two things will happen if a custom identity is used in this way. The identity JSON object will be printed in the final bundle, and the ID will be used for all `created_by_ref` generated by txt2stix.

## Report SDO (`report`)

All files uploaded are represented as a unique [STIX Report SDO](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_n8bjzg1ysgdq) that take the following structure;

```json
{
    "type": "report",
    "spec_version": "2.1",
    "id": "report--<UUID V4 GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<ITEM INGEST DATE>",
    "modified": "<ITEM INGEST DATE>",
    "name": "<NAME ENTERED ON UPLOAD>",
    "description": "<FULL BODY OF TEXT FROM FILE WITH ALIASES APPLIED>",
    "confidence": "<CONFIDENCE VALUE PASSED AT CLI, IF EXISTS, ELSE NOT PRINTED>",
    "published": "<ITEM INGEST DATE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "labels": [
        "<LABELS ADDED BY USER>"
    ],
    "external_references": [
        {
            "source_name": "txt2stix Report MD5",
            "external_id": "<MD5 HASH OF DESCRIPTION FIELD>"
        }   
    ],
    "object_refs": [
        "<LIST OF ALL VISIBLE EXTRACTED SDO OBJECTS EXCEPT NOTE>"
    ]
}
```

Note, the `object_refs` contains all references that are referenced by objects in the report (SDOs, SROs, SCOs, marking definitions, etc.). This includes extracted objects (i.e. Indicator SDOs, Vulnerability SDOs, Software SCOs, Relationship SROs etc.). The only object it does not include is the Note object created automatically.

`<REPORT OBJECT ID>` should match the report object UUID, e.g. if this was 

## Note SDO (`note`)

All files uploaded have a [Note SDOs](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_gudodcg1sbb9) created to capture 

* the input settings
* the extraction JSON
* the relationships JSON (only generated in AI relationship mode because standard mode relationships are hardcoded)

Note objects are always marked with TLP red `marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1` as the content in them does not usually want to be shared beyond the user running the script.

Each object takes the following structure;

### the input settings

```json
{
    "type": "note",
    "spec_version": "2.1",
    "id": "note--<UUID V4 GENERATED BY STIX2 LIBRARY>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "abstract": "txt2stix Config: <REPORT OBJECT ID>",
    "content": "<THE SETTINGS ENTERED AT COMMAND LINE AS BASE64>",
    "object_refs": ["report--<REPORT OBJECT FOR JOB>"],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        }
    ],
    "object_marking_refs": [
        "marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ]
}
```

### the extraction JSON

```json
{
    "type": "note",
    "spec_version": "2.1",
    "id": "note--<UUID V4 GENERATED BY STIX2 LIBRARY>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "abstract": "txt2stix Extractions: <REPORT OBJECT ID>",
    "content": "<THE EXTRACTIONS JSON AS BASE64>",
    "object_refs": ["report--<REPORT OBJECT FOR JOB>"],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        }
    ],
    "object_marking_refs": [
        "marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ]
}
```

### the relationships JSON (only generated in AI relationship mode)

```json
{
    "type": "note",
    "spec_version": "2.1",
    "id": "note--<UUID V4 GENERATED BY STIX2 LIBRARY>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "abstract": "txt2stix Relationships: <REPORT OBJECT ID>",
    "content": "<THE  RELATIONSHIPS JSON AS BASE64>>",
    "object_refs": ["report--<REPORT OBJECT FOR JOB>"],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        }
    ],
    "object_marking_refs": [
        "marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ]
}
```

## STIX Mapping

All extractions detected by txt2stix, regardless of mode are converted to STIX.

txt2stix uses the [STIX2 Python library](https://pypi.org/project/stix2/) for all STIX 2.1 object generation (except for imported objects).

In the extractions document, a `stix-mapping` property exists for all extractions. 

Below shows how the data extracted is mapped to a set of STIX objects for each `stix-mapping` type.

e.g. if an extraction with a `stix-mapping: ipv4-address` is triggered, the `ipv4-addr` STIX mapping shown below is used.

### Standard Relationships for objects created by extractions

Generally speaking, but not in every case, an extraction will create;

1. An Indicator SDO with a pattern to detect the identified IOC (using a STIX patter)
2. An SCO (referenced in the Indicator SDO pattern)
3. An SRO (between SCO [2.] and SDO [1.])
4. An SRO (between to SDOs for an extraction)

These are described below.

Note, this is different to relationship generation logic for relationship mode set (see relationship-modes.md). The relationships described in this document are created for all modes.

### stix-mapping: ipv4-addr

2 objects created:

* `indicator`
* `ipv4-addr` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: ipv4-addr is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "ipv4: <EXTRACTED IPV4 OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ ipv4-addr:value = '<EXTRACTED IPV4 OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "ipv4-addr",
    "spec_version": "2.1",
    "id": "ipv4-addr--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED IPV4 OBSERVABLE VALUE>"
}
```

### stix-mapping: ipv4-addr-port

3 objects created:

* `indicator`
* `ipv4-addr` (with `relationship` to `indicator`)
* `network-traffic`

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: ipv4-addr is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "ipv4: <EXTRACTED IPV4 OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ ipv4-addr:value = '<EXTRACTED IPV4 OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "ipv4-addr",
    "spec_version": "2.1",
    "id": "ipv4-addr--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED IPV4 OBSERVABLE VALUE>"
}
```

When a port is reported, it could be either a source or destination port.

Generally, threat intel research reports cover destination ports when reported with an IP (they report on what was seen). Therefore, a conscious decision was made that txt2stix always classifies IPs with port numbers as showing destination ports.

```json
{
    "type": "network-traffic",
    "spec_version": "2.1",
    "id": "network-traffic--<GENERATED BY STIX2 LIBRARY>",
    "dst_ref": "ipv4-addr--<IPV4 OBJECT ID>",
    "dst_port": "<EXTRACTED IPV4 PORT VALUE>",
    "protocols": [
        "ipv4"
    ]
}
```

### stix-mapping: ipv6-addr

2 objects created:

* `indicator`
* `ipv6-addr` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: ipv6-addr is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "ipv6: <EXTRACTED IPV6 OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ ipv6-addr:value = '<EXTRACTED IPV6 OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "ipv6-addr",
    "spec_version": "2.1",
    "id": "ipv4-addr--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED IPV6 OBSERVABLE VALUE>"
}
```

### stix-mapping: ipv6-addr-port

3 objects created:

* `indicator`
* `ipv6-addr` (with `relationship` to `indicator`)
* `network-traffic`

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: ipv6-addr is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "ipv6: <EXTRACTED IPV6 OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ ipv6-addr:value = '<EXTRACTED IPV6 OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "ipv6-addr",
    "spec_version": "2.1",
    "id": "ipv4-addr--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED IPV6 OBSERVABLE VALUE>"
}
```

```json
{
    "type": "network-traffic",
    "spec_version": "2.1",
    "id": "network-traffic--<GENERATED BY STIX2 LIBRARY>",
    "dst_ref": "ipv6-addr--<IPV6 OBJECT ID>",
    "dst_port": "<EXTRACTED IPV6 PORT VALUE>",
    "protocols": [
        "ipv4"
    ]
}
```

### stix-mapping: domain-name

2 objects created:

* `indicator`
* `domain-name` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: domain-name is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "Domain: <EXTRACTED DOMAIN NAME OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ domain-name:value = '<EXTRACTED DOMAIN NAME OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "domain-name",
    "spec_version": "2.1",
    "id": "domain-name--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED DOMAIN NAME VALUE>"
}
```

### stix-mapping: url

2 objects created:

* `indicator`
* `url` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: url is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "URL: <EXTRACTED URL OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ url:value = '<EXTRACTED URL OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{  
    "type": "url",
    "spec_version": "2.1",
    "id": "url--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED URL VALUE>"
}
```

### stix-mapping: file

2 objects created:

* `indicator`
* `file` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: file is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "File name: <EXTRACTED FILE NAME OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ file:name = '<EXTRACTED FILE NAME OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "file",
    "spec_version": "2.1",
    "id": "file--<GENERATED BY STIX2 LIBRARY>",
    "name": "<EXTRACTED FILE NAME VALUE>"
}
```

### stix-mapping: directory

2 objects created:

* `indicator`
* `directory` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: directory is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "Directory: <EXTRACTED DIRECTORY OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ directory:path = '<EXTRACTED DIRECTORY OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "directory",
    "spec_version": "2.1",
    "id": "directory--<GENERATED BY STIX2 LIBRARY>",
    "path": "<EXTRACTED DIRECTORY OBSERVABLE VALUE>"
}
```

### stix-mapping: directory-file

3 objects created:

* `indicator`
* `directory` (with `relationship` to `indicator`)
* `file`

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: directory is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "Directory: <EXTRACTED DIRECTORY OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ directory:path = '<EXTRACTED DIRECTORY OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "directory",
    "spec_version": "2.1",
    "id": "directory--<GENERATED BY STIX2 LIBRARY>",
    "path": "<EXTRACTED DIRECTORY OBSERVABLE VALUE>",

}
```

```json
{
    "type": "file",
    "spec_version": "2.1",
    "id": "file--<GENERATED BY STIX2 LIBRARY>",
    "name": "<EXTRACTED FILE NAME VALUE>"
}
```

Note, we decided not to add the `parent_directory_ref` to the file object, as we may see the same file in different directories on different txt2stix runs. As the ID contributing properties of the file object do not consider `parent_directory_ref` it means all filenames with different paths will always have the same ID, which is not what we wanted. Thus, we standardise the filenames to always include the same properties, and use an SRO to join it to the directory.

```json
{
    "type": "relationship",
    "spec_version": "2.1",
    "id": "relationship--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<SIGNALS CORPS IDENTITY ID>",
    "created": "<REPORT CREATED DATE>",
    "modified": "<REPORT CREATED DATE>",
    "relationship_type": "directory",
    "source_ref": "file--<FILE OBJECT>",
    "target_ref": "directory--<DIRECTORY OBJECT>",
    "description": "<FILE NAME> is in the directory <DIRECTORY PATH>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ]
}
```

### stix-mapping: file-hash

2 objects created:

* `indicator`
* `file` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: file is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "<FILE HASH TYPE>: <EXTRACTED FILE HASH OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ file:hashes.<FILE HASH TYPE> = '<EXTRACTED FILE HASH OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "file",
    "spec_version": "2.1",
    "id": "file--<GENERATED BY STIX2 LIBRARY>",
    "hashes": {
        "<FILE HASH TYPE>": "<EXTRACTED FILE HASH OBSERVABLE VALUE>"
    }
}
```

### stix-mapping: email-addr

2 objects created:

* `indicator`
* `email-addr` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: email-addr is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "Email Address: <EXTRACTED EMAIL ADDRESS OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ email-addr:value = '<EXTRACTED EMAIL ADDRESS OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "email-addr",
    "spec_version": "2.1",
    "id": "email-addr--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED EMAIL ADDRESS OBSERVABLE VALUE>"
}
```

### stix-mapping: mac-addr

2 objects created:

* `indicator`
* `mac-addr` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: mac-addr is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "MAC Address: <EXTRACTED MAC ADDRESS OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ mac-addr:value = '<EXTRACTED MAC ADDRESS OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "mac-addr",
    "spec_version": "2.1",
    "id": "mac-addr--<GENERATED BY STIX2 LIBRARY>",
    "value": "<EXTRACTED MAC ADDRESS OBSERVABLE VALUE>"
}
```

### stix-mapping: windows-registry-key

2 objects created:

* `indicator`
* `windows-registry-key` (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: windows-registry-key is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "Windows Registry Key: <EXTRACTED WINDOWS REGISTRY KEY OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ windows-registry-key:key = '<EXTRACTED WINDOWS REGISTRY KEY OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "windows-registry-key",
    "spec_version": "2.1",
    "id": "windows-registry-key--<GENERATED BY STIX2 LIBRARY>",
    "key": "<EXTRACTED WINDOWS REGISTRY KEY OBSERVABLE VALUE>"
}
```

### stix-mapping: autonomous-system

2 objects created:

* `indicator`
* [`autonomous-system`](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_27gux0aol9e3) (with `relationship` to `indicator`)

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: autonomous-system is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "AS<EXTRACTED NUMERICAL AS OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ autonomous-system:number = '<EXTRACTED NUMERICAL AS OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "autonomous-system",
    "spec_version": "2.1",
    "id": "autonomous-system--<GENERATED BY STIX2 LIBRARY>",
    "number": "<EXTRACTED NUMERICAL AS OBSERVABLE VALUE>"
}
```

### stix-mapping: user-agent

3 objects created:

* `indicator`
* `user-agent` (with `relationship` to `indicator`)
* User agent extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/user-agent.json

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: user-agent is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "User Agent: <EXTRACTED FULL USER AGENT STRING>",
    "pattern_type": "stix",
    "pattern": "[ user-agent:string = '<EXTRACTED FULL USER AGENT STRING>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "user-agent",
    "spec_version": "2.1",
    "id": "user-agent--<GENERATED BY STIX2 LIBRARY>",
    "string": "<EXTRACTED FULL USER AGENT STRING>",
    "extensions": {
        "extension-definition--7ca5afee-0e4e-5813-b643-de51538658cc" : {
            "extension_type" : "new-sco"
        }
    }
}
```

### stix-mapping: cryptocurrency-wallet

3 objects created:

* `indicator`
* `cryptocurrency-wallet` (with `relationship` to `indicator`)
* Crypto wallet extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/cryptocurrency-wallet.json

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: cryptocurrency-wallet is connected as source or target object (depending on if extraction is source or target)

```json
  {
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "<CRYPTO TYPE> Wallet: <EXTRACTED CRYPTOCURRENCY OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ cryptocurrency-wallet:address = '<EXTRACTED CRYPTOCURRENCY OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

The `cryptocurrency-wallet` object is generated by [crypto2stix](https://github.com/muchdogesec/crypto2stix).

The crypto2stix equivilant command is;

```shell
python3 crypto2stix.py --wallet HASH --wallet_only
```

Which only generates the wallet object.

### stix-mapping: cryptocurrency-wallet-with-transaction

At least 4 objects created:

* `indicator`
* `cryptocurrency-wallet` (with `relationship` to `indicator`)
* `cryptocurrency-transaction` for all crypto transactions that exist related to the wallet (is not always generated if lookup unsuccessful)
* Crypto wallet extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/cryptocurrency-wallet.json
* Crypto transaction extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/cryptocurrency-transaction.json

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: cryptocurrency-wallet is connected as source or target object (depending on if extraction is source or target)

```json
  {
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "<CRYPTO TYPE> Wallet: <EXTRACTED CRYPTOCURRENCY OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ cryptocurrency-wallet:address = '<EXTRACTED CRYPTOCURRENCY OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

The `cryptocurrency-transaction` object is generated by [crypto2stix](https://github.com/muchdogesec/crypto2stix).

The crypto2stix equivilant command is;

```shell
python3 crypto2stix.py --wallet HASH --transactions_only
```

Which generates the wallet object and any transactions associated with it.

### stix-mapping: cryptocurrency-transaction

5 objects created:

* `indicator`
* `cryptocurrency-transaction` (with `relationship` to `indicator`)
* `cryptocurrency-wallet` for wallets seen in transaction identified by crypto2stix (is not always generated if lookup unsuccessful)
* Crypto transaction extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/cryptocurrency-transaction.json
* Crypto wallet extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/cryptocurrency-wallet.json

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: cryptocurrency-transaction is connected as source or target object (depending on if extraction is source or target)

```json
  {
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "<CRYPTO TYPE> Transaction: <EXTRACTED TRANSACTION HASH>",
    "pattern_type": "stix",
    "pattern": "[ cryptocurrency-transaction:hash = '<EXTRACTED CRYPTOCURRENCY HASH VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "cryptocurrency-transaction",
    "spec_version": "2.1",
    "id": "cryptocurrency-transaction--<UUIDV5>",
    "currency_symbol": "<EXTRACTED CRYPTOCURRENCY OBSERVABLE VALUE>",
    "hash": "<EXTRACTED TRANSACTION HASH>",
    "timestamp": "2022-10-02T15:22:21Z",
    "extensions": {
        "extension-definition--151d042d-4dcf-5e44-843f-1024440318e5" : {
            "extension_type" : "new-sco"
        }
    }
}
```

The `cryptocurrency-transaction` object is generated by [crypto2stix](https://github.com/muchdogesec/crypto2stix).

The crypto2stix equivilant command is;

```shell
python3 crypto2stix.py --transaction HASH
```

This will also generate all `cryptocurrency-wallets` seen in the transaction.

### stix-mapping: bank-card

3 objects created:

* `indicator`
* `bank-card` (with `relationship` to `indicator`)
* `identity` (with `relationship` to `bank-card`) generated by creditcard2stix (is not always generated if lookup unsuccessful)
* Bank card extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/bank-card.json

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: bank-card is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "<CARD TYPE>: <EXTRACTED CREDIT CARD OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ bank-card:number = '<EXTRACTED CREDIT CARD OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

The `bank-card` object is generated by [creditcard2stix](https://github.com/muchdogesec/creditcard2stix). This will require users to enter an `BIN_LIST_API_KEY` in the `.env` file.

### stix-mapping: bank-account

3 objects created:

* `indicator`
* `bank-account` (with `relationship` to `indicator`)
* Bank account extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/bank-account.json

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: bank-card is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "Bank account: <EXTRACTED IBAN OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ bank-account:iban_number = '<EXTRACTED IBAN OBSERVABLE VALUE>' ]",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "bank-account",
    "spec_version": "2.1",
    "id": "bank-account--<UUIDV5>",
    "iban_number": "<FULL IBAN NUMBER INCLUDING COUNTRY CODE>",
    "extensions": {
        "extension-definition--f19f3291-6a84-5674-b311-d75a925d5bd9": {
            "extension_type" : "new-sco"
        }
    }
}
```

To ensure duplicate `bank-account` objects are not created for the same values, a UUIDv5 address is generated for the ID as follows;

* Namespace = `00abedb4-aa42-466c-9c01-fed23315a9b7` (this is the default MITRE namespace used in the stix2 python lib https://github.com/oasis-open/cti-python-stix2/blob/50fd81fd6ba4f26824a864319305bc298e89bb45/stix2/base.py#L29)
* Value = `<iban_number>`

### stix-mapping: phone-number

3 objects created:

* `indicator`
* `phone-number` (with `relationship` to `indicator`)
* Phone number extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/scos/phone-number.json

Relationship modes:

* Standard relationship SRO: Indicator is connected to Report
* AI mode relationship SROs: phone-number is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "indicator_types": [
        "unknown"
    ],
    "name": "Phone Number: <EXTRACTED PHONE OBSERVABLE VALUE>",
    "pattern_type": "stix",
    "pattern": "[ phone-number:number = '<EXTRACTED PHONE OBSERVABLE VALUE>'",
    "valid_from": "<REPORT CREATED PROPERTY VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

```json
{
    "type": "phone-number",
    "spec_version": "2.1",
    "id": "phone-number--<UUIDV5>",
    "number": "<EXTRACTED PHONE OBSERVABLE VALUE>",
    "extensions": {
        "extension-definition--14a97ee2-e666-5ada-a6bd-b7177f79e211" : {
            "extension_type" : "new-sco"
        }
    }
}
```

To ensure duplicate `phone-number` objects are not created for the same values, a UUIDv5 address is generated for the ID as follows;

* Namespace = `00abedb4-aa42-466c-9c01-fed23315a9b7` (this is the default MITRE namespace used in the stix2 python lib https://github.com/oasis-open/cti-python-stix2/blob/50fd81fd6ba4f26824a864319305bc298e89bb45/stix2/base.py#L29)
* Value = `<number>`

### stix-mapping: attack-pattern

1 object created:

* `attack-pattern`

Relationship modes:

* Standard relationship SRO: Attack Pattern is connected to Report
* AI mode relationship SROs: attack-pattern is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "attack-pattern",
    "spec_version": "2.1",
    "id": "campaign--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: campaign

1 object created:

* `campaign`

Relationship modes:

* Standard relationship SRO: Campaign is connected to Report
* AI mode relationship SROs: campaign is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "campaign",
    "spec_version": "2.1",
    "id": "campaign--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: course-of-action

1 object created:

* `course-of-action`

Relationship modes:

* Standard relationship SRO: Course of Action is connected to Report
* AI mode relationship SROs: course-of-action is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "course-of-action",
    "spec_version": "2.1",
    "id": "course-of-action--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: infrastructure

1 object created:

* `infrastructure`

Relationship modes:

* Standard relationship SRO: Infrastructure is connected to Report
* AI mode relationship SROs: infrastructure is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type":"infrastructure",
    "spec_version": "2.1",
    "id":"infrastructure--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "infrastructure_types": ["unknown"],
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: intrusion-set

1 object created:

* `intrusion-set`

Relationship modes:

* Standard relationship SRO: Intrusion Set is connected to Report
* AI mode relationship SROs: intrusion-set is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "intrusion-set",
    "spec_version": "2.1",
    "id": "intrusion-set--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: malware

1 object created:

* `malware`

Relationship modes:

* Standard relationship SRO: Malware is connected to Report
* AI mode relationship SROs: malware is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "malware",
    "spec_version": "2.1",
    "id": "malware--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "malware_types": ["unknown"],
    "is_family": true,
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: threat-actor

1 object created:

* `threat-actor`

Relationship modes:

* Standard relationship SRO: Threat Actor is connected to Report
* AI mode relationship SROs: threat-actor is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "threat-actor",
    "spec_version": "2.1",
    "id": "threat-actor--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "threat_actor_types": "unknown",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: tool

1 object created:

* `tool`

Relationship modes:

* Standard relationship SRO: Tool is connected to Report
* AI mode relationship SROs: tool is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "tool",
    "spec_version": "2.1",
    "id": "tool--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "tool_types": "unknown",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: identity

1 object created:

* `identity`

Relationship modes:

* Standard relationship SRO: Identity is connected to Report
* AI mode relationship SROs: identity is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "identity",
    "spec_version": "2.1",
    "id": "identity--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "<EXTRACTED VALUE>",
    "identity_class": "unspecified",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### stix-mapping: location

1 object created:

* `location`

Relationship modes:

* Standard relationship SRO: Location is connected to Report
* AI mode relationship SROs: location is connected as source or target object (depending on if extraction is source or target)

```json
{
    "type": "location",
    "spec_version": "2.1",
    "id": "location--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT OR CUSTOM IDENTITY OBJECT ID>",
    "created": "<REPORT CREATED PROPERTY VALUE>",
    "modified": "<REPORT MODIFIED PROPERTY VALUE>",
    "name": "Country: <EXTRACTED VALUE>",
    "country": "<EXTRACTED VALUE>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>",
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        },
        {
            "source_name": "txt2stix extraction ID",
            "external_id": "<EXTRACTION SLUG>_<EXTRACTION_VERSION>"
        }
    ]
}
```

### Externally generated STIX objects

Some objects created for extractions do not need to be generated by txt2stix, they can be looked up from an external database.

txt2stix is designed to work with a store of intellignece in ArangoDB uploaded using stix2arango: https://github.com/signalscorps/stix2arango

The data is expected to be imported using: https://github.com/signalscorps/stix2arango/blob/main/design/mvp/backfill.md

If no ArangoDB values are set in the `.env` file, the following extractions will not work.

All request to the ArangoDB API require a JWT. This can be obtained

```shell
curl -X 'POST' \
  'http://<ARANGODB_HOST>:<ARANGODB_POST>/_open/auth' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "<ARANGODB_USERNAME>",
  "password": "<ARANGODB_PASSWORD>"
}'
```

Respone will be in format;

```shell
{"jwt":"<GENERATED JWT>"}
```

The token will need to be renewed with every session.

The actual query (shown below for each extraction) can then be executed as follows;

```shell
curl -X 'POST' \
  'http://<ARANGODB_HOST>:<ARANGODB_POST>/_db/<ARANGODB_DATABASE>/_api/cursor' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: bearer <GENERATED JWT>' \
  -d '{ "query" : "<QUERY>" }'
```

This will return the actual STIX object in the `result` property.

The queries set are always designed to return one result, so the printed STIX object can be imported directly (we also set `"batchSize": 1` for the same reason, but this is not really needed)

### stix-mapping: mitre-attack-enterprise-id

N object created (some IDs match multiple objects):

txt2stix extracts Mitre ATT&CK IDs. These can be passed as `<ID>` in the query below;

```sql
FOR doc IN mitre_attack_enterprise_vertex_collection
    FILTER IS_ARRAY(doc.external_references)
    FOR external_references IN doc.external_references
        FILTER external_references.external_id == '<ID>'
    RETURN UNSET(doc, '_key', '_bundle_id', '_file_name', '_id', '_is_latest', '_record_created', '_record_md5_hash', '_record_modified', '_rev', '_stix2arango_note')
```

Relationship modes:

* Standard relationship SRO: Imported object(s) is connected to Report
* AI mode relationship SROs: all imported objects are connected as source or target object (depending on if extraction is source or target)

### stix-mapping: mitre-attack-mobile-id

N object created (some IDs match multiple objects):

txt2stix extracts Mitre ATT&CK IDs. These can be passed as `<ID>` in the query below;

```sql
FOR doc IN mitre_attack_mobile_vertex_collection
    FILTER IS_ARRAY(doc.external_references)
    FOR external_references IN doc.external_references
        FILTER external_references.external_id == '<ID>'
    RETURN UNSET(doc, '_key', '_bundle_id', '_file_name', '_id', '_is_latest', '_record_created', '_record_md5_hash', '_record_modified', '_rev', '_stix2arango_note')
```

Relationship modes:

* Standard relationship SRO: Imported object(s) is connected to Report
* AI mode relationship SROs: all imported objects are connected as source or target object (depending on if extraction is source or target)

### stix-mapping: mitre-attack-ics-id

N object created (some IDs match multiple objects):

txt2stix extracts Mitre ATT&CK IDs. These can be passed as `<ID>` in the query below;

```sql
FOR doc IN mitre_attack_ics_vertex_collection
    FILTER IS_ARRAY(doc.external_references)
    FOR external_references IN doc.external_references
        FILTER external_references.external_id == '<ID>'
    RETURN UNSET(doc, '_key', '_bundle_id', '_file_name', '_id', '_is_latest', '_record_created', '_record_md5_hash', '_record_modified', '_rev', '_stix2arango_note')
```

Relationship modes:

* Standard relationship SRO: Imported object(s) is connected to Report
* AI mode relationship SROs: all imported objects are c

### stix-mapping: mitre-capec-id

1 object created:

These can be passed as `<ID>` in the query below;

```sql
FOR doc IN mitre_capec_vertex_collection
    FILTER doc.type == 'attack-pattern'
    AND IS_ARRAY(doc.external_references)
    FOR external_references IN doc.external_references
        FILTER external_references.external_id == '<ID>'
    RETURN UNSET( doc, '_key', '_bundle_id', '_file_name', '_id',  '_is_latest', '_record_created', '_record_md5_hash', '_record_modified', '_rev', '_stix2arango_note')
```

Relationship modes:

* Standard relationship SRO: Imported object is connected to Report
* AI mode relationship SROs: all imported objects are connected as source or target object (depending on if extraction is source or target)

### stix-mapping: mitre-cwe-id

2 object created:

* Weakness extension definition: https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions/sdos/weakness.json
* The weakness object described below

These can be passed as `<ID>` in the query below;

```sql
FOR doc IN mitre_cwe_vertex_collection
    FILTER doc.type == 'weakness'
    AND IS_ARRAY(doc.external_references)
    FOR external_references IN doc.external_references
        FILTER external_references.external_id == '<ID>'
    RETURN UNSET( doc, '_key', '_bundle_id', '_file_name', '_id',  '_is_latest', '_record_created', '_record_md5_hash', '_record_modified', '_rev', '_stix2arango_note')
```

Relationship modes:

* Standard relationship SRO: Imported object is connected to Report
* AI mode relationship SROs: all imported objects are connected as source or target object (depending on if extraction is source or target)

### stix-mapping: cve-id

1 object created:

These can be passed as `<ID>` in the query below;

```sql
FOR doc IN nvd_cve_vertex_collection
    FILTER doc.type == 'vulnerability'
    AND doc.name == '<ID>'
    RETURN UNSET( doc, '_key', '_bundle_id', '_file_name', '_id',  '_is_latest', '_record_created', '_record_md5_hash', '_record_modified', '_rev', '_stix2arango_note')
```

Relationship modes:

* Standard relationship SRO: Imported object is connected to Report
* AI mode relationship SROs: all imported objects are connected as source or target object (depending on if extraction is source or target)

### stix-mapping: cpe-id

1 object created:

These can be passed as `<ID>` in the query below;

```sql
FOR doc IN nvd_cpe_vertex_collection
    FILTER doc.type == 'software'
    AND doc.cpe == '<ID>'
    RETURN UNSET( doc, '_key', '_bundle_id', '_file_name', '_id',  '_is_latest', '_record_created', '_record_md5_hash', '_record_modified', '_rev', '_stix2arango_note')
```

Relationship modes:

* Standard relationship SRO: Imported object is connected to Report
* AI mode relationship SROs: all imported objects are connected as source or target object (depending on if extraction is source or target)

## Bundle (output)

The output of txt2stix is a STIX bundle file.

This bundle takes the format;

```json
{
    "type": "bundle",
    "id": "bundle--<SAME AS REPORT UUID PART>",
    "objects": [
        "<ALL STIX JSON DEFAULT AND EXTRACTED OBJECTS>"
    ]
}
```

The objects include all SROs generated for the input.

The filename of the bundle takes the format: `bundle--<ID>.json`

# Relationship modes

A user can set the relationship mode at the command line level, depending on the mode set, relationships objects will be created in a certain way as described in this document...

Regardless of mode, all modes create a relationships json in the format;

```json
{"relationships":{"relationship_0":{"source_ref":"<source extraction id>","target_ref":"<target extraction id>","relationship_type":"<valid relationship type>"},"relationship_n":{"source_ref":"<source extraction id>","target_ref":"<target extraction id>","relationship_type":"<valid relationship type>"}}}
```

Where:

* `source_ref`: is the id for the source extraction for the relationship (e.g. extraction_1).
* `target_ref`: is the index for the target extraction for the relationship (e.g. extraction_2).
* relationship_type: is a description of the relationship between target and source.

Only one type of relationship mode can be used per script run, so only one relationship json is ever produced.

## Standard relationship mode

In standard mode, only one SRO is created for each extraction back to the source report object created for the job. Even so, the script still creates a relationships JSON for the job (but it will contain no data because no relationships between extracted data).

Read the extraction definition in extraction-commons.md to see what objects for an extraction (because there are often >1) that will be linked back to the original report at this step.

### STIX SROs

```json
{
    "type": "relationship",
    "spec_version": "2.1",
    "id": "relationship--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT/CUSTOM IDENTITY ID>",
    "created": "<REPORT CREATED DATE>",
    "modified": "<REPORT CREATED DATE>",
    "relationship_type": "extracted-from",
    "source_ref": "<SOURCE OBJECT ID AS DEFINED BY STIX CONVERSION TYPE>",
    "target_ref": "report--<REPORT OBJECT ID CREATED FOR JOB>",
    "description": "<SOURCE OBJECT NAME> is found in <REPORT NAME>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>"
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        }
    ]
}
```

## AI relationship mode

This mode takes the extractions generated and passes them, along with the text of the report input (after aliases applied).

Which is then used in a series of prompts...

### Prompts

#### Prompt 1 (skipped if NO `ai_` extractions applied)

This simply provides an instruction to the AI to remember the text. It includes a full copy of the txt file uploaded by the user AFTER any aliases have been applied.

It asks the AI to provide a one word response, either "successful" or "unsuccessful". If unsuccessful returned the script will fail with an error. If successful, the script will continue.

It is the same as prompt 1 for extractions of `ai_` type, thus this prompt IS NOT used if any AI extraction performed as this prompt will have already been sent (and resending will use up more tokens when not required).

#### Prompt 2 (skipped if ONLY `ai_` extractions applied)

Prompt 2 passed the final extractions JSON and asks the prompt to remember the extractions for the next step.

It asks the AI to provide a one word response, either "successful" or "unsuccessful". If unsuccessful returned the script will fail with an error. If successful, the script will continue.

If ONLY `ai_` extractions used (that is, NO lookup or pattern extractions done) then this prompt is skipped, as the AI will already have the full extractions JSON file it created.

#### Prompt 3

Assuming the word "successful" is returned from prompt 2, the script asks the AI to produce ONLY a structured relationship JSON output containing information about links between extractions.

In this prompt, the list of supported relationship types, defined in `helpers/stix_relationship_types.txt`, are also passed to the AI to limit the `relationship_type` descriptions it makes.

### STIX SROs

The LLM generates a JSON file describing how objects created from extractions are connected.

Keep in mind, an extraction generally, but not always creates at least two non-relationship objects, an SDO and an SCO. You should read the extraction definition in extraction-commons.md to see what objects will be linked using the relationship for an extraction.

The Relationship will be generated as follows;

```json
{
    "type": "relationship",
    "spec_version": "2.1",
    "id": "relationship--<GENERATED BY STIX2 LIBRARY>",
    "created_by_ref": "identity--<DEFAULT/CUSTOM IDENTITY ID>",
    "created": "<REPORT CREATED DATE>",
    "modified": "<REPORT CREATED DATE>",
    "relationship_type": "<OPENAI REPORTED RELATIONSHIP_TYPE>",
    "source_ref": "<SOURCE OBJECT ID AS DEFINED BY STIX CONVERSION TYPE>",
    "target_ref": "<TARGET OBJECT ID AS DEFINED BY STIX CONVERSION TYPE>",
    "description": "<SOURCE OBJECT NAME FOR SDO OR FOR SDO VALUE/HASHES/PATH/KEY/NUMBER/STRING/ADDRESS/HASH/SYMBOL/IBAN_NUMBER/DEFAULT TO ID IF NO VALUE> <relationship_type> <TARGET OBJECT SDO/SCO NAME/VALUE/ETC.>",
    "object_marking_refs": [
        "marking-definition--<TLP LEVEL SET>"
        "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5"
    ],
    "external_references": [
        {
            "source_name": "txt2stix job ID",
            "external_id": "<REPORT OBJECT ID>"
        }
    ]
}
```

Note, a source object can be linked to many target objects in the same report. Thus, a source object might create many SROs, representing links to target objects.

Similarly, in the case of MITRE ATT&CK an extraction might import one or more STIX objects. In this case, an SRO should be created for each imported object to the source/target object identified.