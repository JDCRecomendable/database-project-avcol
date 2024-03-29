#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.constants import *
from configparser import ConfigParser


def print_message(message: str):
    print("[{}] {}".format(Msg.Symbol.message, message))


def print_warning(message: str):
    print("[{}] {}".format(Msg.Symbol.warning, message))


def print_error(message: str):
    print("[{}] {}".format(Msg.Symbol.error, message))


def check_if_config_exists(file_path: str) -> bool:
    config = ConfigParser()
    return config.read(file_path)


def read_config(file_path: str) -> ConfigParser:
    config = ConfigParser()
    config.read(file_path)
    return config


def get_text_file_lines_as_single_line(file_path: str, separation_char: str = " ") -> str:
    """Return a string containing all lines in a text file, separated by the separation character.
    :type file_path: str:
    :type separation_char: str
    """
    query_obj = open(file_path)
    lines = query_obj.readlines()
    query_obj.close()
    result = ""
    for line in lines:
        result += line.strip() + separation_char
    return result


def get_text_file_lines(file_path: str) -> list:
    """Return a list containing all lines in a text file.
    :type file_path: str"""
    query_obj = open(file_path)
    result = query_obj.readlines()
    query_obj.close()
    return result


def format_text_file_lines(text_file_lines: list, **kwargs) -> list:
    """Return a list containing the lines, formatted.
    :type text_file_lines: list
    """
    result = []
    for line in text_file_lines:
        result.append(line.format(**kwargs))
    return result


def remove_unsafe_chars(string: str) -> str:
    """Remove unsafe characters from the string that will be used for SQL queries.
    :type string: str
    :rtype: str
    """
    for char in UNSAFE_QUERY_CHARS:
        string = string.replace(char, " ")
    return string
