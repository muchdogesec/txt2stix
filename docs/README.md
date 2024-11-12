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

There are 3 types of extractions in txt2stix.

1. Pattern: Pattern extraction type works by using regex patterns to extract data from the inputted document.
    * when to use: for pattern based extractions that are easy to detect
    * when not to use: when objects aren't easily identified by patterns
2. Lookup: Lookup extraction type searches an input document from a list of strings defined in a file (the lookup).
    * when to use: for specialist data not easily detected in patterns
    * when not to use: for large amounts of data (in the lookup)
3. AI: AI extractions work by analysing the users text file input and extracting date (keywords / phrases from it) using the prompt template set for each extraction in `includes/extractions/ai/config.yaml`
    * when to use: contextual types data that can't be easily detected using patterns (e.g. ttps)
    * when not to use: when costs are an issue, when user will not review output for errors

A user can use a mix of all extractions in any request.

#### A note on extraction logic

When searching in written reports, extractions are not always obvious to a machine (when pattern matching).

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

Design decision: this does not apply to AI mode extractions because assumption is AI model is smart enough to deal with extracting data in a more intelligent manner.

### Relationship modes

A user can set the relationship mode at the command line level, depending on the mode set, relationships objects will be created in a certain way.

* standard: all objects created will be linked back to the report
* AI: the extractions and text will be passed to the AI and asked to determine wether any relationships exist between the extractions based on the text.
