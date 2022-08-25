#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: log.py
# @Created:   2022-08-25 11:30:28
# @Modified:  2022-08-25 17:29:47

import os
import logging
import sublime

from typing import Dict, Optional, Literal
from datetime import datetime
from .consts import TIME_FORMAT_WITHOUT_DATE

_style = Literal["%", "{", "$"]


class Formatter(logging.Formatter):
    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: _style = "%",
        print_position=True,
    ):
        self.default_color = "{0}"
        self.print_position = print_position

        self.level_config: Dict[str, str] = {
            "DEBUG": "DEB",
            "INFO": "INF",
            "WARN": "WAR",
            "WARNING": "WAR",
            "ERROR": "ERR",
            "FATAL": "FAT",
            "CRITICAL": "FAT",
        }

        super().__init__(fmt, datefmt, style)

    def __level(self, levelname: str):
        level = self.level_config[levelname]

        return "[%s] " % level

    def __time(self, record):
        assert isinstance(self.datefmt, str)

        t = datetime.fromtimestamp(record.created)
        s = (
            t.strftime(self.datefmt)[:-3]
            if self.datefmt == TIME_FORMAT_WITHOUT_DATE
            else t.strftime(self.datefmt)
        )

        return s + " "

    def __name(self, record):
        return "" if record.name == "root" else f"{record.name}"

    def __position(self, record: logging.LogRecord):
        if not self.print_position:
            return ""

        if record.levelname in ["INFO"]:
            return ""

        return f":{record.lineno} "

    @property
    def __connector(self):
        return "- "

    def format(self, record: logging.LogRecord):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        msg = record.msg % record.args if record.args else record.msg

        s = (
            self.__time(record)
            + self.__level(record.levelname)
            + self.__name(record)
            + self.__position(record)
            + self.__connector
            + msg
        )

        return s


def log_level() -> int:
    """Get the log level.

    Returns `DEBUG` in debug mode, `INFO` otherwise.

    Returns:
        int: log level
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    print(current_path)
    print(sublime.installed_packages_path())
    return (
        logging.INFO
        if current_path.startswith(sublime.installed_packages_path())
        else logging.DEBUG
    )


def get_logger():
    """Get the root logger of the package.

    Use a custom Formatter to create a logger
    that is only valid for this package.

    Returns:
        Logger: the instance of `logging.Logger`
    """
    logger = logging.getLogger("python-docblockr")

    console_handler = logging.StreamHandler()
    fmt = Formatter(datefmt=TIME_FORMAT_WITHOUT_DATE, print_position=True)
    console_handler.setFormatter(fmt)

    logger.addHandler(console_handler)

    logger.setLevel(log_level())

    return logger


__logger = get_logger()


def child_logger(name: str) -> logging.Logger:
    """Get a new child logger with `name`.

    Args:
        name (str): the name of child logger

    Returns:
        Logger: the instance of `logging.Logger`
    """
    log = __logger.getChild(name.replace("python-docblockr.", ""))

    return log
