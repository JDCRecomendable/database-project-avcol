#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.utils import *
from base.logger import Logger

logger = Logger(LoggerConfig.file_path)


class QueryConstructor:
    """Class for constructing a query to be executed by the DBMS. Specifically made with the goal to automate adding
    conditions using the WHERE clause in SQL
    """
    def __init__(self, table_name: str, schema_name: str = ""):
        """Initialise the object. Optionally pass a schema name to the constructor.
        :type table_name: str
        :type schema_name: str
        """
        self.table_name = table_name
        self.schema_name = schema_name
        self.field_list = []
        self.value_list = []
        self.condition = ""

    def reset(self):
        """Clear the query in memory for this object. Essential before creating a new query."""
        self.field_list.clear()
        self.value_list.clear()
        self.condition = ""

    # Adding Conditions
    def add_condition_exact_value(self, field: str, value: str):
        """Add a condition to go along with the SQL query, where the value for the condition is a single fixed value.
        :type field: str
        :type value: str
        """
        value = remove_unsafe_chars(value)

        if self.condition:
            self._add_and()
        self.condition += '({} = "{}")'.format(field, value)

    def add_condition_ranged_values(self, field: str, lower_limit: str = "", upper_limit: str = ""):
        """Add a condition to go along with the SQL query, where there is a range of values for the field in
        question.
        :type field: str
        :type lower_limit: str
        :type upper_limit: str
        """
        lower_limit = remove_unsafe_chars(lower_limit)
        upper_limit = remove_unsafe_chars(upper_limit)

        if self.condition and (lower_limit or upper_limit):
            self._add_and()
        if not lower_limit and upper_limit:
            self.condition += '({} <= "{}")'.format(field, upper_limit)
        elif not upper_limit and lower_limit:
            self.condition += '({} >= "{}")'.format(field, lower_limit)
        elif lower_limit and upper_limit:
            self.condition += '({} BETWEEN "{}" AND "{}")'.format(field, lower_limit, upper_limit)
        else:
            print_error(Msg.DatabaseQueryConstructor.missing_ranged_values_limits)
            logger.log_error(Msg.DatabaseQueryConstructor.missing_ranged_values_limits)

    def add_condition_like(self, field: str, like_value: str, at_beginning: bool = False, at_end: bool = False):
        """Add a condition to go along with the SQL query, where the value for the condition would be a subset
        of the full value.
        :type field: str
        :type like_value: str
        :type at_beginning: bool
        :type at_end: bool
        """
        like_value = remove_unsafe_chars(like_value)

        if self.condition:
            self._add_and()
        if not at_beginning and not at_end:
            like_value = "%" + like_value + "%"
        elif not at_end and at_beginning:
            like_value += "%"
        elif not at_beginning and at_end:
            like_value = "%" + like_value
        self.condition += '({} LIKE "{}")'.format(field, like_value)

    def add_nested_query(self, field: str, select_statement: str):
        """Add a select query as a nested query in the existing SQL query.
        :type field: str
        :type select_statement: str
        """
        if self.condition:
            self._add_and()
        self.condition += '({} IN ({}))'.format(field, select_statement)

    def _add_and(self):
        self.condition += " AND "

    # Adding Fields and Values
    def add_field(self, field: str):
        """Add a field to the query."""
        self.field_list.append(field)

    def add_value(self, value: str):
        """Add a value to the query."""
        self.value_list.append(remove_unsafe_chars(value))

    def add_field_and_value(self, field: str, value: str):
        """Add a field and a value to the query."""
        self.add_field(field)
        self.add_value(value)

    # Rendering the Queries
    def render_select_query(self) -> str:
        """Return constructed select SQL query."""
        schema_name = self.schema_name
        table_name = self.table_name
        condition = self.condition

        if len(table_name) == 0:
            print_error(Msg.DatabaseQueryConstructor.missing_table_name)
            logger.log_error(Msg.DatabaseQueryConstructor.missing_table_name)
            return ""

        if not schema_name:
            schema_name = ""
        else:
            schema_name += "."

        if len(self.field_list) == 0:
            fields = "*"
        else:
            fields = self.field_list[0]
            for i in range(1, len(self.field_list)):
                fields += ", {}".format(self.field_list[i])

        if len(condition) > 0:
            condition = "WHERE ({})".format(condition)

        return "SELECT {} FROM {}{} {}".format(
            fields,
            schema_name,
            table_name,
            condition
        )

    def render_update_query(self) -> str:
        """Return constructed update SQL query."""
        fields = self.field_list
        values = self.value_list
        schema_name = self.schema_name
        table_name = self.table_name
        condition = self.condition

        if len(table_name) == 0:
            print_error(Msg.DatabaseQueryConstructor.missing_table_name)
            logger.log_error(Msg.DatabaseQueryConstructor.missing_table_name)
            return ""

        if len(fields) == 0 or len(values) == 0:
            print_error(Msg.DatabaseQueryConstructor.missing_fields_or_values)
            logger.log_error(Msg.DatabaseQueryConstructor.missing_fields_or_values)
            return ""

        if len(fields) != len(values):
            print_error(Msg.DatabaseQueryConstructor.number_of_field_and_value_mismatch)
            logger.log_error(Msg.DatabaseQueryConstructor.number_of_field_and_value_mismatch)
            return ""

        if not schema_name:
            schema_name = ""
        else:
            schema_name += "."

        if len(condition) > 0:
            condition = "WHERE ({})".format(condition)

        set_result = '{}="{}",'.format(fields[0], values[0])
        for i in range(1, len(fields) - 1):
            set_result += ' {}="{}",'.format(fields[i], values[i])
        set_result += ' {}="{}"'.format(fields[len(fields) - 1], values[len(fields) - 1])

        return "UPDATE {}{} SET {} {}".format(
            schema_name,
            table_name,
            set_result,
            condition
        )

    def render_delete_query(self) -> str:
        """Return constructed delete SQL query."""
        schema_name = self.schema_name
        table_name = self.table_name
        condition = self.condition

        if len(table_name) == 0:
            print_error(Msg.DatabaseQueryConstructor.missing_table_name)
            logger.log_error(Msg.DatabaseQueryConstructor.missing_table_name)
            return ""

        if len(condition) == 0:
            print_error(Msg.DatabaseQueryConstructor.cannot_render)
            logger.log_error(Msg.DatabaseQueryConstructor.cannot_render)
            return ""

        if not schema_name:
            schema_name = ""
        else:
            schema_name += "."

        if len(condition) > 0:
            condition = "WHERE ({})".format(condition)

        return "DELETE FROM {}{} {}".format(
            schema_name,
            table_name,
            condition
        )
