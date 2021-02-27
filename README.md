# Lambo

[![pypi](https://img.shields.io/pypi/v/lambo?color=yellow&logo=python&logoColor=eee&style=flat-square)](https://pypi.org/project/lambo/)
[![python](https://img.shields.io/pypi/pyversions/lambo?logo=python&logoColor=eee&style=flat-square)](https://pypi.org/project/lambo/)
[![pytest](https://img.shields.io/github/workflow/status/amancevice/python-lambo/pytest?logo=github&style=flat-square)](https://github.com/amancevice/python-lambo/actions)
[![coverage](https://img.shields.io/codeclimate/coverage/amancevice/python-lambo?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/python-lambo/test_coverage)
[![maintainability](https://img.shields.io/codeclimate/maintainability/amancevice/python-lambo?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/python-lambo/maintainability)

Simple and visually pleasing logger for AWS Lambda that prepends your log lines with the log level and the AWS request ID, making searching CLoudWatch for event logs a cinch!

Before installing lambo…

```
START RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149 Version: $LATEST
This log line was generated with ``print()``
END RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149
REPORT RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149	Duration: 3000.00 ms	Billed Duration: 3000 ms	Memory Size: 128 MB	Max Memory Used: 128 MB
```

After installing lambo…

```
START RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149 Version: $LATEST
DEBUG RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149 This log line was generated with ``logger.debug()``
INFO RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149 This log line was generated with ``logger.info()``
WARNING RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149 This log line was generated with ``logger.warning()``
ERROR RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149 This log line was generated with ``logger.error()``
END RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149
REPORT RequestId: 03cf3256-f2e1-461c-a4a0-60eb91ac8149	Duration: 3000.00 ms	Billed Duration: 3000 ms	Memory Size: 128 MB	Max Memory Used: 128 MB
```

## Installation

```bash
pip install lambo
```

## Usage

Create a logger using the `getLogger()` method and attach it to your Lambda handler functions with the `@attach` decorator.

```python
import lambo

logger = lambo.getLogger('my-logger')


@logger.attach
def handler(event, context):
    logger.info('HELLO!')
    return {'ok': True}
```

Or, if brevity is your thing, import the built-in logger:

```python
from lambo import logger

@logger.attach
def handler(event, context):
    logger.info('HELLO!')
    return {'ok': True}
```

## Customization

The default log level for lambo loggers is `INFO` and the default format string is `%(levelname)s %(awsRequestId)s %(message)s`, where `awsRequestId` is extracted from the Lambda execution context.

You can override these values at runtime…

```python
import lambo

logger = lambo.getLogger('my-logger', 'DEBUG', '%(message)s')
```

Or with ENV variables…

```bash
export LAMBO_LOG_LEVEL=DEBUG
export LAMBO_LOG_FORMAT="%(message)"
```
