import logging
import logging.handlers

class LogHelper:
    def __init__(self, name, log_file):
        self.logger = logging.getLogger(name)
        self.logger.handlers = []  # 清空旧的 handler
        formatter = logging.Formatter("%(asctime)s [%(name)s][%(levelname)s] %(message)s")
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file, maxBytes=1024 * 1024 * 50, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

