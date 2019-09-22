#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

import mysql.connector
from mysql.connector import errorcode
from base.utils import *


class DatabaseConnector:
    """Class to create an object that connects to a DBMS and executes queries there."""
    def __init__(self, database_config):
        self.cnx = None
        self.cursor = None
        self.db_is_connected = False
        self.username = database_config[Config.Keys.Database.username]
        self.password = database_config[Config.Keys.Database.password]
        self.host = database_config[Config.Keys.Database.host]

    def start_connection(self):
        try:
            print_message(Message.DatabaseConnector.connecting)
            self.cnx = mysql.connector.connect(
                user=self.username,
                password=self.password,
                host=self.host
            )
            self.cursor = self.cnx.cursor()
            self.db_is_connected = True
            print_message(Message.DatabaseConnector.connected)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print_error(Message.DatabaseConnector.invalid_database_credentials)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print_error(Message.DatabaseConnector.database_not_exists)
            else:
                print_error(str(err))
            exit(1)

    def execute_query(self, query, inputs=(), select=False, commit=False):
        """Execute a single SQL query. Optionally accepts a list or tuple of input parameters required by the query,
        and returns a list of tuples of data from the database if `select` is set to True.
        """
        if self.db_is_connected:
            statement = query
            if inputs:
                statement = statement.format(*inputs)
            try:
                self.cursor.execute(statement)
                print_message(Message.DatabaseConnector.command_processed + statement)
                if commit:
                    self.cnx.commit()
                if select:
                    return self.cursor.fetchall()
            except mysql.connector.Error as err:
                print_error(str(err))
                exit(1)
        else:
            print_error(Message.DatabaseConnector.not_connected)
            exit(1)

    def execute_queries_sequentially(self, queries):
        """Execute multiple SQL queries at the same time. Assumes that there is no input parameters."""
        if self.db_is_connected:
            try:
                statement = ""
                for query in queries:
                    if query.strip().startswith("--"):
                        continue
                    elif query.strip().endswith(";"):
                        statement += query.strip()
                        self.cursor.execute(statement)
                        print_message(Message.DatabaseConnector.command_processed + statement)
                        statement = ""
                    else:
                        statement += query.strip() + " "
                self.cnx.commit()
            except mysql.connector.Error as err:
                print_error(str(err))
                exit(1)

    def stop_connection(self):
        if self.db_is_connected:
            self.cursor.close()
            self.cnx.close()
            print_message(Message.DatabaseConnector.connection_stopped)
        else:
            print_error(Message.DatabaseConnector.not_connected)
