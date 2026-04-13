import logging
from pathlib import Path

'''
Create and return a configured logger

Features:
    - console logging
    - app file logging
    - error file logging
    - no duplicate handles
'''
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    '''get logger with specific name'''
    logger = logging.getLogger(name)

    '''
    logger.setLevel: set the lowest handling level for logger
    logger level:
        - DEBUG
        - INFO
        - WARNING
        - ERROR
        - CRITICAL
    '''
    logger.setLevel(logging.DEBUG)

    '''
    To avoid repeatedly allocate stream Channel, for this logger
    if true, means it's already allocate channel (handler), it will handler the msg as preassigned
    handler is like a specific channel to spread the msg
    only with handlers, it will handler the msg, not logger itself can do it
    so "return" here not means do not print, it's only represented do not repeatedly assign channel
    '''

    if logger.handlers:
        return logger
    
    logger.propagate = False
    formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )
    
    # Console handler: show Info and above msg
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler: save DEBUG and above to app.log
    app_file_handler = logging.FileHandler(
        LOG_DIR/"app.log",
        encoding="utf-8"
    )
    app_file_handler.setLevel(logging.DEBUG)
    app_file_handler.setFormatter(formatter)
    logger.addHandler(app_file_handler)

    # File handler: save ERROR and above to error.log
    error_file_handler = logging.FileHandler(
        LOG_DIR/"error.log",
        encoding="utf-8"
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)
    
    return logger                             