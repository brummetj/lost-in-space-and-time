import logging
import pygogo as gogo

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)

logger = gogo.Gogo(
    'examples.fmt',
    low_hdlr=gogo.handlers.file_hdlr('custom_fmt.log'),
    low_formatter=formatter,
    high_level='error',
    high_formatter=formatter).logger

logger.info("yee")

class CommandManager:

    def __init__(self, path):
        logger.info("Command Manager Created with path")
        print('yo')
        self.path = path
