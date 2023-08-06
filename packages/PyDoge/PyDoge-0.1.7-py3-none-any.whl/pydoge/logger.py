import logging
import json
from pydoge.utils import concat


class Logger:
    def __init__(self, local=False):
        self.local = local
        if not local:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.INFO)
        self.logs = []
        
    def info(self, *message):
        msg = concat(message)
        if self.local:
            print(msg)
        else:
            self.logger.info(msg)
    
    def save_log(self, *message):
        msg = concat(message)
        self.logs.append(msg)

    def get_saved_log(self):
        return self.logs

    def dir(self, message, object, sort_keys=True, indent=2):
        self.info(
            message,
            json.dumps(object, sort_keys=sort_keys, indent=indent)
        )
