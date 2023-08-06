import json
import logging
from enum import Enum, unique
from typing import Optional


@unique
class OutFormatterStyle(Enum):
    JSON = "json"
    TEXT = "text"


class GenericFormatter(logging.Formatter):
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None, style: str = '%',
                 validate: bool = True, outfmtstyle: str = OutFormatterStyle.TEXT.value) -> None:
        """
        outfmtstyle: text or json, link to OutFormatterStyle
        """
        self.outfmtstyle = outfmtstyle
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if self.outfmtstyle != OutFormatterStyle.JSON.value or not self._fmt:
            return self.formatMessage(record)

        # Output format json structure
        # {"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "pathname": "%(pathname)s", "funcName": "%(funcName)s", "lineno": "%(lineno)d", "message": "%(message)s", "stack_trace": "%(exc_text)s"}'
        if not isinstance(self._style, (logging.PercentStyle, logging.StrFormatStyle)):
            raise ValueError("When the output structure is in JSON format, the style parameter can only be '%' or '{'.")

        log_fmt_dict = json.loads(self._fmt)
        json_msg = {}
        record_dict = record.__dict__
        for k, v in log_fmt_dict.items():
            json_msg[k] = v % record_dict if isinstance(self._style, logging.PercentStyle) else v.format(**record_dict)

        return json.dumps(json_msg)
