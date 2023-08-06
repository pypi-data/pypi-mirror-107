# itfr-btdp-pyPI-lib-lologging

This is the first version of our meaningfull logging library.
The purpose of this library is to provide clear error logs for all python cloud run services running on GCP. 


loreal logging => lologging

## Test locally

Run command:

```bash 
python3 setup.py pytest

```

## Deploy to pyPI

First update version number and download_url in setup.py

Run commands:

```bash
# Install twine
pip3 install twine

# Build dist folder
python3 setup.py sdist

# Deploy to pyPI
twine upload dist/*
```

This is the tutorial that was followed 
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56 

## Usage

The function both logs and returns the error or success message

```python
from google.cloud import logging as glogging
logging_client = glogging.Client()
from lologging import lologging
lologger=lologging.Client(logging_client=logging_client, service_name="test-service", logger_name="cloudrun-custom-logs")
import traceback

def test_test_function():
    try:
        raise FileNotFoundError("This is my explanation")
    except FileNotFoundError as e:
        assert lologger.print_log_and_return(
            severity=SEVERITY,
            message=MESSAGE,
            [traceback=TRACEBACK],
            code=CODE)
```

Where:

* `service_name`: Name of the cloud run service
* `logger_name`: Name of the logger => Defines a new logger which in turn creates, via logs router, a new destination table in bigquery in the monitoring project

* `severity`: One of: "ERROR, INFO" if "ERROR" then the log is forwarded to the bq log sync
* `message`: Either the error or a success message
* `traceback` (optional): the traceback
* `code`: The error code
 
## Samples

Error with traceback:

```python
def test_test_function():
    try:
        raise FileNotFoundError("This is my explanation/ Clem")
    except FileNotFoundError as e:
        assert lologger.print_log_and_return(
            severity="ERROR",
            message=e,
            status_code=400,
            traceback=traceback.format_exc()
            )

```

Success message:

```python
    return lologger.print_log_and_return(
        severity="INFO",
        message=f"File {source} successfully moved to {destination}",
        status_code=200,
        details = {
            "source": glob_list(source),
            "destination": destination_glob_list
        }
    )

```

