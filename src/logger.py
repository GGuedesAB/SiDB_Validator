import logging

class Logger ():
    def __init__ (self):
        self.log_format = "%(asctime)s - %(levelname)s: %(message)s"
        self.date_format = '%d-%m-%Y %H:%M:%S'
        self.logger = logging.getLogger(__name__)

    def set_debug(self):
        logging.basicConfig(level=logging.DEBUG, format=self.log_format, datefmt=self.date_format)

    def set_info(self):
        logging.basicConfig(level=logging.INFO, format=self.log_format, datefmt=self.date_format)
	
    def set_warning(self):
        logging.basicConfig(level=logging.WARNING, format=self.log_format, datefmt=self.date_format)

    def error(self, msg):
        logging.error(msg)
    
    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)

if __name__ == "__main__":
    my_logger = Logger()
    my_logger.set_debug()
    my_logger.debug ('ohno')