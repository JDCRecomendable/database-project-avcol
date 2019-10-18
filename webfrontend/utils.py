#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from flask import flash
from database.query_constructors import QueryConstructor
from base.constants import *
from base.utils import get_text_file_lines_as_single_line, remove_unsafe_chars

database_connector = None
customers_query_constructor = None
locations_query_constructor = None
customer_locations_query_constructor = None
products_query_constructor = None
customer_orders_query_constructor = None
customer_order_items_query_constructor = None
company_orders_query_constructor = None


# Flash Messages
def flash_success(message: str):
    """Add success message to next request. Assumes that the next request supports rendering flashed messages.
    :type message: str
    """
    flash(message, "success")


def flash_info(message: str):
    """Add info message to next request. Assumes that the next request supports rendering flashed messages.
    :type message: str
    """
    flash(message, "info")


def flash_danger(message: str):
    """Add danger message to next request. Assumes that the next request supports rendering flashed messages.
    :type message: str
    """
    flash(message, "danger")


# Manipulate Database
def get_selected_records(query_constructor: QueryConstructor) -> list:
    """Return selected records.
    :type query_constructor: QueryConstructor
    """
    query = query_constructor.render_select_query()
    selection = database_connector.execute_query(query, select=True)
    return selection


def update_record(query_constructor: QueryConstructor):
    """Update record(s) that the query_constructor will select, given condition(s) set to it.
    :type query_constructor: QueryConstructor
    """
    query = query_constructor.render_update_query()
    return database_connector.execute_query(query, commit=True)


def add_record(insert_query_filepath: str, values: list):
    """Add a record to the appropriate table that the insert query refers to.
    :type insert_query_filepath: str
    :type values: list
    """
    query = get_text_file_lines_as_single_line(insert_query_filepath)
    values_processed = []
    for value in values:
        values_processed.append(remove_unsafe_chars(value))
    return database_connector.execute_query(query.format(DBSchemaTableNames.schema, *values_processed), commit=True)


def delete_record(query_constructor: QueryConstructor):
    """Delete record(s) that the query_constructor will select, given condition(s) set to it.
    :type query_constructor: QueryConstructor
    """
    query = query_constructor.render_delete_query()
    return database_connector.execute_query(query, commit=True)


# Filter Data from Forms
def filter_customer_selection(form_result: dict) -> bool:
    """Add the conditions for customers to the SQL query constructor, if any, and return True if at least one condition
    is added.
    """
    customers_query_constructor.reset()
    condition_count = 0
    if form_result["customer_id_selection"][0] == "filter":
        customers_query_constructor.add_condition_exact_value(
            DBFields.Customers.id,
            form_result["customer_id_string"][0]
        )
        condition_count += 1
    if form_result["first_name_selection"][0] == "filter":
        customers_query_constructor.add_condition_like(
            DBFields.Customers.first_name,
            form_result["first_name_string"][0],
            at_beginning=("first_name_at_beginning" in form_result),
            at_end=("first_name_at_end" in form_result)
        )
        condition_count += 1
    if form_result["last_name_selection"][0] == "filter":
        customers_query_constructor.add_condition_like(
            DBFields.Customers.last_name,
            form_result["last_name_string"][0],
            at_beginning=("last_name_at_beginning" in form_result),
            at_end=("last_name_at_end" in form_result)
        )
        condition_count += 1
    if form_result["email_address_selection"][0] == "filter":
        customers_query_constructor.add_condition_exact_value(
            DBFields.Customers.email_address,
            form_result["email_address_string"][0]
        )
        condition_count += 1
    if form_result["phone_selection"][0] == "filter":
        customers_query_constructor.add_condition_exact_value(
            DBFields.Customers.phone,
            form_result["phone_string"][0]
        )
        condition_count += 1
    return bool(condition_count)


def filter_location_selection(form_result: dict) -> bool:
    """Add the conditions for locations to the SQL query constructor, if any, and return True if at least one condition
    is added.
    """
    locations_query_constructor.reset()
    if form_result["location_selection"][0] == "filter":
        locations_query_constructor.add_condition_like(
            DBFields.Locations.place_no,
            form_result["location_place_no"][0]
        )
        locations_query_constructor.add_condition_like(
            DBFields.Locations.road_name,
            form_result["location_road_name"][0]
        )
        locations_query_constructor.add_condition_like(
            DBFields.Locations.city,
            form_result["location_city"][0]
        )
        return True
    return False


def filter_product_selection(form_result: dict) -> bool:
    """Add the condition for products to the SQL query constructor, if any, and return True if at least one condition
    is added.
    """
    products_query_constructor.reset()
    condition_count = 0
    if form_result["gtin14_selection"][0] == "filter":
        products_query_constructor.add_condition_like(
            DBFields.Products.gtin14,
            form_result["gtin14_string"][0],
            at_beginning=("gtin14_at_beginning" in form_result),
            at_end=("gtin14_at_end" in form_result)
        )
        condition_count += 1
    if form_result["name_selection"][0] == "filter":
        products_query_constructor.add_condition_like(
            DBFields.Products.name,
            form_result["name_string"][0],
            at_beginning=("name_at_beginning" in form_result),
            at_end=("name_at_end" in form_result)
        )
        condition_count += 1
    if form_result["desc_selection"][0] == "filter":
        products_query_constructor.add_condition_like(
            DBFields.Products.description,
            form_result["desc_string"][0],
            at_beginning=("desc_at_beginning" in form_result),
            at_end=("desc_at_end" in form_result)
        )
        condition_count += 1
    if form_result["qty_in_stock_selection"][0] == "filter":
        products_query_constructor.add_condition_ranged_values(
            DBFields.Products.qty_in_stock,
            lower_limit=form_result["qty_in_stock_lower_limit_string"][0],
            upper_limit=form_result["qty_in_stock_upper_limit_string"][0]
        )
        condition_count += 1
    return bool(condition_count)


def filter_customer_order_selection(form_result: dict) -> bool:
    """Add the condition for customer orders to the SQL query constructor, if any, and return True if at least one
    condition is added.
    """
    customer_orders_query_constructor.reset()
    condition_count = 0
    if form_result["customer_order_id_selection"][0] == "filter":
        customer_orders_query_constructor.add_condition_exact_value(
            DBFields.CustomerOrders.id,
            form_result["customer_order_id_string"][0]
        )
        condition_count += 1
    if form_result["customer_datetime_ordered_selection"][0] == "filter":
        customer_orders_query_constructor.add_condition_ranged_values(
            DBFields.CustomerOrders.datetime_ordered,
            lower_limit=form_result["customer_datetime_ordered_lower_limit_string"][0],
            upper_limit=form_result["customer_datetime_ordered_upper_limit_string"][0]
        )
        condition_count += 1
    if form_result["customer_delivery_date_selection"][0] == "filter":
        customer_orders_query_constructor.add_condition_ranged_values(
            DBFields.CustomerOrders.delivery_date,
            lower_limit=form_result["customer_delivery_date_lower_limit_string"][0],
            upper_limit=form_result["customer_delivery_date_upper_limit_string"][0]
        )
        condition_count += 1
    return bool(condition_count)


def filter_company_order_selection(form_result: dict) -> bool:
    """Add the condition for company orders to the SQL query constructor, if any, and return True if at least one
    condition is added.
    """
    company_orders_query_constructor.reset()
    condition_count = 0
    if form_result["company_order_id_selection"][0] == "filter":
        company_orders_query_constructor.add_condition_exact_value(
            DBFields.CompanyOrders.id,
            form_result["company_order_id_string"][0]
        )
        condition_count += 1
    if form_result["company_datetime_ordered_selection"][0] == "filter":
        company_orders_query_constructor.add_condition_ranged_values(
            DBFields.CompanyOrders.datetime_ordered,
            lower_limit=form_result["company_datetime_ordered_lower_limit_string"][0],
            upper_limit=form_result["company_datetime_ordered_upper_limit_string"][0]
        )
        condition_count += 1
    if form_result["company_delivery_date_selection"][0] == "filter":
        company_orders_query_constructor.add_condition_ranged_values(
            DBFields.CompanyOrders.delivery_date,
            lower_limit=form_result["company_delivery_date_lower_limit_string"][0],
            upper_limit=form_result["company_delivery_date_upper_limit_string"][0]
        )
        condition_count += 1
    if form_result["qty_bought_selection"][0] == "filter":
        company_orders_query_constructor.add_condition_ranged_values(
            DBFields.CompanyOrders.qty_bought,
            lower_limit=form_result["qty_bought_lower_limit_string"][0],
            upper_limit=form_result["qty_bought_upper_limit_string"][0]
        )
        condition_count += 1
    return bool(condition_count)

