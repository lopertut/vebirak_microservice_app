import logging
import os
from pydantic import BaseModel


class LoggerConfig(BaseModel):
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    log_dir: str = os.path.join(base_dir, "logs")
    log_file: str = os.path.join(log_dir, "ai-service.log")
    level: int = logging.INFO
    format: str = "%(asctime)s [%(levelname)s] %(message)s"


class Logger:
    def __init__(self, config: LoggerConfig = LoggerConfig()):
        self.config = config
        os.makedirs(self.config.log_dir, exist_ok=True)
        logging.basicConfig(
            level=self.config.level,
            format=self.config.format,
            handlers=[
                logging.FileHandler(self.config.log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )


Logger()