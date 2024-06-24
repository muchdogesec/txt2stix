## API

### Authentication

Requests will require not authentication. This tool as designed to be run locally only.

### Schema

To make it easy for users to get up and running, we should build the API against the OpenAPI v3 spec (https://spec.openapis.org/oas/v3.1.0). We can then use Swagger (https://swagger.io/resources/open-api/) to automatically deliver a lightweight view to allow users to interact with the API in the browser.

### Pagination

Default response size for paginated results should be `50`

All paginated responses should contain the header;

```json
{
  "page_number": "<NUMBER>",
  "page_size": "<SET IN ENV>",
  "page_results_count": "<COUNT OF RESULTS ON PAGE>",
  "total_results_count": "<COUNT OF RESULTS ON ALL PAGES>"
```

### Endpoints

#### Get Extractions

The endpoint shows extractions available in txt2stix

```shell
GET HOST/api/VERSION/extractions/
```

Accepts URL parameters

* `page`:
    * default: 1
* `sort`: 
    * name_ascending
    * name_descending
    * type_ascending
    * type_descending (default)

```json
{
    "extractions": [
        {
            "id": "<TXT2STIX EXTRACTION SLUG>",
            "name": "<TXT2STIX EXTRACTION NAME>",
            "description": "<TXT2STIX EXTRACTION DESCRIPTION>",
            "type": "<TXT2STIX EXTRACTION TYPE>"
        },
        {
            "id": "<TXT2STIX EXTRACTION SLUG>",
            "name": "<TXT2STIX EXTRACTION NAME>",
            "description": "<TXT2STIX EXTRACTION DESCRIPTION>",
            "type": "<TXT2STIX EXTRACTION TYPE>"
        }
    ]   
}
```

#### Get Extraction

```shell
GET HOST/api/VERSION/extractions/:extraction_id
```

```json
{
    "extractions": [
        {
            "id": "<TXT2STIX EXTRACTION SLUG>",
            "name": "<TXT2STIX EXTRACTION NAME>",
            "description": "<TXT2STIX EXTRACTION DESCRIPTION>",
            "type": "<TXT2STIX EXTRACTION TYPE>"
        }
    ]
}
```

#### Get Whitelists

The endpoint shows whitelists available in txt2stix

```shell
GET HOST/api/VERSION/whitelists/
```

Accepts URL parameters

* `page`:
    * default: 1
* `sort`: 
    * name_ascending
    * name_descending
    * type_ascending
    * type_descending (default)

```json
{
    "whitelists": [
        {
            "id": "<TXT2STIX WHITELIST SLUG>",
            "name": "<TXT2STIX WHITELIST NAME>",
            "description": "<TXT2STIX WHITELIST DESCRIPTION>",
            "type": "<TXT2STIX WHITELIST TYPE>",
            "file": "<TXT2STIX WHITELIST FILE>"
        },
        {
            "id": "<TXT2STIX WHITELIST SLUG>",
            "name": "<TXT2STIX WHITELIST NAME>",
            "description": "<TXT2STIX WHITELIST DESCRIPTION>",
            "type": "<TXT2STIX WHITELIST TYPE>",
            "file": "<TXT2STIX WHITELIST FILE>"
        }
    ]   
}
```

#### Get Whitelist

The endpoint shows whitelists available in txt2stix

```shell
GET HOST/api/VERSION/whitelists/:whitelist_id
```

```json
{
    "whitelists": [
        {
            "id": "<TXT2STIX WHITELIST SLUG>",
            "name": "<TXT2STIX WHITELIST NAME>",
            "description": "<TXT2STIX WHITELIST DESCRIPTION>",
            "type": "<TXT2STIX WHITELIST TYPE>",
            "file": "<TXT2STIX WHITELIST FILE>"
        }
    ]   
}
```

#### Get Aliases

The endpoint shows aliases available in txt2stix

```shell
GET HOST/api/VERSION/aliases/
```

Accepts URL parameters

* `page`:
    * default: 1
* `sort`: 
    * name_ascending
    * name_descending
    * type_ascending
    * type_descending (default)

```json
{
    "aliases": [
        {
            "id": "<TXT2STIX ALIAS SLUG>",
            "name": "<TXT2STIX ALIAS NAME>",
            "description": "<TXT2STIX ALIAS DESCRIPTION>",
            "type": "<TXT2STIX ALIAS TYPE>",
            "file": "<TXT2STIX ALIAS FILE>"
        },
        {
            "id": "<TXT2STIX ALIAS SLUG>",
            "name": "<TXT2STIX ALIAS NAME>",
            "description": "<TXT2STIX ALIAS DESCRIPTION>",
            "type": "<TXT2STIX ALIAS TYPE>",
            "file": "<TXT2STIX ALIAS FILE>"
        }
    ]   
}
```

#### Get Alias

```shell
GET HOST/api/VERSION/aliases/:alias_id
```

```json
{
    "aliases": [
        {
            "id": "<TXT2STIX ALIAS SLUG>",
            "name": "<TXT2STIX ALIAS NAME>",
            "description": "<TXT2STIX ALIAS DESCRIPTION>",
            "type": "<TXT2STIX ALIAS TYPE>",
            "file": "<TXT2STIX ALIAS FILE>"
        }
    ]   
}
```

#### POST File

```shell
POST HOST/api/VERSION/upload/
```

With the payload of the request containing the following

```json
{
    "input_text": "<VALUE>",
    "relationship_mode": "<VALUE>",
    "name": "<VALUE>"
}
```

A full list of available options is as follows;

* `--relationship_mode` (required): either.
    * `ai`: AI provider must be enabled. extractions performed by either regex or AI for extractions user selected. Rich relationships created from AI provider from extractions.
    * `standard`: extractions performed by either regex or AI (AI provider must be enabled) for extractions user selected. Basic relationships created from extractions back to master Report object generated.
* `--input_text` (required): the file to be converted. Must be raw text
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

A successful response will return a job id

```json
{
    "jobs": [
        {
            "id": "<value>",
            "state": "<value>",
            "run_datetime": "<value>",
            "feed_id": "<value>",
            "info": "<value>"
        }
    ]
}
```

#### GET Get jobs

Jobs allow users to track the status of the request to get posts for feeds they've added to the database.

Jobs for daily updates for each feed are not shown to a user. This only shows jobs triggering a backfill for URL triggered by that user.

```shell
GET HOST/api/VERSION/jobs
```

Accepts URL parameters;

* `bundle_id`: allows results to be filtered by feed ID. Only exists if job is in `success` state
    * default: none
    * required: false
* `state`: either `fail`, `success`, `pending`, `running`
    * default: all
    * required: false
* `page`
    * default: 0
* `sort`
    * run_datetime_descending (default)
    * run_datetime_ascending
    * state_ascending
    * state_descending

200 response

```json
{
    "jobs": [
        {
            "id": "<value>",
            "state": "<value>",
            "run_datetime": "<value>",
            "bundle_id": "<value>",
            "info": "<value>"
        },
        {
            "id": "<value>",
            "state": "<value>",
            "run_datetime": "<value>",
            "feed_id": "<value>",
            "info": "<value>"
        }
    ]
}
```

Response paginated? TRUE

#### Get Job

```shell
GET HOST/api/VERSION/jobs/:job_id
```

200 response

```json
{
    "jobs": [
        {
            "id": "<value>",
            "state": "<value>",
            "run_datetime": "<value>",
            "feed_id": "<value>",
            "info": "<value>"
        }
    ]
}
```

#### GET STIX Bundles

```shell
GET HOST/api/VERSION/bundles/
```

Accepts the URL parameters

* `report_name`
* `report_created_earliest`
* `report_created_latest`
* `page`:
    * default: 1
* `sort`: 
    * title_ascending
    * title_descending
    * report_created_ascending
    * report_created_descending (default)

Will return  

```json
{
    "bundles": [
        {
            "id": "<BUNDLE_NAME>",
            "report_name": "<REPORT_NAME>",
            "report_created": "<REPORT_CREATED>"
        },
        {
            "id": "<BUNDLE_NAME>",
            "report_name": "<REPORT_NAME>",
            "report_created": "<REPORT_CREATED>"
        }
    ]
}
```

#### GET STIX Bundles

```shell
GET HOST/api/VERSION/bundles/:bundle_id
```

Will return the entire bundle payload in the response.

```json
{
    "type": "bundle",
    "id": "bundle--ID",
    "objects": [
        {
            "STIX OBJECTS"
        }
    ]
}
```

PAGINATED: FALSE

### Errors

Bad parameters / bad request format;

```json
{
    "message": " The server did not understand the request",
    "code": 400
}
```

Endpoint does not exist

```json
{
    "message": " The server cannot find the resource you requested",
    "code": 404
}
```