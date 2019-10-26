#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""


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

    def log(self, msg: str):
        """Log a message.
        :type msg: str
        """
        with open(self.file_path, "a+") as file_obj:
            file_obj.write("{}\n".format(msg))

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
