# itfr-btdp-pyPI-lib-lologging

This is the first version of our meaningfull logging library.
The purpose of this library is to provide clear error logs for all python cloud run services running on GCP. 

loreal logging => lologging

## Test locally

Run command:

```
python3 setup.py pytest

```

## Deploy to pyPI

Run commands:

```
# Install twine
pip3 install twine

# Build dist folder
python3 setup.py sdist

# Deploy to piPI
twine upload dist/*
```

This is the tutorial that was followed 
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56 

## Usage

Method: `POST`

Endpoint: `/`

Body:

```json
{
    "source": "gs://frsellout-gcs-input-boost-eu-dv/ARTICLES",
    "load_config": {
        "destination": "frsellout_bqdset_stg_sellout_eu_dv.articles",
        "source_format": "CSV",
        "write_disposition": "WRITE_TRUNCATE",
        "field_delimiter": "|",
        "skip_leading_rows": 1,
        "allow_jagged_rows": false,
        "autodetect": true,
        "schema": [
            {
                "name": "field1",
                "description": "description",
                "type": "STRING",
                "mode": "NULLABLE"
            }
        ],
        "schema_file": "gs://mybucket/myfile.json"
    },
    "num_retries": 3
}
```

Where:

* `source`: path on Google Cloud Storage to the file to load (format: gs://xxx/yyy)
* `load_config`:
  * `destination`: name of BigQuery table where to load data. In the format project_id.dataset_id.table_id or dataset_id.table_id.
  * `source_format` (optional): format of source file. Could be CSV, AVRO, NEWLINE_DELIMITED_JSON, PARQUET, ORC. Defaults to CSV.
  * `write_disposition` (optional): WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY. Defaults to WRITE_TRUNCATE.
  * `field_delimiter`: in case of a CSV file, indicates the delimiter character.
  * `skip_leading_rows`: in case of a CSV file, indicates the number of lines to skip at the head of the file.
  * `allow_jagged_rows` (optional): in case of a CSV file, indicates if input rows can lack trailing columns. Default: false.
  * `autodetect` (optional): true or false. If false, you need to provide the `schema` of the table.
  * `schema` (optional): Schema of the external table.
    * `name`: Name of field.
    * `type`: Type of field (STRING, INTEGER, FLOAT, ...)
    * `mode` (optional): NULLABLE or REQUIRED.
    * `description` (optional): friendly description of field.
  * `schema_file` (optional): Schema file of the external table format: gs://xxx/yyy.json).
* `num_retries` (optional): specify the number of retries before failing, with random exponential backoff between each retry. Default: 3 retries.

## Sample requests

To send a request to the API, use for instance Postman <https://www.postman.com/> or curl.

Local request:

```bash
curl -X POST \
-H "Content-Type: application/json" \
http://0.0.0.0:8080/ \
-d '{"source": "gs://frsellout-gcs-input-boost-eu-dv/ARTICLES","load_config": {"destination": "frsellout_bqdset_stg_sellout_eu_dv.articles","source_format": "CSV","write_disposition":"WRITE_TRUNCATE","field_delimiter": "|","skip_leading_rows": 1}}'
```

Request sent to Cloud Run service:

```bash
curl -X POST -H \
"Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" \
https://cloudrun-bqload-lzsxxklfta-ew.a.run.app -d '{"source": "gs://frsellout-gcs-input-boost-eu-dv/ARTICLES","load_config": {"destination": "frsellout_bqdset_stg_sellout_eu_dv.articles","source_format": "CSV","write_disposition":"WRITE_TRUNCATE","field_delimiter": "|","skip_leading_rows": 1}}'
```

Where: <https://cloudrun-bqload-lzsxxklfta-ew.a.run.app> is the URL of your Cloud Run service.
The command `gcloud auth print-identity-token` allows you to authenticate to your service endpoint.



