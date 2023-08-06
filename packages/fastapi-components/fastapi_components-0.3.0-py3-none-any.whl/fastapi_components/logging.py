import logging
import sys
from typing import Union

from loguru import logger
from pydantic import BaseModel


class InterceptLoguruHandler(logging.Handler):
    def __init__(self, stream: str = ""):
        del stream
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class LoggerSettings(BaseModel):
    json_enabled: bool = False
    level: str = "INFO"


def setup_logging(settings: LoggerSettings) -> None:
    logging.basicConfig(handlers=[InterceptLoguruHandler()], level=getattr(logging, settings.level))

    if settings.json_enabled:
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "serialize": True,
                    "colorize": False,
                    "level": settings.level,
                    "enqueue": True,
                    "backtrace": False,
                }
            ],
        )


class LoggerMixin:
    @property
    def logger(self) -> logging.Logger:
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(self.__class__.__name__)

        return self._logger
