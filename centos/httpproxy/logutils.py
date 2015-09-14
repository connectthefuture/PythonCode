#coding=gbk
import logging, sys, os

_LogNames = []


class iLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None):
        #if self.logtyp == 'A':
        #    inst = args[0]
        #    if not extra:
        #        extra = dict()
        #    extra = {'serialno': inst.getattr("serialno")}
        #    args = args[1:]
        logging.Logger._log(self, level, msg, args, exc_info, extra)


logging.setLoggerClass(iLogger)


def getlogger(logname, formatter=None):
    logdir = os.path.join(os.getenv("HOME"), "log")
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    if logname in iLogger.manager.loggerDict:
        return logging.getLogger(logname)
    logger = logging.getLogger(logname)
    if not formatter:
        formatter = logging.Formatter('[%(levelname)-8s][%(filename)-20s%(lineno)06d][%(message)s]')
    fileHandler = logging.FileHandler(os.path.join(logdir, logname + ".log"))
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    logger = getlogger("hello.world", "S")
    logger.debug("yoo")

