from io import StringIO
from textwrap import dedent
from types import SimpleNamespace

import pytest

import lambo


class TestLogger:
    def setup(self):
        self.stream = StringIO()

    @pytest.mark.parametrize(('event', 'context', 'name', 'awsRequestId'), [
        (
            {'fizz': 'buzz'},
            SimpleNamespace(aws_request_id='<awsRequestId>'),
            'lambda',
            'RequestId: <awsRequestId>'
        ),
        (
            {'fizz': 'buzz'},
            None,
            'local',
            '-'
        ),
    ])
    def test_bind(self, event, context, name, awsRequestId):
        logger = lambo.getLogger(name, stream=self.stream)
        logger.setLevel('DEBUG')

        @logger.bind
        def handler(event=None, context=None):
            logger.warning('TEST')
            return {'ok': True}

        logger.debug('BEFORE CONTEXT')
        handler(event, context)
        logger.debug('AFTER CONTEXT')

        exp = dedent(f"""\
            DEBUG - BEFORE CONTEXT
            INFO {awsRequestId} EVENT {{
              "fizz": "buzz"
            }}
            WARNING {awsRequestId} TEST
            INFO {awsRequestId} RETURN {{
              "ok": true
            }}
            DEBUG - AFTER CONTEXT
        """)
        self.stream.seek(0)
        ret = self.stream.read()
        assert ret == exp
