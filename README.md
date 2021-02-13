# Lambo

<!--[![pypi](https://img.shields.io/pypi/v/lambo?color=yellow&logo=python&logoColor=eee&style=flat-square)](https://pypi.org/project/lambo/)
[![python](https://img.shields.io/pypi/pyversions/lambo?logo=python&logoColor=eee&style=flat-square)](https://pypi.org/project/lambo/)-->
[![pytest](https://img.shields.io/github/workflow/status/amancevice/python-lambo/pytest?logo=github&style=flat-square)](https://github.com/amancevice/python-lambo/actions)
[![coverage](https://img.shields.io/codeclimate/coverage/amancevice/python-lambo?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/python-lambo/test_coverage)
[![maintainability](https://img.shields.io/codeclimate/maintainability/amancevice/python-lambo?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/python-lambo/maintainability)

Simple and visually pleasing logger for AWS Lambda.

## Installation

```bash
pip install lambo
```

## Usage

```python
import lambo

logger = lambo.getLogger(__name__)
logger.info('COLD START, NO REQUEST ID')


@logger.attach()
def handler(event, context):
    logger.info('HELLO!')
    return {'ok': True}
```

Yields…

```
INFO - COLD START, NO REQUEST ID
INFO RequestId: …  EVENT {"fizz": "buzz"}
INFO RequestId: …  TEST
INFO RequestId: …  RETURN {"ok": true}
```
