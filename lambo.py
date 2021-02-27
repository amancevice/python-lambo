import json
import logging
import os

LOG_LEVEL = os.getenv('LAMBO_LOG_LEVEL') or logging.INFO
LOG_FORMAT = os.getenv('LAMBO_LOG_FORMAT') \
    or '%(levelname)s %(awsRequestId)s %(message)s'


class SuppressFilter(logging.Filter):
    """
    Suppress Log Records from registered logger

    Taken from ``aws_lambda_powertools.logging.filters.SuppressFilter``
    """
    def __init__(self, logger):
        self.logger = logger

    def filter(self, record):
        logger = record.name
        return False if self.logger in logger else True


class LambdaLoggerAdapter(logging.LoggerAdapter):
    """
    Lambda logger adapter.
    """
    def __init__(self, name, level=None, format_string=None):
        # Get logger, formatter
        logger = logging.getLogger(name)

        # Set log level
        logger.setLevel(level or LOG_LEVEL)

        # Set handler if necessary
        if not logger.handlers:  # and not logger.parent.handlers:
            formatter = logging.Formatter(format_string or LOG_FORMAT)
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Suppress AWS logging for this logger
        for handler in logging.root.handlers:
            logFilter = SuppressFilter(name)
            handler.addFilter(logFilter)

        # Initialize adapter with null RequestId
        super().__init__(logger, dict(awsRequestId='-'))

    def attach(self, handler):
        """
        Decorate Lambda handler to attach logger to AWS request.

        :Example:

        >>> logger = lambo.getLogger(__name__)
        >>>
        >>> @logger.attach
        ... def handler(event, context):
        ...     logger.info('Hello, world!')
        ...     return {'ok': True}
        ...
        >>> handler({'fizz': 'buzz'})
        >>> # => INFO RequestId: {awsRequestId} EVENT {"fizz": "buzz"}
        >>> # => INFO RequestId: {awsRequestId} Hello, world!
        >>> # => INFO RequestId: {awsRequestId} RETURN {"ok": True}
        """
        def wrapper(event=None, context=None):
            try:
                self.addContext(context)
                self.info('EVENT %s', json.dumps(event, default=str))
                result = handler(event, context)
                self.info('RETURN %s', json.dumps(result, default=str))
                return result
            finally:
                self.dropContext()
        return wrapper

    def addContext(self, context=None):
        """
        Add runtime context to logger.
        """
        try:
            awsRequestId = f'RequestId: {context.aws_request_id}'
        except AttributeError:
            awsRequestId = '-'
        self.extra.update(awsRequestId=awsRequestId)
        return self

    def dropContext(self):
        """
        Drop runtime context from logger.
        """
        self.extra.update(awsRequestId='-')
        return self


def getLogger(name, level=None, format_string=None):
    """
    Helper to get Lambda logger.

    :Example:

    >>> getLogger('logger-name', 'DEBUG', '%(message)s')
    """
    return LambdaLoggerAdapter(name, level, format_string)


logger = getLogger(__name__)
