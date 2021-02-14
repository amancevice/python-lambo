from logging import Formatter
from textwrap import dedent
from types import SimpleNamespace

import pytest

import lambo

logger = lambo.getLogger(__name__)


@logger.attach
def handler(event=None, context=None):
    logger.warning('TEST')
    return {'ok': True}


class TestLogger:
    def setup(self):
        self.formatter = Formatter('%(levelname)s %(reqid)s %(message)s')

    @pytest.mark.parametrize(('event', 'context', 'reqid'), [
        (
            {'fizz': 'buzz'},
            SimpleNamespace(aws_request_id='<awsRequestId>'),
            'RequestId: <awsRequestId>'
        ),
        (
            {'fizz': 'buzz'},
            None,
            '-'
        ),
    ])
    def test_handler(self, caplog, event, context, reqid):
        caplog.handler.setFormatter(self.formatter)

        with caplog.at_level('DEBUG'):
            handler(event, context)
            logger.info('OUT OF CONTEXT')

        exp = dedent(f"""\
            INFO {reqid} EVENT {{"fizz": "buzz"}}
            WARNING {reqid} TEST
            INFO {reqid} RETURN {{"ok": true}}
            INFO - OUT OF CONTEXT
        """)
        assert caplog.text == exp
