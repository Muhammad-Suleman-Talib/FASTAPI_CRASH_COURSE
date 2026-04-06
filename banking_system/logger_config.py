import logging
import logging.config
from math import log
import sys
import os
import json
from datetime import date


class Bank_logger():
  """professional logger for banking system"""
  def __init__(self):
    self.env = os.getenv("ENV","development")
    self.log_level = os.getenv("LOG_LEVEL","DEBUG")
    self.setup_logging()


  def setup_logging(self):

    os.makedirs("logs",exist_ok=True)

    class Sensitive_fileter(logging.Filter):

      def filter(self,record):
        if hasattr(record,"msg"):
          msg = record.msg
          if "account_number" in msg:
            import re
            msg = re.sub(r"\d{8,}","****_****_****",str(msg))
            record.msg = msg

        return True

    if self.env == "production":
      config = self.deployment_configration()
    else:
      config = self.deployment_configration()


    for handler in config['handlers'].values():
      if "filters" not in handler:
        handler["filters"] = ["sensitive"]

    config["filters"] = {
      "sensitive":{
        "()":Sensitive_fileter
      }
    }

    logging.config.dictConfig(config)

    filter_obj = Sensitive_fileter()

    for handler in logging.root.handlers:
      handler.addFilter(filter_obj)
      print(f"Added Sensitive_fileter to handler {filter_obj}")

    self.bank_logger = logging.getLogger("banking")
    self.transaction_logger = logging.getLogger("transaction")
    self.security_logger = logging.getLogger("security")
    self.error_logger = logging.getLogger("errors")

    for logger_name in ["banking","transaction","security","errors"]:
      logger = logging.getLogger(logger_name)
      logger.addFilter(filter_obj)

  def deployment_configration(self):
    """Deployment configration for next level make your self super strong ok """
    return {
      "version":1,
      "disable_existing_loggers":False,
      "formatters":{
        "detailed":{
          'format':"%(asctime)s -| %(name)s -| %(levelname)s  -| %(filename)s:%(lineno)d- %(funcName)s -| %(message)s",
          "datefmt":"%Y-%m-%d %H:%M:%S",
        },

        'colored':{
          "()":"colorlog.ColoredFormatter",
          "format":"%(log_color)s%(asctime)s [%(levelname)s] %(message)s%(reset)s",
          "datefmt":"%Y-%m-%d %H:%M:%S",

        },
        'simple':{
            "format":"%(asctime)s - %(name)s - %(levelname)s %(message)s "
          },

      },
      'handlers':{
          "console":{
            "class":"logging.StreamHandler",
            "level":"DEBUG",
            "formatter":"colored",
            "stream":sys.stdout
          },
          "file_banking":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"DEBUG",
            "formatter":"detailed",
            "filename":"logs/banking.log",
            "maxBytes":5_000_000,
            "backupCount":5,
            "encoding":"utf-8"
          },
          "file_errors":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"ERROR",
            "formatter":"detailed",
            "filename":"logs/errors.log",
            "maxBytes":5_000_000,
            "backupCount":10,
            "encoding":"utf-8",

          },
          "file_transactions":{
            "class":"logging.handlers.TimedRotatingFileHandler",
            "level":"DEBUG",
            "formatter":"simple",
            "filename":"logs/transaction.log",
            "when":"midnight",
            "backupCount":30,
            "encoding":"utf-8"
          }
        },
        "loggers":{
          "banking":{
            "handlers":['console','file_banking'],
            "level":"DEBUG",
            "propagate":False
          },
          "transaction":{
            "handlers":['file_transactions'],
            "level":"INFO",
            "propagate":False,
          },
          "security":{
            "handlers":['console','file_banking'],
            "level":"INFO",
            "propagate":False
          },
          "errors":{
            "handlers":["file_errors"],
            "level":"ERROR",
            "propagate":False

          }

        },
        "root":{
          "level":"WARNING",
          "handlers":["console"]
        }

    }



  def prodcution_configration(self):
    pass

  def get_logger(self,name):
    return logging.getLogger(name)


bank_logger = Bank_logger()

logger = bank_logger.get_logger("banking")
transaction_logger = bank_logger.get_logger("transaction")
security_logger = bank_logger.get_logger("security")
error_logger = bank_logger.get_logger("errors")
