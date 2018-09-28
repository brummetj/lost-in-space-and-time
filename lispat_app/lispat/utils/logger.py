import logging
import sys
from logging.handlers import TimedRotatingFileHandler
class Logger:
   def __init__(self, logger_name):
      self.FORMATTER = logging.Formatter("%(filename)s:%(lineno)s — %(name)s - %(threadName)s - %(funcName)s() — %(levelname)s — %(message)s")
      self.LOG_FILE = "lispat_app.log"
      self.logger = logging.getLogger(logger_name)
      self.logger.setLevel(logging.DEBUG) # better to have too much log than not enough
      self.logger.addHandler(self.get_console_handler())
      self.logger.addHandler(self.get_file_handler())
      # with this pattern, it's rarely necessary to propagate the error up to parent
      self.logger.propagate = False

   def get_console_handler(self):
      self.console_handler = logging.StreamHandler(sys.stdout)
      self.console_handler.setFormatter(self.FORMATTER)
      return self.console_handler

   def getLogger(self):
      return self.logger

   def get_file_handler(self):
      self.file_handler = TimedRotatingFileHandler(self.LOG_FILE, when='midnight')
      self.file_handler.setFormatter(self.FORMATTER)
      return self.file_handler
