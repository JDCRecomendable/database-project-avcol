#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.utils import *
from base.logger import Logger
from database import connector

logger = Logger(LoggerConfig.file_path)
logger.trim(LoggerConfig.log_size)

# If configuration exists, read it. Else, make one for editing by the user.
config = read_config(Config.file_path)
config_exists = check_if_config_exists(Config.file_path)
if not config_exists:
    config[Config.Headers.system] = Config.DefaultKeyValuePairs.system
    config[Config.Headers.database] = Config.DefaultKeyValuePairs.database
    config[Config.Headers.web_interface] = Config.DefaultKeyValuePairs.web_interface
    with open(Config.file_path, "w+", newline=Config.newline_char) as config_file:
        config.write(config_file)
    print(Msg.Config.initialised)
    exit(0)
else:
    print_message(Msg.Config.configuration_read)
    logger.log_message(Msg.Config.configuration_read)

DBSchemaTableNames.schema = config[Config.Headers.database][Config.Keys.Database.schema]
import webfrontend


def add_sample_data(query_file_path, data_source_file_path, db_connector):
    query = get_text_file_lines_as_single_line(query_file_path)
    for line in get_text_file_lines(data_source_file_path):
        line = line.strip()
        line_elements = line.split(";")
        db_connector.execute_query(
            query.format(DBSchemaTableNames.schema, *line_elements),
            commit=True
        )


def main_activity():
    # Initialise Connection to Database
    database_connector = connector.DatabaseConnector(config[Config.Headers.database])
    database_connector.start_connection()

    if (config[Config.Headers.system][Config.Keys.System.is_initialised] ==
            Config.DefaultKeyValuePairs.system[Config.Keys.System.is_initialised]):
        # Define the Schema and Tables for the Database
        schema_definition = format_text_file_lines(get_text_file_lines(DBQueryFilePath.schema),
                                                   schema_name=DBSchemaTableNames.schema)
        database_connector.execute_queries_sequentially(schema_definition)

        # Addition of Sample Data (before modification during demonstration, provided the data has not been added yet)
        add_sample_data(DBQueryFilePath.add_customer,
                        SampleDataFilePath.customers, database_connector)
        add_sample_data(DBQueryFilePath.add_product,
                        SampleDataFilePath.products, database_connector)
        add_sample_data(DBQueryFilePath.add_location,
                        SampleDataFilePath.locations, database_connector)
        add_sample_data(DBQueryFilePath.add_customer_location,
                        SampleDataFilePath.customer_locations, database_connector)
        add_sample_data(DBQueryFilePath.add_company_order,
                        SampleDataFilePath.company_orders, database_connector)
        add_sample_data(DBQueryFilePath.add_customer_order,
                        SampleDataFilePath.customer_orders, database_connector)
        add_sample_data(DBQueryFilePath.add_customer_order_item,
                        SampleDataFilePath.customer_order_items, database_connector)
        
        # Update Config File
        config[Config.Headers.system][Config.Keys.System.is_initialised] = "1"
        # noinspection PyShadowingNames
        with open(Config.file_path, "w+", newline=Config.newline_char) as config_file:
            config.write(config_file)

    # Set-Up Database Connector in and Activate Web Interface
    database_connector.execute_queries_sequentially(get_text_file_lines(DBQueryFilePath.startup))
    webfrontend.utils.database_connector = database_connector
    webfrontend.app.run(debug=True, host=config[Config.Headers.web_interface][Config.Keys.WebInterface.host],
                        port=config[Config.Headers.web_interface][Config.Keys.WebInterface.port])

    # Stop Connection to Database
    database_connector.stop_connection()


if __name__ == "__main__":
    main_activity()
    logger.trim(LoggerConfig.log_size)
