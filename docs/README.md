# Docs

## Overview

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

Now this isn't rocket science, and indeed there are already quite a few open source tools that contain regular expressions for extracting Observables in this way.

However, we wanted a more modularised extraction logic, especially to take advantage of the new accessibility of AI.

## Concepts

Here is an overview of how the txt2stix processes txt files into STIX 2.1 bundles:

https://miro.com/app/board/uXjVKEyFzB8=/

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

* `ai`: NLP based relationships created by LLM between extractions.
* `standard`: Basic relationships created from extractions back to master Report object generated.

### Aliases

In many cases two extractions might be related to the same thing. For example, the extraction `USA` and `United States` and `United States of America` are all referring to the same thing.

Aliases normalise the input text before extractions happen so that the same extraction is used. e.g. changing `United States` -> `USA`.

Aliases are applied before extractions. Essentially the first step of processing is to replace the alias values, with the desired value.

The aliaases are set in the `includes/extractions/config.yaml`

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

This will turn all references of AFG in the inp

### Whitelists

In many cases files will have IoC extractions that are not malicious. e.g. `google.com` (and thus they don't want them to appear in final bundle).

Whitelists provide a list of values to be compared to extractions. If a whitelist value matches an extraction, that extraction is removed and any relationships where is the `source_ref` or `target_ref` are also removed so that a user does not see them.

Design decision: This is done after extractions to save tokens with AI providers (otherwise might be easily passing 10000+ more tokens to the AI).

Note, whitelists are designed to be simplistic in txt2stix. If you want more advanced removal of potential benign extractions you should use another tool, like a Threat Intelligence Platform.


# Extractions Types


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



## Mixing of extraction types

It is completely possible for a user to pass a mix of extraction type modes;

e.g. `--use_extractions lookup_country_alpha2,pattern_ipv4_address_only,ai_directory_unix`

Ultimately extraction mode is run in sequence, e.g. for the above

1. only lookup type extractions run on text
2. only pattern type extractions run on text
3. only ai type extractions passed to AI and run on text

At the end of this process, 3 extractions json documents will exist. These are then concatenated into a single extractions JSON before being passed onto the next step, generate relationship JSON.



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

