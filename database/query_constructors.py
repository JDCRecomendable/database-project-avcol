#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.utils import *


class QueryConstructor:
    """Base class for constructing a query to be executed by the DBMS."""
    def __init__(self, table_name: str, schema_name: str = False):
        """Initialise the object. Optionally pass a schema name to the constructor.
        :type table_name: str
        :type schema_name: str
        """
        self.table_name = table_name
        self.schema_name = schema_name
        self.condition = ""

    def reset(self):
        """Clear the query in memory for this object. Essential before creating a new SQL query."""
        self.condition = ""

    def add_condition_exact_value(self, variable: str, value: str):
        """Add a condition to go along with the SQL query, where the value for the condition is a single fixed value.
        :type variable: str
        :type value: str
        """
        if self.condition:
            self._add_and()
        self.condition += '({} = "{}")'.format(variable, value)

    def add_condition_ranged_values(self, variable: str, lower_limit: str = "", upper_limit: str = ""):
        """Add a condition to go along with the SQL query, where there is a range of values for the variable in
        question.
        :type variable: str
        :type lower_limit: str
        :type upper_limit: str
        """
        if self.condition and (lower_limit or upper_limit):
            self._add_and()
        if not lower_limit and upper_limit:
            self.condition += '({} <= "{}")'.format(variable, upper_limit)
        elif not upper_limit and lower_limit:
            self.condition += '({} >= "{}")'.format(variable, lower_limit)
        elif lower_limit and upper_limit:
            self.condition += '({} BETWEEN "{}" AND "{}")'.format(variable, lower_limit, upper_limit)
        else:
            print_error(Message.DatabaseQueryConstructor.missing_ranged_values_limits)

    def add_condition_like(self, variable: str, like_value: str, at_beginning: bool = False, at_end: bool = False):
        """Add a condition to go along with the SQL query, where the value for the condition would be a subset
        of the full value.
        :type variable: str
        :type like_value: str
        :type at_beginning: bool
        :type at_end: bool
        """
        if self.condition:
            self._add_and()
        if not at_beginning and not at_end:
            like_value = "%" + like_value + "%"
        elif not at_end and at_beginning:
            like_value += "%"
        elif not at_beginning and at_end:
            like_value = "%" + like_value
        self.condition += '({} LIKE "{}")'.format(variable, like_value)

    def add_nested_query(self, variable: str, select_statement: str):
        """Add a select query as a nested query in the existing SQL query.
        :type variable: str
        :type select_statement: str
        """
        if self.condition:
            self._add_and()
        self.condition += '({} IN ({}))'.format(variable, select_statement)

    def _add_and(self):
        self.condition += " AND "


class SelectQueryConstructor(QueryConstructor):
    """Class for constructing a SELECT query to be executed by the DBMS."""
    def __init__(self, table_name: str, schema_name: str = False):
        """Initialise the object. Optionally pass a schema name to the constructor.
        :type table_name: str
        :type schema_name: str
        """
        super(SelectQueryConstructor, self).__init__(table_name, schema_name)
        self.elements_selection = ""

    def reset(self):
        """Clear the query in memory for this object. Essential before creating a new select SQL query."""
        super(SelectQueryConstructor, self).reset()
        self.elements_selection = ""

    def render(self) -> str:
        """Return the constructed select SQL query."""
        elements_selection = self.elements_selection
        schema_name = self.schema_name
        table_name = self.table_name
        condition = self.condition

        if len(table_name) == 0:
            print_error(Message.DatabaseQueryConstructor.missing_table_name)
            return ""

        if len(elements_selection) == 0:
            elements_selection = "*"

        if not schema_name:
            schema_name = ""
        else:
            schema_name += "."

        if len(condition) > 0:
            condition = "WHERE ({})".format(condition)

        return "SELECT {} FROM {}{} {}".format(
            elements_selection,
            schema_name,
            table_name,
            condition
        )

    def add_field(self, field: str):
        """Add a field for obtaining for the select SQL query.
        :type field: str
        """
        if self.elements_selection:
            self.elements_selection += ", "
        self.elements_selection += field

    def add_fields(self, field_list: list):
        """Add a series of fields for obtaining for the select SQL query.
        :type field_list: list
        """
        if not self.elements_selection:
            self.elements_selection += field_list[0]
        for i in range(1, len(field_list)):
            self.elements_selection += ", {}".format(field_list[i])


class UpdateQueryConstructor(QueryConstructor):
    """Class for constructing UPDATE queries to be executed by the DBMS."""
    def __init__(self, table_name: str, schema_name: str = False):
        """Initialise the object. Optionally pass a schema name to the constructor.
        :type table_name: str
        :type schema_name: str
        """
        super(UpdateQueryConstructor, self).__init__(table_name, schema_name)
        self.field_list = []
        self.value_list = []

    def reset(self):
        """Clear the query in memory for this object. Essential before creating a new update SQL query."""
        super(UpdateQueryConstructor, self).reset()
        self.field_list = []
        self.value_list = []

    def render(self) -> str:
        """Return the constructed SQL update query."""
        schema_name = self.schema_name
        table_name = self.table_name
        condition = self.condition

        if len(table_name) == 0:
            print_error(Message.DatabaseQueryConstructor.missing_table_name)
            return ""

        if len(self.field_list) == 0 or len(self.value_list) == 0:
            print_error(Message.DatabaseQueryConstructor.missing_fields_or_values)
            return ""

        if len(self.field_list) != len(self.value_list):
            print_error(Message.DatabaseQueryConstructor.number_of_field_and_value_mismatch)
            return ""

        if not schema_name:
            schema_name = ""
        else:
            schema_name += "."

        if len(condition) > 0:
            condition = "WHERE ({})".format(condition)

        set_result = "{} = {}".format(self.field_list[0], self.value_list[0])
        for i in range(1, len(self.field_list)):
            set_result += ", {} = {}".format(self.field_list[i], self.value_list[i])

        return "UPDATE {}{} SET {} {}".format(
            schema_name,
            table_name,
            set_result,
            condition
        )

    def add_field(self, field: str):
        """Add a field for updating for the update SQL query.
        :type field: str
        """
        self.field_list.append(field)

    def add_fields(self, field_list: list):
        """Add a series of fields for updating for the update SQL query.
        :type field_list: list
        """
        self.field_list += field_list

    def add_value(self, value: str):
        """Add a value to use in the update(s) for the update SQL query.
        :type value: str
        """
        self.value_list.append(value)

    def add_values(self, value_list: list):
        """Add a series of values to use in the update(s) for the update SQL query.
        :type value_list: list
        """
        self.value_list += value_list


class DeleteQueryConstructor(QueryConstructor):
    """Class for constructing DELETE FROM queries to be executed by the DBMS."""
    def __init__(self, table_name: str, schema_name: str = False):
        """Initialise the object. Optionally pass a schema name to the constructor.
        :type table_name: str
        :type schema_name: str
        """
        super(DeleteQueryConstructor, self).__init__(table_name, schema_name)

    def render(self) -> str:
        """Return the constructed SQL delete query."""
        schema_name = self.schema_name
        table_name = self.table_name
        condition = self.condition

        if len(self.table_name) == 0:
            print_error(Message.DatabaseQueryConstructor.missing_table_name)
            return ""

        if len(condition) == 0:
            print_error(Message.DatabaseQueryConstructor.cannot_render)
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
