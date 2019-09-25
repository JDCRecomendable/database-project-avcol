#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.utils import *
from database import connector
import webfrontend

# If configuration exists, read it. Else, make one for editing by the user.
config = read_config(Config.file_path)
config_exists = check_if_config_exists(Config.file_path)
if not config_exists:
    config[Config.Headers.system] = Config.DefaultKeyValuePairs.system
    config[Config.Headers.database] = Config.DefaultKeyValuePairs.database
    with open(Config.file_path, "w+", newline=Config.newline_char) as config_file:
        config.write(config_file)


def add_sample_data(query_file_path, data_source_file_path, db_connector):
    query = get_text_file_lines_as_single_line(query_file_path)
    for line in get_text_file_lines(data_source_file_path):
        line = line.strip()
        line_elements = line.split(";")
        db_connector.execute_query(
            query.format(*line_elements),
            commit=True
        )


def main_activity():
    # Initialise Connection to Database
    database_connector = connector.DatabaseConnector(config[Config.Headers.database])
    database_connector.start_connection()

    if (config[Config.Headers.system][Config.Keys.System.is_initialised] ==
            Config.DefaultKeyValuePairs.system[Config.Keys.System.is_initialised]):
        # Define the Schema and Tables for the Database
        database_connector.execute_queries_sequentially(get_text_file_lines(DBQueryFilePath.schema))

        # Addition of Sample Data (before modification during demonstration, provided the data has not been added yet)
        add_sample_data(DBQueryFilePath.add_customer,
                        SampleDataFilepath.customers, database_connector)
        add_sample_data(DBQueryFilePath.add_product,
                        SampleDataFilepath.products, database_connector)
        add_sample_data(DBQueryFilePath.add_location,
                        SampleDataFilepath.locations, database_connector)
        add_sample_data(DBQueryFilePath.add_customer_location,
                        SampleDataFilepath.customer_locations, database_connector)
        add_sample_data(DBQueryFilePath.add_company_order,
                        SampleDataFilepath.company_orders, database_connector)
        add_sample_data(DBQueryFilePath.add_customer_order,
                        SampleDataFilepath.customer_orders, database_connector)
        add_sample_data(DBQueryFilePath.add_customer_order_item,
                        SampleDataFilepath.customer_order_items, database_connector)
        config[Config.Headers.system][Config.Keys.System.is_initialised] = "1"
        with open(Config.file_path, "w+", newline=Config.newline_char) as config_file:
            config.write(config_file)

    # Set-Up Database Connector in and Activate Web Interface
    webfrontend.database_connector = database_connector
    webfrontend.app.run(debug=True)

    # Stop Connection to Database
    database_connector.stop_connection()


def test_activity():
    from database import query_constructors

    # query_constructor = query_constructors.NewQueryConstructor("products", "online_shop_logistics")
    query_constructor = query_constructors.QueryConstructor("products")
    query_constructor.add_field("gtin14")
    print(query_constructor.render_select_query())
    print("Meant to fail:")
    print(query_constructor.render_update_query())
    print("Meant to fail:")
    print(query_constructor.render_delete_query())
    query_constructor.add_condition_like("name", "rice")
    query_constructor.add_condition_ranged_values("price", "50", "200")
    print(query_constructor.render_select_query())
    query_constructor.add_field("name")
    print(query_constructor.render_select_query())
    query_constructor.add_value("rice")
    query_constructor.add_value("15.50")
    print(query_constructor.render_update_query())
    print(query_constructor.render_delete_query())
    query_constructor.reset()
    print(query_constructor.render_select_query())
    print("Meant to fail:")
    print(query_constructor.render_update_query())
    print("Meant to fail:")
    print(query_constructor.render_delete_query())
    query_constructor.add_condition_exact_value("name", "rice")
    print(query_constructor.render_delete_query())
    print("Meant to fail:")
    print(query_constructor.render_update_query())
    query_constructor.add_field("description")
    query_constructor.add_value("test")
    print(query_constructor.render_update_query())


if __name__ == "__main__":
    main_activity()
    # test_activity()
