import logging

logger = logging.getLogger(__name__)

class _log():
    __default_lvl = [0,10,20,30,40,50]
    # redirect to log
    @classmethod
    def log(self, msg):
        logger.log(self.__default_lvl[1],msg)

    # redirect to info
    @classmethod
    def info(self, msg):
        logger.info(msg)

    # redirect to debug
    @classmethod
    def debug(self, msg):
        logger.debug(msg)

    # redirect to warning
    @classmethod
    def warning(self, msg):
        logger.warning(msg)

def log_test(msg):
    logger.debug(msg)
