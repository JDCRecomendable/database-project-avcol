#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.constants import Msg
from datetime import datetime


class Logger:
    def __init__(self, file_path: str):
        """Initialise a logger object to be able to log text.
        :type file_path: str
        """
        self.file_path = file_path
        try:
            open(self.file_path)
        except FileNotFoundError:
            open(self.file_path, "w+")

    def log(self, msg: str, symbol: str = ""):
        """Log text, with symbol for the text at the beginning of the text, if any.
        :type msg: str
        :type symbol: str
        """
        with open(self.file_path, "a+") as file_obj:
            if len(symbol) > 0:
                file_obj.write("{} [{}] {}\n".format(str(datetime.now()), symbol, msg))
            else:
                file_obj.write("{} {}\n".format(str(datetime.now()), msg))

    def log_message(self, msg: str):
        """Log a message, with the symbol for the message at the beginning of the message.
        :type msg: str
        """
        self.log(msg=msg, symbol=Msg.Symbol.message)

    def log_warning(self, msg: str):
        """Log a warning, with the symbol for the warning at the beginning of the warning.
        :type msg: str
        """
        self.log(msg=msg, symbol=Msg.Symbol.warning)

    def log_error(self, msg: str):
        """Log an error, with the symbol for the error at the beginning of the error.
        :type msg: str
        """
        self.log(msg=msg, symbol=Msg.Symbol.error)

    def trim(self, no_of_lines: int):
        """Trim the file to the specified number of lines. The earliest lines are deleted first.
        :type no_of_lines: int
        """
        with open(self.file_path) as file_obj:
            lines = file_obj.readlines()
        while len(lines) > no_of_lines:
            lines.pop(0)
        with open(self.file_path, "w") as file_obj:
            file_obj.writelines(lines)
