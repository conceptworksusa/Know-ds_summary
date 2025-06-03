import sys
import uuid
import logging
import logging.config
from typing import Union
from pathlib import Path
from src.logger.conf import Configuration

class Logger:
    def __init__(self,
                 app_name: str,
                 log_folder_path: str,
                 log_format: str = Configuration.DEFAULT_LOG_FORMAT,
                 level: Union[int, str] = Configuration.DEFAULT_LOG_LEVEL,
                 stdout: bool = True):
        """
        This class is used to create a logger object for the application and save the log messages in a file.
        It does create a log file with the name of the application and a unique id for each run
        to avoid overwriting the log file.

        :param app_name: Name of the application
        :param log_folder_path: Path to save the log file
        :param log_format: Format of the log message
        :param level: Log level
        :param stdout: Print log message

        """
        self.app_name = app_name.replace(' ', '_')
        self.log_folder_path = Path(log_folder_path)
        self.log_format = log_format
        self.level = level
        self.stdout = stdout
        self.log = logging.getLogger(self.app_name)
        self.run_id = self.generate_run_id

    @property
    def generate_run_id(self):
        """
        Generate a unique id for each run of the application.
        This unique id will be used to create a unique log file and output messages with the unique id.

        return: Unique id for the run
        """
        return str(uuid.uuid5(uuid.uuid4(), self.app_name))

    def __set_logger(self, uid):
        """
        Set the logger with the given unique id.
        This private method set the file handler and stream handler for the logger.

        :param uid: Unique id for the run
        return: None

        """
        log_file = self.log_folder_path / f'{self.app_name}_{uid}.log'
        log_format_str = self.log_format

        # Prepare File Handlers
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format_str))
        self.log.addHandler(file_handler)

        # Prepare output stream handler
        if self.stdout:
            stdout_handler = logging.StreamHandler()
            stdout_handler.setFormatter(logging.Formatter(log_format_str))
            self.log.addHandler(stdout_handler)

        self.log.setLevel(self.level)

    def start(self):
        """
        Start the logger thread with the given application name and run id.
        return: None
        """
        self.__set_logger(self.run_id)
        self.log.info(f"Starting logger thread on {self.app_name}", extra={'run_id': self.run_id})

    def info(self, message):
        """
        Print the information message.
        """
        self.log.info(message, extra={'run_id': self.run_id})

    def debug(self, message):
        """
        Print the debug message.
        """
        self.log.debug(message, extra={'run_id': self.run_id})

    def error(self, message):
        """
        Print the error message.
        """
        self.log.error(message, extra={'run_id': self.run_id})

    def warning(self, message):
        """
        Print the warning message.
        """
        self.log.warning(message, extra={'run_id': self.run_id})

    def critical(self, message):
        """
        Print the critical message.
        """
        self.log.critical(message, extra={'run_id': self.run_id})

    def exception(self, message):
        """
        Print the exception message and exit the application.
        """
        self.log.exception(message, exc_info=True, extra={'run_id': self.run_id})

    def stop(self):
        """
        Stop the logger thread and shutdown the logger.
        """
        self.log.info(f"Stopping logger thread on {self.app_name}", extra={'run_id': self.run_id})
        self.log.handlers.clear()

