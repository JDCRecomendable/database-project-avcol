#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""


class Config:
    file_path = "config.cfg"
    newline_char = "\r\n"

    class Headers:
        system = "SYSTEM"
        database = "DATABASE"

    class Keys:
        class System:
            is_initialised = "is_initialised"

        class Database:
            username = "username"
            password = "password"
            host = "host"

    class DefaultKeyValuePairs:
        system = {
            "is_initialised": "0"
        }
        database = {
            "username": "root",
            "password": "abc123",
            "host": "127.0.0.1"
        }


class Msg:
    class Symbol:
        message = "*"
        warning = "!"
        error = "E"

    class DatabaseConnector:
        # Processing
        connecting = "Connecting to database server..."
        table_creating = "Creating database tables..."

        # Completed
        connected = "Connection to database server successful."
        connection_stopped = "Connection to database server stopped."
        tables_created = "Database tables successfully created."
        command_processed = "Executed SQL command "

        # Error
        invalid_database_credentials = "Invalid username or password for database! Please check your config file."
        database_not_exists = "The target database does not exist! Please check your config file."
        not_connected = "Not connected to database server."
        failed_to_add_data = "Failed to add data to the database."

    class DatabaseQueryConstructor:
        # Error
        missing_table_name = "Missing table name so cannot render the SQL query."
        missing_fields_or_values = "Missing fields or values required, so cannot render SQL UPDATE query."
        number_of_field_and_value_mismatch = "Number of fields is not the same as number of values, so cannot render SQL UPDATE query."
        missing_ranged_values_limits = "Missing lower and upper limits required for adding a condition for ranged values."
        cannot_render = "Unable to render the SQL query."

    class FileManipulation:
        # Error
        file_not_exists = "File does not exist!"


class DBSchemaTableNames:
    schema = "online_shop_logistics"
    customers = "customers"
    customer_locations = "customer_locations"
    locations = "locations"
    customer_order_items = "customer_order_items"
    customer_orders = "customer_orders"
    products = "products"
    company_orders = "company_orders"


class DBFields:
    class Customers:
        id = "id"
        last_name = "last_name"
        first_name = "first_name"
        email_address = "email_address"
        phone = "phone"
        date_registered = "date_registered"

    class CustomerLocations:
        customer_id = "customer_id"
        location_id = "location_id"

    class Locations:
        id = "id"
        city = "city"
        road_name = "road_name"
        place_no = "place_no"

    class CustomerOrderItems:
        customer_order_id = "customer_order_id"
        product_gtin14 = "product_gtin14"
        qty_bought = "qty_bought"
        total_price_paid = "total_price_paid"

    class CustomerOrders:
        id = "id"
        customer_id = "customer_id"
        datetime_ordered = "datetime_ordered"
        delivery_date = "delivery_date"
        delivery_location = "delivery_location"

    class Products:
        gtin14 = "gtin14"
        name = "name"
        description = "description"
        current_price = "current_price"
        qty_in_stock = "qty_in_stock"

    class CompanyOrders:
        id = "id"
        product_gtin14 = "product_gtin14"
        datetime_ordered = "datetime_ordered"
        qty_bought = "qty_bought"
        total_price_paid = "total_price_paid"
        delivery_date = "delivery_date"


class DBQueryFilePath:
    """File paths for database commands on the local machine."""
    # Schema Creation
    schema = "commands/schema.sql"

    # Data Deletion (QUESTIONABLE)
    delete_company_order = "commands/deletion/delete_company_order.sql"
    delete_customer_location = "commands/deletion/delete_customer_location.sql"
    delete_customer_order_item = "commands/deletion/delete_customer_order_item.sql"
    delete_customer_order = "commands/deletion/delete_customer_order.sql"
    delete_customer = "commands/deletion/delete_customer.sql"
    delete_location = "commands/deletion/delete_location.sql"
    delete_product = "commands/deletion/delete_product.sql"

    # Data Insertion
    add_company_order = "commands/insertion/add_company_order.sql"
    add_customer_location = "commands/insertion/add_customer_location.sql"
    add_customer_order_item = "commands/insertion/add_customer_order_item.sql"
    add_customer_order = "commands/insertion/add_customer_order.sql"
    add_customer = "commands/insertion/add_customer.sql"
    add_location = "commands/insertion/add_location.sql"
    add_product = "commands/insertion/add_product.sql"

    # Data Reading (QUESTIONABLE)
    get_company_order_id_from_customerid_and_date = "commands/reading/get_company_order_id_from_customerid_and_datetime.sql"
    get_customer_order_id_from_customerid_and_date = "commands/reading/get_customer_order_id_from_customerid_and_datetime.sql"
    get_customerid_from_email_address = "commands/reading/get_customerid_from_email_address.sql"
    get_locationid_from_address = "commands/reading/get_locationid_from_address.sql"
    get_product_id_from_name = "commands/reading/get_product_id_from_name.sql"
    list_all_company_orders = "commands/reading/list_all_company_orders.sql"
    list_all_customer_locations = "commands/reading/list_all_customer_locations.sql"
    list_all_customer_orders = "commands/reading/list_all_customer_orders.sql"
    list_all_customers = "commands/reading/list_all_customers.sql"
    list_all_locations = "commands/reading/list_all_locations.sql"
    list_all_products = "commands/reading/list_all_products.sql"
    list_specific_company_orders_of_products = "commands/reading/list_specific_company_orders_of_products.sql"
    list_specific_customer_order_items_from_customer_order = "commands/reading/list_specific_customer_order_items_from_customer_order.sql"
    list_specific_customer_order_items_from_customer = "commands/reading/list_specific_customer_order_items_from_customer.sql"
    list_specific_customer_order_items_to_customer_and_location = "commands/reading/list_specific_customer_order_items_to_customer_and_location.sql"
    list_specific_customer_order_items_to_location = "commands/reading/list_specific_customer_order_items_to_location.sql"
    list_specific_customer_orders_of_customer = "commands/reading/list_specific_customer_orders_of_customer.sql"
    list_specific_customer_orders_to_customer_and_location = "commands/reading/list_specific_customer_orders_to_customer_and_location.sql"
    list_specific_customer_orders_to_location = "commands/reading/list_specific_customer_orders_to_location.sql"
    list_specific_customers_in_location = "commands/reading/list_specific_customers_in_location.sql"
    list_specific_locations_of_customer = "commands/reading/list_specific_locations_of_customer.sql"
    list_specific_products_from_customer_order = "commands/reading/list_specific_products_from_customer_order.sql"
    list_specific_products_to_customer_and_location = "commands/reading/list_specific_products_to_customer_and_location.sql"
    list_specific_products_to_customer = "commands/reading/list_specific_products_to_customer.sql"
    list_specific_products_to_location = "commands/reading/list_specific_products_to_location.sql"
    return_total_expenditure = "commands/reading/return_total_expenditure.sql"
    return_total_income = "commands/reading/return_total_income.sql"


class SampleDataFilepath:
    customers = "sample_data/customers.txt"
    locations = "sample_data/locations.txt"
    customer_locations = "sample_data/customer_locations.txt"
    customer_orders = "sample_data/customer_orders.txt"
    products = "sample_data/products.txt"
    customer_order_items = "sample_data/customer_order_items.txt"
    company_orders = "sample_data/company_orders.txt"


class WebInterface:
    class DBAttibuteLabels:
        class Customers:
            id = "#"
            first_name = "First Name"
            last_name = "Last Name"
            email_address = "Email Address"
            phone = "Phone Number"
            date_registered = "Date Registered"

        class Products:
            gtin14 = "GTIN-14"
            name = "Name of Product"
            description = "Description"
            current_price = "Current Price"
            qty_in_stock = "Qty in Stock"

        class CustomerOrders:
            id = "#"
            customer_id = "Customer"
            datetime_ordered = "Date/Time Ordered"
            delivery_date = "Delivery Date"
            delivery_location = "Delivery Location"

        class CompanyOrders:
            id = "#"
            product_gtin14 = "Product GTIN-14"
            datetime_ordered = "Date/Time Ordered"
            qty_bought = "Qty Bought"
            total_price_paid = "Total Price Paid"
            delivery_date = "Delivery Date"

    class DataFilterForm:
        @staticmethod
        def selection_label(attribute_name):
            return "Sort by {}".format(attribute_name)

        @staticmethod
        def entry_label(attribute_name):
            return "Enter {}".format(attribute_name)

        class Customers:
            # Selection
            first_name_no_filter_id = "fNameNoFilter"
            first_name_no_filter_label = "Do not filter"
            first_name_filter_id = "fNameFilter"
            first_name_filter_label = "Filter"

            last_name_no_filter_id = "lNameNoFilter"
            last_name_no_filter_label = "Do not filter"
            last_name_filter_id = "lNameFilter"
            last_name_filter_label = "Filter"

            email_address_no_filter_id = "emailAddressNoFilter"
            email_address_no_filter_label = "Do not filter"
            email_address_filter_id = "emailAddressFilter"
            email_address_filter_label = "Filter"

            phone_no_filter_id = "phoneNoFilter"
            phone_no_filter_label = "Do not filter"
            phone_filter_id = "phoneFilter"
            phone_filter_label = "Filter"

            date_registered_no_filter_id = "dateRegisteredFilter"
            date_registered_no_filter_label = "Do not filter"
            date_registered_filter_id = "dateRegisteredFilter"
            date_registered_filter_label = "Filter"

            # Validators
            email_address_invalid = "Invalid email address!"
            phone_length_invalid = "Phone number length is invalid!"

        class Products:
            # Selection
            pass
            # Validators
