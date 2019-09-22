#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.utils import *
from database import connector
from database import table_adapters
import webfrontend

# If configuration exists, read it. Else, make one for editing by the user.
config = read_config(Config.file_path)
config_exists = check_if_config_exists(Config.file_path)
if not config_exists:
    config[Config.Headers.system] = Config.DefaultKeyValuePairs.system
    config[Config.Headers.database] = Config.DefaultKeyValuePairs.database
    with open(Config.file_path, "w+", newline=Config.newline_char) as config_file:
        config.write(config_file)


def add_sample_data(table_adapter, data_source_file_path, db_connector):
    for line in get_text_file_lines(data_source_file_path):
        line = line.strip()
        line_elements = line.split(";")
        db_connector.execute_query(
            table_adapter.insert_data(line_elements),
            commit=True
        )


def read_sample_data(table_adapter, db_connector):
    table_adapter.reset_select_query_constructor()
    results = db_connector.execute_query(
        table_adapter.render_select_query(),
        select=True
    )
    return results


def main_activity():
    # Initialise Connection to Database
    database_connector = connector.DatabaseConnector(config[Config.Headers.database])
    database_connector.start_connection()

    # Initialise Table Adapters
    customers_table = table_adapters.CustomersTableAdapter()
    products_table = table_adapters.ProductsTableAdapter()
    locations_table = table_adapters.LocationsTableAdapter()
    customer_locations_table = table_adapters.CustomerLocationsTableAdapter()
    company_orders_table = table_adapters.CompanyOrdersTableAdapter()
    customer_orders_table = table_adapters.CustomerOrdersTableAdapter()
    customer_order_items_table = table_adapters.CustomerOrderItemsTableAdapter()

    if (config[Config.Headers.system][Config.Keys.System.is_initialised] ==
            Config.DefaultKeyValuePairs.system[Config.Keys.System.is_initialised]):
        # Define the Schema and Tables for the Database
        database_connector.execute_queries_sequentially(get_text_file_lines(DatabaseQueryFilePath.schema))

        # Addition of Sample Data (before modification during demonstration, provided the data has not been added yet)
        add_sample_data(customers_table, SampleDataFilepath.customers, database_connector)
        add_sample_data(products_table, SampleDataFilepath.products, database_connector)
        add_sample_data(locations_table, SampleDataFilepath.locations, database_connector)
        add_sample_data(customer_locations_table, SampleDataFilepath.customer_locations, database_connector)
        add_sample_data(company_orders_table, SampleDataFilepath.company_orders, database_connector)
        add_sample_data(customer_orders_table, SampleDataFilepath.customer_orders, database_connector)
        add_sample_data(customer_order_items_table, SampleDataFilepath.customer_order_items, database_connector)
        config[Config.Headers.system][Config.Keys.System.is_initialised] = "1"
        with open(Config.file_path, "w+", newline=Config.newline_char) as config_file:
            config.write(config_file)

    # Read Sample Data from Database
    customers_selection = read_sample_data(customers_table, database_connector)
    products_selection = read_sample_data(products_table, database_connector)
    customer_orders_selection = read_sample_data(customer_orders_table, database_connector)
    company_orders_selection = read_sample_data(company_orders_table, database_connector)

    # Activate Web Interface
    webfrontend.customers_selection = customers_selection
    webfrontend.products_selection = products_selection
    webfrontend.customer_orders_selection = customer_orders_selection
    webfrontend.company_orders_selection = company_orders_selection
    webfrontend.app.run(debug=True)

    # Stop Connection to Database
    database_connector.stop_connection()


if __name__ == "__main__":
    main_activity()
