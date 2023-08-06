from logging import getLogger
from logging import config
from os import path
from os import makedirs
from os import getcwd

class gt_logger():
    
    def __init__(self, name, log_path=None):
        """Initialises the logger object"""
        if not path.exists(path.join(getcwd(), "logs")):
            if log_path:
                makedirs(path.join(log_path, "logs"))
            else:
                makedirs(path.join(getcwd(), "logs"))
        this_dir, this_filename = path.split(__file__)
        CONF_PATH = path.join(this_dir, "logging.conf")
        config.fileConfig(CONF_PATH)
        self.name = name
        self.glogger = getLogger(self.name)
        
    def write_to_log(self, error_msg, error_type='C'):
        """Writes the error message to log"""
        if error_type == 'D':
            self.glogger.debug(error_msg)
        elif error_type == 'I':
            self.glogger.info(error_msg)
        elif error_type == 'W':
            self.glogger.warning(error_msg)
        elif error_type == 'E':
            self.glogger.error(error_msg)
        else:	
            self.glogger.critical(error_msg)
