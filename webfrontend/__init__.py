#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from flask import Flask, request, render_template
from database.query_constructors import QueryConstructor
from base.constants import *
from webfrontend.forms.select_filters import CustomersDataFilterForm, ProductsDataFilterForm
from webfrontend.forms.select_filters import CustomerOrdersDataFilterForm, CompanyOrdersDataFilterForm
from webfrontend.forms.details_view import CustomerDetails


app = Flask(__name__)
database_connector = None


customers_query_constructor = QueryConstructor(
    DBSchemaTableNames.customers,
    DBSchemaTableNames.schema
)

locations_query_constructor = QueryConstructor(
    DBSchemaTableNames.locations,
    DBSchemaTableNames.schema
)

customer_locations_query_constructor = QueryConstructor(
    DBSchemaTableNames.customer_locations,
    DBSchemaTableNames.schema
)

products_query_constructor = QueryConstructor(
    DBSchemaTableNames.products,
    DBSchemaTableNames.schema
)

customer_orders_query_constructor = QueryConstructor(
    DBSchemaTableNames.customer_orders,
    DBSchemaTableNames.schema
)

customer_order_items_query_constructor = QueryConstructor(
    DBSchemaTableNames.customer_order_items,
    DBSchemaTableNames.schema
)

company_orders_query_constructor = QueryConstructor(
    DBSchemaTableNames.company_orders,
    DBSchemaTableNames.schema
)


def get_selected_records(query_constructor: QueryConstructor) -> list:
    """Get the select query for a particular table, using the QueryConstructor object assigned to it.
    :type query_constructor: QueryConstructor
    """
    query = query_constructor.render_select_query()
    selection = database_connector.execute_query(
        query,
        select=True
    )
    return selection


def update_record(query_constructor: QueryConstructor):
    query = query_constructor.render_update_query()
    return database_connector.execute_query(query, commit=True)


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
    if form_result["date_registered_selection"][0] == "filter":
        customers_query_constructor.add_condition_ranged_values(
            DBFields.Customers.date_registered,
            lower_limit=form_result["date_registered_lower_limit_string"][0],
            upper_limit=form_result["date_registered_upper_limit_string"][0]
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
    if form_result["gtin14_selection"][0]:
        products_query_constructor.add_condition_like(
            DBFields.Products.gtin14,
            form_result["gtin14_string"][0],
            at_beginning=("gtin14_at_beginning" in form_result),
            at_end=("gtin14_at_end" in form_result)
        )
        condition_count += 1
    if form_result["name_selection"][0]:
        products_query_constructor.add_condition_like(
            DBFields.Products.name,
            form_result["name_string"][0],
            at_beginning=("name_at_beginning" in form_result),
            at_end=("name_at_end" in form_result)
        )
        condition_count += 1
    if form_result["desc_selection"][0]:
        products_query_constructor.add_condition_like(
            DBFields.Products.description,
            form_result["desc_string"][0],
            at_beginning=("desc_at_beginning" in form_result),
            at_end=("desc_at_end" in form_result)
        )
        condition_count += 1
    if form_result["current_price_selection"][0]:
        products_query_constructor.add_condition_ranged_values(
            DBFields.Products.current_price,
            lower_limit=form_result["current_price_lower_limit_string"][0],
            upper_limit=form_result["current_price_upper_limit_string"][0]
        )
        condition_count += 1
    if form_result["qty_in_stock_selection"][0]:
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
    if form_result["total_price_paid_selection"][0] == "filter":
        company_orders_query_constructor.add_condition_ranged_values(
            DBFields.CompanyOrders.total_price_paid,
            lower_limit=form_result["total_price_paid_lower_limit_string"][0],
            upper_limit=form_result["total_price_paid_upper_limit_string"][0]
        )
        condition_count += 1
    return bool(condition_count)


@app.route("/customers", methods=["GET", "POST"])
def show_customers():
    form = CustomersDataFilterForm()
    if request.method == "GET" or (request.method == "POST" and not form.validate()):
        customers_query_constructor.reset()
        selection = get_selected_records(customers_query_constructor)
        if selection[0] == 0:
            return render_template("customers.html",
                                   selection=selection[1],
                                   form=form)
    result = request.form.to_dict(flat=False)
    filter_customer_selection(result)
    if filter_location_selection(result):
        locations_query_constructor.add_field(DBFields.Locations.id)
        customer_locations_query_constructor.reset()
        customer_locations_query_constructor.add_nested_query(
            DBFields.CustomerLocations.location_id,
            locations_query_constructor.render_select_query()
        )
        customer_locations_query_constructor.add_field(DBFields.CustomerLocations.customer_id)
        customers_query_constructor.add_nested_query(
            DBFields.Customers.id,
            customer_locations_query_constructor.render_select_query()
        )
    if filter_customer_order_selection(result):
        customer_orders_query_constructor.add_field(DBFields.CustomerOrders.customer_id)
        customers_query_constructor.add_nested_query(
            DBFields.Customers.id,
            customer_orders_query_constructor.render_select_query()
        )
    if filter_product_selection(result):
        products_query_constructor.add_field(DBFields.Products.gtin14)
        customer_order_items_query_constructor.reset()
        customer_order_items_query_constructor.add_nested_query(
            DBFields.CustomerOrderItems.product_gtin14,
            products_query_constructor.render_select_query()
        )
        customer_order_items_query_constructor.add_field(DBFields.CustomerOrderItems.customer_order_id)
        customer_orders_query_constructor.reset()
        customer_orders_query_constructor.add_nested_query(
            DBFields.CustomerOrders.id,
            customer_order_items_query_constructor.render_select_query()
        )
        customer_orders_query_constructor.add_field(DBFields.CustomerOrders.customer_id)
        customers_query_constructor.add_nested_query(
            DBFields.Customers.id,
            customer_orders_query_constructor.render_select_query()
        )
    selection = get_selected_records(customers_query_constructor)
    if selection[0] == 0:
        return render_template("customers.html",
                               selection=selection[1],
                               form=form)


@app.route("/products", methods=["GET", "POST"])
def show_products():
    form = ProductsDataFilterForm()
    if request.method == "GET" or (request.method == "POST" and not form.validate()):
        products_query_constructor.reset()
        selection = get_selected_records(products_query_constructor)
        if selection[0] == 0:
            return render_template("products.html",
                                   selection=selection[1],
                                   form=form)
    result = request.form.to_dict(flat=False)
    filter_product_selection(result)
    if filter_customer_selection(result):
        customers_query_constructor.add_field(DBFields.Customers.id)
        customer_orders_query_constructor.reset()
        customer_orders_query_constructor.add_nested_query(
            DBFields.CustomerOrders.customer_id,
            customers_query_constructor.render_select_query()
        )
        customer_orders_query_constructor.add_field(DBFields.CustomerOrders.id)
        customer_order_items_query_constructor.reset()
        customer_order_items_query_constructor.add_nested_query(
            DBFields.CustomerOrderItems.customer_order_id,
            customer_orders_query_constructor.render_select_query()
        )
        customer_order_items_query_constructor.add_field(DBFields.CustomerOrderItems.product_gtin14)
        products_query_constructor.add_nested_query(
            DBFields.Products.gtin14,
            customer_order_items_query_constructor.render_select_query()
        )
    if filter_location_selection(result):
        locations_query_constructor.add_field(DBFields.Locations.id)
        customer_orders_query_constructor.reset()
        customer_orders_query_constructor.add_nested_query(
            DBFields.CustomerOrders.delivery_location,
            locations_query_constructor.render_select_query()
        )
        customer_orders_query_constructor.add_field(DBFields.CustomerOrders.id)
        customer_order_items_query_constructor.reset()
        customer_order_items_query_constructor.add_nested_query(
            DBFields.CustomerOrderItems.customer_order_id,
            customer_orders_query_constructor.render_select_query()
        )
        customer_order_items_query_constructor.add_field(DBFields.CustomerOrderItems.product_gtin14)
        products_query_constructor.add_nested_query(
            DBFields.Products.gtin14,
            customer_order_items_query_constructor.render_select_query()
        )
    if filter_customer_order_selection(result):
        customer_orders_query_constructor.add_field(DBFields.CustomerOrders.id)
        customer_order_items_query_constructor.reset()
        customer_order_items_query_constructor.add_nested_query(
            DBFields.CustomerOrderItems.customer_order_id,
            customer_orders_query_constructor.render_select_query()
        )
        customer_order_items_query_constructor.add_field(DBFields.CustomerOrderItems.product_gtin14)
        products_query_constructor.add_nested_query(
            DBFields.Products.gtin14,
            customer_order_items_query_constructor.render_select_query()
        )
    if filter_company_order_selection(result):
        company_orders_query_constructor.add_field(DBFields.CompanyOrders.product_gtin14)
        products_query_constructor.add_nested_query(
            DBFields.Products.gtin14,
            company_orders_query_constructor.render_select_query()
        )
    selection = get_selected_records(products_query_constructor)
    if selection[0] == 0:
        return render_template("products.html",
                               selection=selection[1],
                               form=form)


@app.route("/customer-orders", methods=["GET", "POST"])
def show_customer_orders():
    form = CustomerOrdersDataFilterForm()
    if request.method == "GET" or (request.method == "POST" and not form.validate()):
        customer_orders_query_constructor.reset()
        selection = get_selected_records(customer_orders_query_constructor)
        if selection[0] == 0:
            return render_template("customerOrders.html",
                                   selection=selection[1],
                                   form=form)
    result = request.form.to_dict(flat=False)
    filter_customer_order_selection(result)
    if filter_customer_selection(result):
        customers_query_constructor.add_field(DBFields.Customers.id)
        customer_orders_query_constructor.add_nested_query(
            DBFields.CustomerOrders.customer_id,
            customers_query_constructor.render_select_query()
        )
    if filter_location_selection(result):
        locations_query_constructor.add_field(DBFields.Locations.id)
        customer_orders_query_constructor.add_nested_query(
            DBFields.CustomerOrders.delivery_location,
            locations_query_constructor.render_select_query()
        )
    if filter_product_selection(result):
        products_query_constructor.add_field(DBFields.Products.gtin14)
        customer_order_items_query_constructor.reset()
        customer_order_items_query_constructor.add_nested_query(
            DBFields.CustomerOrderItems.product_gtin14,
            products_query_constructor.render_select_query()
        )
        customer_order_items_query_constructor.add_field(DBFields.CustomerOrderItems.customer_order_id)
        customer_orders_query_constructor.add_nested_query(
            DBFields.CustomerOrders.id,
            customer_order_items_query_constructor.render_select_query()
        )
    selection = get_selected_records(customer_orders_query_constructor)
    if selection[0] == 0:
        return render_template("customerOrders.html",
                               selection=selection[1],
                               form=form)


@app.route("/company-orders", methods=["GET", "POST"])
def show_company_orders():
    form = CompanyOrdersDataFilterForm()
    if request.method == "GET" or (request.method == "POST" and not form.validate()):
        company_orders_query_constructor.reset()
        selection = get_selected_records(company_orders_query_constructor)
        if selection[0] == 0:
            return render_template("companyOrders.html",
                                   selection=selection[1],
                                   form=form)
    result = request.form.to_dict(flat=False)
    filter_company_order_selection(result)
    if filter_product_selection(result):
        products_query_constructor.add_field(DBFields.Products.gtin14)
        company_orders_query_constructor.add_nested_query(
            DBFields.CompanyOrders.product_gtin14,
            products_query_constructor.render_select_query()
        )
    selection = get_selected_records(company_orders_query_constructor)
    if selection[0] == 0:
        return render_template("companyOrders.html",
                               selection=selection[1],
                               form=form)


@app.route("/customers/<customer_id>", methods=["GET", "POST"])
def show_customer_details_view(customer_id):
    form = CustomerDetails()
    is_updated = -1
    alert_msg = ""

    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        customers_query_constructor.reset()
        customers_query_constructor.add_condition_exact_value(
            DBFields.Customers.id,
            customer_id
        )
        customers_query_constructor.add_field_and_value(
            DBFields.Customers.first_name,
            result["first_name_string"][0]
        )
        customers_query_constructor.add_field_and_value(
            DBFields.Customers.last_name,
            result["last_name_string"][0]
        )
        customers_query_constructor.add_field_and_value(
            DBFields.Customers.email_address,
            result["email_address_string"][0]
        )
        customers_query_constructor.add_field_and_value(
            DBFields.Customers.phone,
            result["phone_string"][0]
        )
        is_updated = update_record(customers_query_constructor)

        if is_updated[0] == 1:
            alert_msg = is_updated[1]
        is_updated = is_updated[0]

    customers_query_constructor.reset()
    customers_query_constructor.add_condition_exact_value(
        DBFields.Customers.id,
        customer_id
    )
    details = get_selected_records(customers_query_constructor)[1]
    form.customer_id_string.data = details[0][0]
    form.first_name_string.data = details[0][2]
    form.last_name_string.data = details[0][1]
    form.email_address_string.data = details[0][3]
    form.phone_string.data = details[0][4]
    form.date_registered_string.data = details[0][5]
    print("updated?", is_updated)
    return render_template("customerDetailsView.html", form=form, updated=is_updated, alert_msg=alert_msg)
