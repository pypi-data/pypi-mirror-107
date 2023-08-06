import logging
from typing import Optional

from celery._state import get_current_task

from pylogformatter.generic import GenericFormatter, OutFormatterStyle


class CeleryTaskFormatter(GenericFormatter):
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None, style: str = '%',
                 validate: bool = True, outfmtstyle: str = OutFormatterStyle.TEXT.value,
                 protected_origin: bool = True) -> None:
        self.protected_origin = protected_origin
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate, outfmtstyle=outfmtstyle)

    def format(self, record: logging.LogRecord) -> str:
        task = get_current_task()
        if task and task.request:
            record.__dict__.update(task_id=task.request.id, task_name=task.name)
        else:
            record.__dict__.setdefault('task_name', '???')
            record.__dict__.setdefault('task_id', '???')
        return super().format(record)
