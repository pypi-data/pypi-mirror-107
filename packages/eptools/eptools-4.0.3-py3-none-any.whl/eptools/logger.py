import logging
from logging.handlers import RotatingFileHandler
from .slacker import Slacker
import os
from inspect import getframeinfo, stack
import traceback

#_svc_name_ = "..."
#log_path = C:\\logs\\pythonservice\\

eformat = logging.Formatter('%(asctime)s,%(msecs)d - %(levelname)s - %(message)s')
# iformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s - (in %(funcName)s)')
iformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def createLogger(name, log_path, level=logging.DEBUG, normal_format=iformat, error_format=eformat):
    handler = logging.FileHandler(os.path.join(log_path, 'info.log'))
    debug_handler = logging.FileHandler(
        os.path.join(log_path, 'debug.log'))
    error_handler = logging.FileHandler(
        os.path.join(log_path, 'error.log'))
    handler.setFormatter(normal_format)
    debug_handler.setFormatter(normal_format)
    error_handler.setFormatter(error_format)
    handler.setLevel(logging.INFO)
    debug_handler.setLevel(logging.DEBUG)
    error_handler.setLevel(logging.ERROR)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    return logger


def createRotatingLogger(name, log_path, level=logging.DEBUG, normal_format = iformat, error_format = eformat):
    handler = RotatingFileHandler(os.path.join(log_path , 'info.log'),backupCount=20,maxBytes=10000000)
    debug_handler = RotatingFileHandler(os.path.join(log_path , 'debug.log'),backupCount=20,maxBytes=10000000)
    error_handler = RotatingFileHandler(os.path.join(log_path , 'error.log'),backupCount=20,maxBytes=10000000)
    handler.setFormatter(normal_format)
    debug_handler.setFormatter(normal_format)
    error_handler.setFormatter(error_format)
    handler.setLevel(logging.INFO)
    debug_handler.setLevel(logging.DEBUG)
    error_handler.setLevel(logging.ERROR)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    return logger

def createSlackLogger(name, logger = None):
    slacker = Slacker()
    try:
        slacker.setup(name, logger=logger)
    except Exception as ex:
        print(ex)
    return slacker


class EasyPostLogger():
    """ 
    Wrapper class for logging.

    Allows to log to following outputs:
    - console
    - file log
    - slack log

    params
    ----
    name
        If name is passed, it will setup a file logger and slack logger by default
    If 
    """
    def __init__(self, name: str=None) -> None:
        self.file_logger = None
        self.slack_logger = Slacker() 
        if name:
            self._svc_logger_ = name + '_logger'
            self._svc_logpath_ = 'C:\\logs\\' + name + '\\'
            self.file_logger = createRotatingLogger(self._svc_logger_ , self._svc_logpath_)
            self.slack_logger = createSlackLogger(name,logger=self.file_logger)
        self.slacker_level = logging.WARNING

    def set_file_logger(self, file_logger):
        self.file_logger = file_logger

    def set_slack_logger(self, slack_logger: Slacker):
        """ Sets slack logger instance. """
        self.slack_logger = slack_logger

    def set_slack_level(self, log_level: int):
        """ Sets minimum loglevel which is written to slack. """
        self.slacker_level = log_level

    def __overall__(self, msg: str, level: int):
        caller = getframeinfo(stack()[2][0])
        msg = f"{msg} - (in \"{caller.function}()\" at path \"{caller.filename}\" at line {caller.lineno})"
        if self.file_logger:
            # log to file logger with correct loglevel
            if level == logging.DEBUG: 
                self.file_logger.debug(msg)
            elif level == logging.INFO: 
                self.file_logger.info(msg)
            elif level == logging.WARNING: 
                self.file_logger.warning(msg)
            elif level == logging.ERROR: 
                self.file_logger.error(msg)
            elif level == logging.CRITICAL: 
                self.file_logger.critical(msg)
        else:
            # If no file logger is added, prints to console
            print(msg)

        if self.slack_logger:
            if self.slacker_level <= level:
                self.slack_logger.log(msg)

    def debug(self, msg: str):
        self.__overall__(msg=msg,level = logging.DEBUG)

    def info(self, msg: str):
        self.__overall__(msg=msg,level = logging.INFO)

    def warning(self, msg: str, ex: Exception = None):
        """ Prints warning log. """
        self.__overall__(msg=msg, level = logging.WARNING)

    def warning_with_exception(self, msg: str, ex: Exception = None):
        """ 
        Prints warning log. 
        
        Params:
        ----
        msg: 
            message to log. Can be message or context in case an exception is passed as second param
        ex:
            Optional exception. 
            Appends the stacktrace of the exception to the msg param. 
        """

        error_msg = msg        
        if ex:
            error_msg += "\n" + str(ex)

        self.__overall__(msg=error_msg,level = logging.WARNING)

    def error(self, msg=None, ex: Exception= None):
        error_msg = ""
        
        if ex:
            if msg:
                error_msg = msg + " \n "
            error_msg += self.get_exception_with_stacktrace(ex)
            error_msg += "\n" + type(ex).__name__
        else:
            if msg:
                error_msg = msg
        if len(error_msg) < 1:
            error_msg = "Error withouth info occured"
        self.__overall__(msg=error_msg,level = logging.ERROR)

    
    def critical(self, msg=None, ex: Exception= None):
        error_msg = ""
        
        if ex:
            if msg:
                error_msg = msg + " \n "
            error_msg += self.get_exception_with_stacktrace(ex)
            error_msg += "\n" + type(ex).__name__
        else:
            if msg:
                error_msg = msg
        if len(error_msg) < 1:
            error_msg = "Error withouth info occured"
        self.__overall__(msg=error_msg,level =logging.CRITICAL)

    def get_exception_with_stacktrace(self, ex):
        """ Gets the stacktrace of an exception. """
        # Reference: https://stackoverflow.com/a/4564595/15657263
        error_msg = str(ex)
        tb = traceback.format_exc()
        error_msg += "\n" + tb
        return error_msg


def test_code():
    # Setup logging
    logger = EasyPostLogger()
    slack_logger = createSlackLogger("EPTools-slacker-logger")
    logger.debug("test")
    logger.set_slack_level(logging.ERROR)
    logger.set_slack_logger(slack_logger)

    # Run demo exception which gets caught
    try:
        raise ValueError("I'm an ValueError Exception. Wiehoewiehoe toetatoeta. I will be the last test exception of today. Sorry for disturbing.")
    except Exception as ex:
        logger.warning_with_exception("I'm a test exception that should not happen", ex)
        logger.error(ex)

if __name__ == '__main__':
    test_code()