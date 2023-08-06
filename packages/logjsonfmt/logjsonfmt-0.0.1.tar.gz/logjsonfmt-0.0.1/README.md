# log-json-fmt

python logging json formatter.

## Installation

<div class="termy">

```console
$ pip install logjsonfmt

---> 100%
```

</div>

## Example

### Create it

* Create a file `example.py` with:

```Python
import logging
import logjsonfmt

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = logjsonfmt.JSONFormatter(hostname="app.example.com", indent=True)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.error('hello world!', extra={"tags": ["app=helloworld"]})
```
Out:
```json
{
 "@timestamp": "2021-05-27 03:03:01.745983 +00:00",
 "app_host_name": "app.example.com",
 "logger_name": "root",
 "level": "ERROR",
 "pathname": ".\\example.py",
 "lineno": 17,
 "func_name": "<module>",
 "thread_id": 30612,
 "thread_name": "MainThread",
 "process_id": 7356,
 "process_name": "MainProcess",
 "message": "hello world!",
 "tags": [
  "app=helloworld"
 ]
}
```