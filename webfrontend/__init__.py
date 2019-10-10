#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from flask import Flask, flash, request, render_template, redirect, url_for
from os import urandom
from database.query_constructors import QueryConstructor
from base.constants import *
from webfrontend.forms.select_filters import CustomersDataFilterForm, ProductsDataFilterForm
from webfrontend.forms.select_filters import CustomerOrdersDataFilterForm, CompanyOrdersDataFilterForm
from webfrontend.forms.details_view import CustomerDetailsForm, ProductDetailsForm
from webfrontend.forms.details_view import CustomerOrderDetailsForm, CompanyOrderDetailsForm


app = Flask(__name__)
app.secret_key = urandom(16)
database_connector = None


FLASH_DATA_FILTERED = "Data filtered."
FLASH_ERROR = "Error: {}"
FLASH_RECORD_UPDATED = "Record successfully updated."
FLASH_RECORD_DELETED = "Record successfully deleted."
FLASH_RECORD_NOT_DELETED = "Record not deleted. Any orders pending related to this record?"
FLASH_RECORD_ID_NO_MATCH = "Record not deleted. ID entered does not match the actual ID."

customers_query_constructor = QueryConstructor(DBSchemaTableNames.customers, DBSchemaTableNames.schema)
locations_query_constructor = QueryConstructor(DBSchemaTableNames.locations, DBSchemaTableNames.schema)
customer_locations_query_constructor = QueryConstructor(DBSchemaTableNames.customer_locations,
                                                        DBSchemaTableNames.schema)
products_query_constructor = QueryConstructor(DBSchemaTableNames.products, DBSchemaTableNames.schema)
customer_orders_query_constructor = QueryConstructor(DBSchemaTableNames.customer_orders, DBSchemaTableNames.schema)
customer_order_items_query_constructor = QueryConstructor(DBSchemaTableNames.customer_order_items,
                                                          DBSchemaTableNames.schema)
company_orders_query_constructor = QueryConstructor(DBSchemaTableNames.company_orders, DBSchemaTableNames.schema)


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


def delete_record(query_constructor: QueryConstructor):
    """Delete record(s) that the query_constructor will select, given condition(s) set to it.
    :type query_constructor: QueryConstructor
    """
    query = query_constructor.render_delete_query()
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


@app.route("/customers", methods=["GET", "POST"])
def show_customers():
    form = CustomersDataFilterForm()

    customers_query_constructor.reset()
    if request.method == "POST" and form.validate():
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
        flash_success(FLASH_DATA_FILTERED)

    selection = get_selected_records(customers_query_constructor)
    if selection[0] == 0:
        return render_template("dataTables/customers.html", selection=selection[1], form=form)
    return selection[1]


@app.route("/products", methods=["GET", "POST"])
def show_products():
    form = ProductsDataFilterForm()

    products_query_constructor.reset()
    if request.method == "POST" and form.validate():
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
        flash_success(FLASH_DATA_FILTERED)

    selection = get_selected_records(products_query_constructor)
    if selection[0] == 0:
        return render_template("dataTables/products.html", selection=selection[1], form=form)
    return selection[1]


@app.route("/customer-orders", methods=["GET", "POST"])
def show_customer_orders():
    form = CustomerOrdersDataFilterForm()

    customer_orders_query_constructor.reset()
    if request.method == "POST" and form.validate():
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
        flash_success(FLASH_DATA_FILTERED)

    selection = get_selected_records(customer_orders_query_constructor)
    if selection[0] == 0:
        return render_template("dataTables/customerOrders.html", selection=selection[1], form=form)
    return selection[1]


@app.route("/company-orders", methods=["GET", "POST"])
def show_company_orders():
    form = CompanyOrdersDataFilterForm()

    company_orders_query_constructor.reset()
    if request.method == "POST" and form.validate():
        result = request.form.to_dict(flat=False)
        filter_company_order_selection(result)
        if filter_product_selection(result):
            products_query_constructor.add_field(DBFields.Products.gtin14)
            company_orders_query_constructor.add_nested_query(
                DBFields.CompanyOrders.product_gtin14,
                products_query_constructor.render_select_query()
            )
        flash_success(FLASH_DATA_FILTERED)

    selection = get_selected_records(company_orders_query_constructor)
    if selection[0] == 0:
        return render_template("dataTables/companyOrders.html", selection=selection[1], form=form)
    return selection[1]


@app.route("/customers/<customer_id>", methods=["GET", "POST"])
def show_customer_details_view(customer_id):
    form = CustomerDetailsForm()

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
            flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    customers_query_constructor.reset()
    customers_query_constructor.add_condition_exact_value(
        DBFields.Customers.id,
        customer_id
    )
    selection = get_selected_records(customers_query_constructor)

    customer_locations_query_constructor.reset()
    customer_locations_query_constructor.add_condition_exact_value(
        DBFields.CustomerLocations.customer_id,
        customer_id
    )
    customer_locations_query_constructor.add_field(DBFields.CustomerLocations.location_id)
    locations_query_constructor.reset()
    locations_query_constructor.add_nested_query(
        DBFields.Locations.id,
        customer_locations_query_constructor.render_select_query()
    )
    location_selection = get_selected_records(locations_query_constructor)

    if selection[0] == 0 and location_selection[0] == 0:
        details = selection[1]
        form.customer_id_string.data = details[0][0]
        form.first_name_string.data = details[0][2]
        form.last_name_string.data = details[0][1]
        form.email_address_string.data = details[0][3]
        form.phone_string.data = details[0][4]
        return render_template("detailsView/customer.html", form=form, customer_id=customer_id, table_exists=True,
                               locations=location_selection[1])
    return "{}\n{}".format(selection[1], location_selection[1])


@app.route("/products/<product_gtin14>", methods=["GET", "POST"])
def show_product_details_view(product_gtin14):
    form = ProductDetailsForm()

    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        products_query_constructor.reset()
        products_query_constructor.add_condition_exact_value(
            DBFields.Products.gtin14,
            product_gtin14
        )
        products_query_constructor.add_field_and_value(
            DBFields.Products.name,
            result["name_string"][0]
        )
        products_query_constructor.add_field_and_value(
            DBFields.Products.description,
            result["desc_string"][0]
        )
        products_query_constructor.add_field_and_value(
            DBFields.Products.qty_in_stock,
            result["qty_in_stock_string"][0]
        )
        is_updated = update_record(products_query_constructor)

        if is_updated[0] == 1:
            flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    products_query_constructor.reset()
    products_query_constructor.add_condition_exact_value(
        DBFields.Products.gtin14,
        product_gtin14
    )
    selection = get_selected_records(products_query_constructor)
    if selection[0] == 0:
        details = selection[1]
        form.gtin14_string.data = details[0][0]
        form.name_string.data = details[0][1]
        form.desc_string.data = details[0][2]
        form.qty_in_stock_string.data = details[0][3]
        return render_template("detailsView/product.html", form=form, product_gtin14=product_gtin14, table_exists=False)
    return selection[1]


@app.route("/customer-orders/<customer_order_id>", methods=["GET", "POST"])
def show_customer_order_details_view(customer_order_id):
    form = CustomerOrderDetailsForm()

    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        customer_orders_query_constructor.reset()
        customer_orders_query_constructor.add_condition_exact_value(
            DBFields.CustomerOrders.id,
            customer_order_id
        )
        customer_orders_query_constructor.add_field_and_value(
            DBFields.CustomerOrders.delivery_date,
            result["customer_order_delivery_date_string"][0]
        )
        customer_orders_query_constructor.add_field_and_value(
            DBFields.CustomerOrders.delivery_location,
            result["delivery_location_string"][0]
        )
        is_updated = update_record(customer_orders_query_constructor)

        if is_updated[0] == 1:
            flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    customer_orders_query_constructor.reset()
    customer_orders_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrders.id,
        customer_order_id
    )
    selection = get_selected_records(customer_orders_query_constructor)
    customer_order_items_query_constructor.reset()
    customer_order_items_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrderItems.customer_order_id,
        customer_order_id
    )
    customer_order_items_selection = get_selected_records(customer_order_items_query_constructor)

    if selection[0] == 0 and customer_order_items_selection[0] == 0:
        details = selection[1]
        form.customer_order_id_string.data = details[0][0]
        form.customer_id_string.data = details[0][1]
        form.customer_order_datetime_ordered_string.data = details[0][2]
        form.customer_order_delivery_date_string.data = details[0][3]
        form.delivery_location_string.data = details[0][4]
        return render_template("detailsView/customerOrder.html", form=form, customer_order_id=customer_order_id,
                               table_exists=True, customer_order_items=customer_order_items_selection[1])
    return "{}\n{}".format(selection[1], customer_order_items_selection[1])


@app.route("/company-orders/<company_order_id>", methods=["GET", "POST"])
def show_company_order_details_view(company_order_id):
    form = CompanyOrderDetailsForm()

    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        company_orders_query_constructor.reset()
        company_orders_query_constructor.add_condition_exact_value(
            DBFields.CompanyOrders.id,
            company_order_id
        )
        company_orders_query_constructor.add_field_and_value(
            DBFields.CompanyOrders.qty_bought,
            result["company_order_qty_bought_string"][0]
        )
        company_orders_query_constructor.add_field_and_value(
            DBFields.CompanyOrders.delivery_date,
            result["company_order_delivery_date_string"][0]
        )
        is_updated = update_record(company_orders_query_constructor)

        if is_updated[0] == 1:
            flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    company_orders_query_constructor.reset()
    company_orders_query_constructor.add_condition_exact_value(
        DBFields.CompanyOrders.id,
        company_order_id
    )
    selection = get_selected_records(company_orders_query_constructor)
    if selection[0] == 0:
        details = selection[1]
        form.company_order_id_string.data = details[0][0]
        form.company_order_product_gtin14_string.data = details[0][1]
        form.company_order_datetime_ordered_string.data = details[0][2]
        form.company_order_qty_bought_string.data = details[0][3]
        form.company_order_delivery_date_string.data = details[0][4]
        return render_template("detailsView/companyOrder.html", form=form, company_order_id=company_order_id,
                               table_exists=False)
    return selection[1]


@app.route("/customers/<customer_id>/delete", methods=["GET", "POST"])
def delete_customer(customer_id):
    form = CustomerDetailsForm()
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        response_customer_id = result["customer_id_string"][0]
        if customer_id == response_customer_id:
            customers_query_constructor.reset()
            customers_query_constructor.add_condition_exact_value(
                DBFields.Customers.id,
                customer_id
            )
            is_deleted = delete_record(customers_query_constructor)
            if is_deleted[0] == 1:
                flash_danger(FLASH_RECORD_NOT_DELETED)
            else:
                flash_info(FLASH_RECORD_DELETED)
                return redirect(url_for("show_customers"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/customer.html", field=form.customer_id_string)


@app.route("/products/<product_gtin14>/delete", methods=["GET", "POST"])
def delete_product(product_gtin14):
    form = ProductDetailsForm()
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        response_product_id = result["gtin14_string"][0]
        if product_gtin14 == response_product_id:
            products_query_constructor.reset()
            products_query_constructor.add_condition_exact_value(
                DBFields.Products.gtin14,
                product_gtin14
            )
            is_deleted = delete_record(products_query_constructor)
            if is_deleted[0] == 1:
                flash_danger(FLASH_RECORD_NOT_DELETED)
            else:
                flash_info(FLASH_RECORD_DELETED)
                return redirect(url_for("show_products"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/product.html", field=form.gtin14_string)


@app.route("/customer-orders/<customer_order_id>/delete", methods=["GET", "POST"])
def delete_customer_order(customer_order_id):
    form = CustomerOrderDetailsForm()
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        response_customer_order_id = result["customer_order_id_string"][0]
        if customer_order_id == response_customer_order_id:
            customer_orders_query_constructor.reset()
            customer_orders_query_constructor.add_condition_exact_value(
                DBFields.CustomerOrders.id,
                customer_order_id
            )
            is_deleted = delete_record(customer_orders_query_constructor)
            if is_deleted[0] == 1:
                flash_danger(FLASH_RECORD_NOT_DELETED)
            else:
                flash_info(FLASH_RECORD_DELETED)
                return redirect(url_for("show_customer_orders"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/customerOrder.html", field=form.customer_order_id_string)


@app.route("/company-orders/<company_order_id>/delete", methods=["GET", "POST"])
def delete_company_order(company_order_id):
    form = CompanyOrderDetailsForm()
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        response_company_order_id = result["company_order_id_string"][0]
        if company_order_id == response_company_order_id:
            company_orders_query_constructor.reset()
            company_orders_query_constructor.add_condition_exact_value(
                DBFields.CompanyOrders.id,
                company_order_id
            )
            is_deleted = delete_record(company_orders_query_constructor)
            if is_deleted[0] == 1:
                flash_danger(FLASH_RECORD_NOT_DELETED)
            else:
                flash_info(FLASH_RECORD_DELETED)
                return redirect(url_for("show_company_orders"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/companyOrder.html", field=form.company_order_id_string)
