import logging
import threading 
import os
logger_lock = threading.Lock()

is_running_in_lambda = 'AWS_LAMBDA_FUNCTION_NAME' in os.environ
current_dir = os.getcwd()


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if is_running_in_lambda:
            record.msg = str(record.msg).replace("\n", "\r")
        relative_path = os.path.relpath(record.pathname, current_dir)
        record.relativePathName = relative_path
        return super().format(record)


class Logger:
    logger_map = {}
    @classmethod
    def _get_logger(
        cls,
        name,
        level=int(os.environ.get('DEBUG_LEVEL',logging.INFO)),
        format='%(asctime)s [%(levelname)s] %(relativePathName)s:%(lineno)d %(funcName)s() %(message)s',
        ):
        if name in cls.logger_map:
            return cls.logger_map[name]
        logger = logging.getLogger(name)
        logger.propagate = 0
        # Create a handler
        c_handler = logging.StreamHandler()
        formatter = CustomFormatter(format)
        c_handler.setFormatter(formatter)
        logger.addHandler(c_handler)
        logger.setLevel(level) 

        cls.logger_map[name] = logger
        return logger
    
    @classmethod
    def get_logger(
        cls,
        *args,
        **kwargs
        ):
        with logger_lock:
            return cls._get_logger(*args,**kwargs)
    
get_logger = Logger.get_logger