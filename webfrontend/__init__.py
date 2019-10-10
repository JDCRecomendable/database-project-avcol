#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

# Import Utils from System
from flask import Flask, request, render_template, redirect, url_for
from os import urandom
from datetime import datetime

# Import Utils and Constants from Application
from base.constants import *
from webfrontend.constants import *
import webfrontend.utils
from webfrontend.utils import flash_success, flash_info, flash_danger, QueryConstructor

# Import Database Actions
from webfrontend.utils import get_selected_records, update_record, add_record, delete_record
from webfrontend.utils import filter_customer_selection, filter_product_selection
from webfrontend.utils import filter_customer_order_selection, filter_company_order_selection
from webfrontend.utils import filter_location_selection

# Import Web Interface Forms
from webfrontend.forms.select_filters import CustomersDataFilterForm, ProductsDataFilterForm
from webfrontend.forms.select_filters import CustomerOrdersDataFilterForm, CompanyOrdersDataFilterForm
from webfrontend.forms.data_fields import CustomerDetailsForm, ProductDetailsForm
from webfrontend.forms.data_fields import CustomerOrderDetailsForm, CompanyOrderDetailsForm


# Prepare Flask (Web Interface) App
app = Flask(__name__)
app.secret_key = urandom(16)

# Create the Query Constructor Objects
customers_query_constructor = QueryConstructor(DBSchemaTableNames.customers, DBSchemaTableNames.schema)
locations_query_constructor = QueryConstructor(DBSchemaTableNames.locations, DBSchemaTableNames.schema)
customer_locations_query_constructor = QueryConstructor(DBSchemaTableNames.customer_locations,
                                                        DBSchemaTableNames.schema)
products_query_constructor = QueryConstructor(DBSchemaTableNames.products, DBSchemaTableNames.schema)
customer_orders_query_constructor = QueryConstructor(DBSchemaTableNames.customer_orders, DBSchemaTableNames.schema)
customer_order_items_query_constructor = QueryConstructor(DBSchemaTableNames.customer_order_items,
                                                          DBSchemaTableNames.schema)
company_orders_query_constructor = QueryConstructor(DBSchemaTableNames.company_orders, DBSchemaTableNames.schema)

# Assign the Query Constructor Objects as Variables in Utils for use
webfrontend.utils.customers_query_constructor = customers_query_constructor
webfrontend.utils.locations_query_constructor = locations_query_constructor
webfrontend.utils.customer_locations_query_constructor = customer_locations_query_constructor
webfrontend.utils.products_query_constructor = products_query_constructor
webfrontend.utils.customer_orders_query_constructor = customer_orders_query_constructor
webfrontend.utils.customer_order_items_query_constructor = customer_order_items_query_constructor
webfrontend.utils.company_orders_query_constructor = company_orders_query_constructor


# WEB INTERFACE ROUTING
# Show Data
@app.route("/customers/", methods=["GET", "POST"])
def list_customers():
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
        return render_template("dataTables/customers.html", selection=selection[1], form=form, link_name="customers")
    return selection[1]


@app.route("/products/", methods=["GET", "POST"])
def list_products():
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
        return render_template("dataTables/products.html", selection=selection[1], form=form, link_name="products")
    return selection[1]


@app.route("/customer-orders/", methods=["GET", "POST"])
def list_customer_orders():
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
        return render_template("dataTables/customerOrders.html", selection=selection[1], form=form,
                               link_name="customer-orders")
    return selection[1]


@app.route("/company-orders/", methods=["GET", "POST"])
def list_company_orders():
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
        return render_template("dataTables/companyOrders.html", selection=selection[1], form=form,
                               link_name="company-orders")
    return selection[1]


# WEB INTERFACE ROUTING
# Show Record Details
@app.route("/customers/<customer_id>", methods=["GET", "POST"])
def show_customer_details(customer_id):
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
def show_product_details(product_gtin14):
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
def show_customer_order_details(customer_order_id):
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
def show_company_order_details(company_order_id):
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


# WEB INTERFACE ROUTING
# Add Records
@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    form = CustomerDetailsForm()
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        first_name = result["first_name_string"][0]
        last_name = result["last_name_string"][0]
        email_address = result["email_address_string"][0]
        phone = result["phone_string"][0]
        values = [first_name, last_name, email_address, phone]
        is_added = add_record(DBQueryFilePath.add_customer, values)
        if is_added[0] == 1:
            flash_danger(FLASH_ERROR.format(is_added[1]))
        else:
            flash_success(FLASH_RECORD_ADDED)
            customers_query_constructor.reset()
            customers_query_constructor.add_condition_exact_value(
                DBFields.Customers.email_address,
                email_address
            )
            customers_query_constructor.add_field(
                DBFields.Customers.id
            )

            selection = get_selected_records(customers_query_constructor)
            if selection[0] == 1:
                flash_danger(FLASH_ERROR.format(selection[1]))
            else:
                customer_id = selection[1][0][0]
                return redirect(url_for("show_customer_details", customer_id=customer_id))
    return render_template("addition/customer.html", form=form)


@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    form = ProductDetailsForm()
    form.qty_in_stock_string.data = 0
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        gtin14 = result["gtin14_string"][0]
        name = result["name_string"][0]
        description = result["desc_string"][0]
        qty_in_stock = result["qty_in_stock_string"][0]
        values = [gtin14, name, description, qty_in_stock]
        is_added = add_record(DBQueryFilePath.add_product, values)
        if is_added[0] == 1:
            flash_danger(FLASH_ERROR.format(is_added[1]))
        else:
            flash_success(FLASH_RECORD_ADDED)
            products_query_constructor.reset()
            products_query_constructor.add_condition_exact_value(
                DBFields.Products.gtin14,
                gtin14
            )
            products_query_constructor.add_field(DBFields.Products.gtin14)
            selection = get_selected_records(products_query_constructor)
            if selection[0] == 1:
                flash_danger(FLASH_ERROR.format(selection[1]))
            else:
                product_gtin14 = selection[1][0][0]
                return redirect(url_for("show_product_details", product_gtin14=product_gtin14))
    return render_template("addition/product.html", form=form)


@app.route("/customer-orders/add", methods=["GET", "POST"])
def add_customer_order():
    form = CustomerOrderDetailsForm()
    form.customer_order_delivery_date_string.data = datetime.now()
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        datetime_ordered = str(datetime.now())[:19]
        customer_id = result["customer_id_string"][0]
        delivery_date = result["customer_order_delivery_date_string"][0]
        delivery_location = result["delivery_location_string"][0]
        values = [customer_id, datetime_ordered, delivery_date, delivery_location]
        is_added = add_record(DBQueryFilePath.add_customer_order, values)
        if is_added[0] == 1:
            flash_danger(FLASH_ERROR.format(is_added[1]))
        else:
            flash_success(FLASH_RECORD_ADDED)
            customer_orders_query_constructor.reset()
            customer_orders_query_constructor.add_condition_exact_value(
                DBFields.CustomerOrders.customer_id,
                customer_id
            )
            customer_orders_query_constructor.add_condition_exact_value(
                DBFields.CustomerOrders.datetime_ordered,
                datetime_ordered
            )
            customer_orders_query_constructor.add_field(
                DBFields.CustomerOrders.id
            )

            selection = get_selected_records(customer_orders_query_constructor)
            if selection[0] == 1:
                flash_danger(FLASH_ERROR.format(selection[1]))
            else:
                customer_order_id = selection[1][0][0]
                return redirect(url_for("show_customer_order_details", customer_order_id=customer_order_id))
    return render_template("addition/customerOrder.html", form=form)


@app.route("/company-orders/add", methods=["GET", "POST"])
def add_company_order():
    form = CompanyOrderDetailsForm()
    form.company_order_delivery_date_string.data = datetime.now()
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        datetime_ordered = str(datetime.now())[:19]
        product_gtin14 = result["company_order_product_gtin14_string"][0]
        qty_bought = result["company_order_qty_bought_string"][0]
        delivery_date = result["company_order_delivery_date_string"][0]
        values = [product_gtin14, datetime_ordered, qty_bought, delivery_date]
        is_added = add_record(DBQueryFilePath.add_company_order, values)
        if is_added[0] == 1:
            flash_danger(FLASH_ERROR.format(is_added[1]))
        else:
            flash_success(FLASH_RECORD_ADDED)
            company_orders_query_constructor.reset()
            company_orders_query_constructor.add_condition_exact_value(
                DBFields.CompanyOrders.product_gtin14,
                product_gtin14
            )
            company_orders_query_constructor.add_condition_exact_value(
                DBFields.CompanyOrders.datetime_ordered,
                datetime_ordered
            )
            company_orders_query_constructor.add_field(
                DBFields.CompanyOrders.id
            )

            selection = get_selected_records(company_orders_query_constructor)
            if selection[0] == 1:
                flash_danger(FLASH_ERROR.format(selection[1]))
            else:
                company_order_id = selection[1][0][0]
                return redirect(url_for("show_company_order_details", company_order_id=company_order_id))
    return render_template("addition/companyOrder.html", form=form)


# WEB INTERFACE ROUTING
# Delete Records
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
                return redirect(url_for("list_customers"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/customer.html", field=form.customer_id_string, record_id=customer_id)


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
                return redirect(url_for("list_products"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/product.html", field=form.gtin14_string, record_id=product_gtin14)


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
                return redirect(url_for("list_customer_orders"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/customerOrder.html", field=form.customer_order_id_string,
                           record_id=customer_order_id)


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
                return redirect(url_for("list_company_orders"))
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("deletion/companyOrder.html", field=form.company_order_id_string, record_id=company_order_id)
