# coding=gbk
import logging, sys
import os

_LogNames = []

LOGBASE = "E:\\AppTmp\\log"


class iLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None):
        if self.logtyp == 'A':
            inst = args[0]
            if not extra:
                extra = dict()
            extra = {'serialno': inst.runEnv.get("totalruncount", 0)}
            args = args[1:]
        logging.Logger._log(self, level, msg, args, exc_info, extra)


logging.setLoggerClass(iLogger)


def getlogger(logname, logtyp='A'):
    if logname in iLogger.manager.loggerDict:
        return logging.getLogger(logname)
    logger = logging.getLogger(logname)
    logger.logtyp = logtyp
    if logtyp == 'A':
        formatter = logging.Formatter('[%(levelname)-8s][%(filename)-20s%(lineno)06d][%(serialno)010d][%(message)s]')
    elif logtyp == 'S':
        formatter = logging.Formatter('[%(levelname)-8s][%(filename)-20s%(lineno)06d][%(message)s]')
    logfile = os.path.join(LOGBASE, logname + '.log')
    streamHandler = logging.FileHandler(logfile)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    logger = getlogger("helloworld", "S")
    logger.debug("yoo")
