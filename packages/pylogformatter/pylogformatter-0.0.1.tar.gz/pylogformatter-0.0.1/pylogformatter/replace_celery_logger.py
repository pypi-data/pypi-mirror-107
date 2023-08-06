import copy
import logging
from typing import List

from celery.signals import after_setup_logger, after_setup_task_logger

from pylogformatter.generic import OutFormatterStyle
from pylogformatter.celery import CeleryTaskFormatter


def reset_celery_logger_formatter(fmt: logging.Formatter = None):
    if fmt is None:
        fmt = CeleryTaskFormatter(outfmtstyle=OutFormatterStyle.JSON.value)
    _formatter_controller(fmt)


class _replaceformatter:
    def __init__(self, fmt: logging.Formatter = None) -> None:
        self.fmt = fmt if fmt else CeleryTaskFormatter(outfmtstyle=OutFormatterStyle.TEXT.value)
        self._loggers: List[logging.Logger] = []
        self._is_replaced: bool = False

    def __call__(self, fmt: logging.Formatter) -> '_replaceformatter':
        self.fmt = fmt
        if self._is_replaced:
            for logger in self._loggers:
                _replace_logger_formatter(logger=logger, fmt=self.fmt)
        return self

    def add_logger(self, logger: logging.Logger) -> None:
        self._loggers.append(logger)

    def mark_replaced(self, is_replaced: bool = True):
        self._is_replaced = is_replaced


_formatter_controller = _replaceformatter()


@after_setup_logger.connect
@after_setup_task_logger.connect
def receive_celery_setup_logger_signal(logger: logging.Logger, *args, **kwargs):
    fmt = _formatter_controller.fmt
    _formatter_controller.add_logger(logger=logger)
    _replace_logger_formatter(logger=logger, fmt=fmt)
    _formatter_controller.mark_replaced()


def _replace_logger_formatter(logger: logging.Logger, fmt: logging.Formatter):
    for h in logger.handlers:
        if h is None:
            continue
        if h.formatter is None:
            continue
        if getattr(fmt, "protected_origin", False):
            copy_fmt = copy.copy(fmt)
            copy_fmt.datefmt = h.formatter.datefmt
            copy_fmt._style = h.formatter._style
            copy_fmt._fmt = h.formatter._fmt
            h.setFormatter(copy_fmt)
        else:
            h.setFormatter(fmt)
