#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

# Import Utils from System
from flask import Flask, request, render_template, redirect, url_for, make_response
from os import urandom
from datetime import datetime

# Import Utils and Constants from Application
from base.constants import *
from webfrontend.constants import *
import webfrontend.utils
from webfrontend.utils import flash_success, flash_info, flash_danger, QueryConstructor, prepare_for_latin1
from pdf_report import PDF

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
from webfrontend.forms.data_fields import CustomerLocationsDetailsForm, CustomerOrderItemDetailsForm


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
# Default
@app.route("/")
def default_route():
    return redirect(url_for("list_customers"))


# WEB INTERFACE ROUTING
# Display Reports
@app.route("/customers/report")
def report_customers():
    customers_query_constructor.reset()
    customers_query_constructor.add_order(DBFields.Customers.id, ascending=True)
    selection = get_selected_records(customers_query_constructor)
    if selection[0] == 0:
        pdf = PDF("Online Shop Logistics Management", "Selection of Customers", "View of All Customers")
        for record in selection[1]:
            pdf.auto_write("Customer {}".format(prepare_for_latin1(record[0])), fill=1)

            pdf.auto_write("Name:", width=20, line_break=0)
            pdf.auto_write("{} {}".format(prepare_for_latin1(record[2]), prepare_for_latin1(record[1])))

            pdf.auto_write("Email:", width=20, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[3])))

            pdf.auto_write("Phone:", width=20, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[4])))

            pdf.ln()
        response = make_response(pdf.output(dest="S").encode("latin-1"))
        response.headers.set('Content-Disposition', 'inline', filename='Report.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response
    return selection[1]


@app.route("/products/report")
def report_products():
    products_query_constructor.reset()
    products_query_constructor.add_order(DBFields.Products.gtin14, ascending=True)
    selection = get_selected_records(products_query_constructor)
    if selection[0] == 0:
        pdf = PDF("Online Shop Logistics Management", "Selection of Products", "View of All Products")
        for record in selection[1]:
            pdf.auto_write("Product {}".format(prepare_for_latin1(record[0])), fill=1)

            pdf.auto_write("Name:", width=32, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[1])))

            pdf.auto_write("Qty in Stock:", width=32, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[3])))

            if len(record[2]):
                pdf.auto_write("Description:", width=32, line_break=1)
                pdf.write(5, "{}".format(prepare_for_latin1(record[2])))
                pdf.ln()

            pdf.ln()
            pdf.ln()
        response = make_response(pdf.output(dest="S").encode("latin-1", "replace"))
        response.headers.set('Content-Disposition', 'inline', filename='Report.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response
    return selection[1]


@app.route("/customer-orders/report")
def report_customer_orders():
    customer_orders_query_constructor.reset()
    customer_orders_query_constructor.add_order(DBFields.CustomerOrders.id, ascending=True)
    selection = get_selected_records(customer_orders_query_constructor)
    if selection[0] == 0:
        pdf = PDF("Online Shop Logistics Management", "Selection of Customer Orders", "View of All Customer Orders")
        for record in selection[1]:
            pdf.auto_write("Customer Order {}".format(prepare_for_latin1(record[0])), fill=1)

            customers_query_constructor.reset()
            customers_query_constructor.add_condition_exact_value(DBFields.Customers.id, str(record[1]))
            customers_query_constructor.add_field(DBFields.Customers.first_name)
            customers_query_constructor.add_field(DBFields.Customers.last_name)
            name = get_selected_records(customers_query_constructor)[1][0]
            pdf.auto_write("Customer:", width=44, line_break=0)
            pdf.auto_write("[{}] {} {}".format(prepare_for_latin1(record[1]), name[0], name[1]))

            pdf.auto_write("Date/Time Ordered", width=44, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[2])))

            pdf.auto_write("Target Delivery Date:", width=44, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[3])))

            locations_query_constructor.reset()
            locations_query_constructor.add_condition_exact_value(DBFields.Locations.id, str(record[4]))
            locations_query_constructor.add_field(DBFields.Locations.place_no)
            locations_query_constructor.add_field(DBFields.Locations.road_name)
            locations_query_constructor.add_field(DBFields.Locations.city)
            location = get_selected_records(locations_query_constructor)[1][0]
            pdf.auto_write("Delivery Location:", width=44, line_break=0)
            pdf.auto_write("{} {}, {}".format(prepare_for_latin1(location[0]), prepare_for_latin1(location[1]),
                                              prepare_for_latin1(location[2])))

            pdf.ln()
        response = make_response(pdf.output(dest="S").encode("latin-1"))
        response.headers.set('Content-Disposition', 'inline', filename='Report.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response
    return selection[1]


@app.route("/company-orders/report")
def report_company_orders():
    company_orders_query_constructor.reset()
    company_orders_query_constructor.add_order(DBFields.CompanyOrders.id, ascending=True)
    selection = get_selected_records(company_orders_query_constructor)
    if selection[0] == 0:
        pdf = PDF("Online Shop Logistics Management", "Selection of Company Orders", "View of All Company Orders")
        for record in selection[1]:
            pdf.auto_write("Company Order {}".format(prepare_for_latin1(record[0])), fill=1)

            products_query_constructor.reset()
            products_query_constructor.add_condition_exact_value(DBFields.Products.gtin14, str(record[1]))
            products_query_constructor.add_field(DBFields.Products.name)
            product = get_selected_records(products_query_constructor)[1][0]
            pdf.auto_write("Product:", width=44, line_break=0)
            pdf.auto_write("[{}] {}".format(prepare_for_latin1(record[1]), prepare_for_latin1(product[0])))

            pdf.auto_write("Qty Bought:", width=44, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[3])))

            pdf.auto_write("Date/Time Ordered:", width=44, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[2])))

            pdf.auto_write("Target Delivery Date:", width=44, line_break=0)
            pdf.auto_write("{}".format(prepare_for_latin1(record[4])))

            pdf.ln()
        response = make_response(pdf.output(dest="S").encode("latin-1", "replace"))
        response.headers.set('Content-Disposition', 'inline', filename='Report.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response
    return selection[1]


# WEB INTERFACE ROUTING
# Show Data
@app.route("/customers/", methods=["GET", "POST"])
def list_customers():
    form = CustomersDataFilterForm()

    customers_query_constructor.reset()
    customers_query_constructor.add_order(DBFields.Customers.id, ascending=True)
    if request.method == "POST":
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
    products_query_constructor.add_order(DBFields.Products.gtin14, ascending=True)
    if request.method == "POST":
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
    customer_orders_query_constructor.add_order(DBFields.CustomerOrders.id, ascending=True)
    if request.method == "POST":
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
    company_orders_query_constructor.add_order(DBFields.CompanyOrders.id, ascending=True)
    if request.method == "POST":
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
# Show/Update Record Details (except Customer Order Items)
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
            if "HY000" in is_updated[1] and "3819" in is_updated[1]:
                    flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_updated[1] and "1452" in is_updated[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
                flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    customers_query_constructor.reset()
    customers_query_constructor.add_condition_exact_value(
        DBFields.Customers.id,
        customer_id
    )
    selection = get_selected_records(customers_query_constructor)
    details = selection[1]

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

    if selection[0] == 0 and not details:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_customers"))
    elif selection[0] == 0 and location_selection[0] == 0:
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
            if "HY000" in is_updated[1] and "3819" in is_updated[1]:
                    flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_updated[1] and "1452" in is_updated[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
                flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    products_query_constructor.reset()
    products_query_constructor.add_condition_exact_value(
        DBFields.Products.gtin14,
        product_gtin14
    )
    selection = get_selected_records(products_query_constructor)
    details = selection[1]

    if selection[0] == 0 and not details:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_products"))
    elif selection[0] == 0:
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
            if "HY000" in is_updated[1] and "3819" in is_updated[1]:
                    flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_updated[1] and "1452" in is_updated[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
                flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    customer_orders_query_constructor.reset()
    customer_orders_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrders.id,
        customer_order_id
    )
    selection = get_selected_records(customer_orders_query_constructor)
    details = selection[1]

    customer_order_items_query_constructor.reset()
    customer_order_items_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrderItems.customer_order_id,
        customer_order_id
    )
    customer_order_items_selection = get_selected_records(customer_order_items_query_constructor)

    if selection[0] == 0 and not details:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_customer_orders"))
    elif selection[0] == 0 and customer_order_items_selection[0] == 0:
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
            if "HY000" in is_updated[1] and "3819" in is_updated[1]:
                    flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_updated[1] and "1452" in is_updated[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
                flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)

    company_orders_query_constructor.reset()
    company_orders_query_constructor.add_condition_exact_value(
        DBFields.CompanyOrders.id,
        company_order_id
    )
    selection = get_selected_records(company_orders_query_constructor)
    details = selection[1]

    if selection[0] == 0 and not details:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_company_orders"))
    elif selection[0] == 0:
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
            if "HY000" in is_added[1] and "3819" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_added[1] and "1452" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
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


@app.route("/customers/<customer_id>/add-location", methods=["GET", "POST"])
def add_customer_location(customer_id):
    # check if customer exists
    customers_query_constructor.reset()
    customers_query_constructor.add_condition_exact_value(DBFields.Customers.id, customer_id)
    selection = get_selected_records(customers_query_constructor)
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_customers"))
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("list_customers"))

    form = CustomerLocationsDetailsForm()
    form.customer_id_string.data = customer_id
    if request.method == "POST":
        # get the city, road name and place no. from the form results
        result = request.form.to_dict(flat=False)
        city = result["city_name_string"][0]
        road_name = result["road_name_string"][0]
        place_no = result["place_no_string"][0]

        # find out if location already exists, and set the location query constructor conditions accordingly
        locations_query_constructor.reset()
        locations_query_constructor.add_condition_like(DBFields.Locations.city, city)
        locations_query_constructor.add_condition_exact_value(DBFields.Locations.road_name, road_name)
        locations_query_constructor.add_condition_exact_value(DBFields.Locations.place_no, place_no)
        locations_query_constructor.add_field(DBFields.Locations.id)
        selection = get_selected_records(locations_query_constructor)
        # stop and display errors at next screen if errors are found
        if selection[0] == 1:
            flash_danger(FLASH_ERROR.format(selection[1]))
            return redirect(url_for("add_customer_location", customer_id=customer_id))

        # check for any ID present, which means location exists, otherwise, must create new location
        selection = selection[1]
        # if no ID present, create new location
        if not selection:
            # insert into database the new location record
            values = [city, road_name, place_no]
            is_added = add_record(DBQueryFilePath.add_location, values)
            # check for any errors in inserting the record
            if is_added[0] == 1:
                if "HY000" in is_added[1] and "3819" in is_added[1]:
                    flash_danger(FLASH_INVALID_INPUT_TO_ADD)
                elif "23000" in is_added[1] and "1452" in is_added[1]:
                    flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
                else:
                    flash_danger(FLASH_ERROR.format(is_added[1]))
                return redirect(url_for("add_customer_location", customer_id=customer_id))

            # retrieve the ID of the newly-inserted record, using the exact same location query conditions set earlier
            location_target = get_selected_records(locations_query_constructor)
            # check for any errors in retrieving the ID of the newly-inserted record
            if location_target[0] == 1:
                flash_danger(FLASH_ERROR.format(is_added[1]))
                return redirect(url_for("add_customer_location", customer_id=customer_id))

            # set the ID to that of the newly-created location
            location_id = location_target[1][0][0]
        # otherwise, if ID is present, then location must be present, so use the ID of that location
        else:
            location_id = selection[0][0]

        # after finding existing or creating new location record, create now the customer location record
        values = [customer_id, location_id]
        is_added = add_record(DBQueryFilePath.add_customer_location, values)
        # check for any errors in adding the new customer location record
        if is_added[0] == 1:
            if "HY000" in is_added[1] and "3819" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_added[1] and "1452" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
                flash_danger(FLASH_ERROR.format(is_added[1]))
            return redirect(url_for("add_customer_location", customer_id=customer_id))

        # if customer location record successfuly added, redirect back to the customer details, where the new location
        # must be shown
        flash_success(FLASH_RECORD_ADDED)
        return redirect(url_for("show_customer_details", customer_id=customer_id))
    return render_template("addition/customerLocation.html", form=form)


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
            if "HY000" in is_added[1] and "3819" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_added[1] and "1452" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
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
            if "HY000" in is_added[1] and "3819" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_added[1] and "1452" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
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


@app.route("/customer-orders/<customer_order_id>/add-item", methods=["GET", "POST"])
def add_customer_order_item(customer_order_id):
    customer_orders_query_constructor.reset()
    customer_orders_query_constructor.add_condition_exact_value(DBFields.CustomerOrders.id, customer_order_id)
    selection = get_selected_records(customer_orders_query_constructor)
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_customer_orders"))
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("list_customer_orders"))

    form = CustomerOrderItemDetailsForm()
    form.customer_order_id_string.data = customer_order_id
    form.qty_bought_string.data = 1
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        product_gtin14 = result["product_gtin14_string"][0]
        qty_bought = result["qty_bought_string"][0]
        values = [customer_order_id, product_gtin14, qty_bought]
        is_added = add_record(DBQueryFilePath.add_customer_order_item, values)
        if is_added[0] == 1:
            if "HY000" in is_added[1] and "3819" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_added[1] and "1452" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
                flash_danger(FLASH_ERROR.format(is_added[1]))
            return redirect(url_for("add_customer_order_item", customer_order_id=customer_order_id))
        flash_success(FLASH_RECORD_ADDED)
        return redirect(url_for("show_customer_order_details", customer_order_id=customer_order_id))
    return render_template("addition/customerOrderItem.html", form=form)


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
            if "HY000" in is_added[1] and "3819" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_added[1] and "1452" in is_added[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
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
# Update Customer Order Items
@app.route("/customer-orders/<customer_order_id>/update-item/<product_gtin14>", methods=["GET", "POST"])
def update_customer_order_item(customer_order_id, product_gtin14):
    form = CustomerOrderItemDetailsForm()

    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        customer_order_items_query_constructor.reset()
        customer_order_items_query_constructor.add_condition_exact_value(
            DBFields.CustomerOrderItems.customer_order_id,
            customer_order_id
        )
        customer_order_items_query_constructor.add_condition_exact_value(
            DBFields.CustomerOrderItems.product_gtin14,
            product_gtin14
        )
        customer_order_items_query_constructor.add_field_and_value(
            DBFields.CustomerOrderItems.product_gtin14,
            result["product_gtin14_string"][0]
        )
        customer_order_items_query_constructor.add_field_and_value(
            DBFields.CustomerOrderItems.qty_bought,
            result["qty_bought_string"][0]
        )
        is_updated = update_record(customer_order_items_query_constructor)

        if is_updated[0] == 1:
            if "HY000" in is_updated[1] and "3819" in is_updated[1]:
                    flash_danger(FLASH_INVALID_INPUT_TO_ADD)
            elif "23000" in is_updated[1] and "1452" in is_updated[1]:
                flash_danger(FLASH_INVALID_INPUT_KEY_CONSTRAINT)
            else:
                flash_danger(FLASH_ERROR.format(is_updated[1]))
        else:
            flash_success(FLASH_RECORD_UPDATED)
            return redirect(url_for("show_customer_order_details", customer_order_id=customer_order_id))

    customer_order_items_query_constructor.reset()
    customer_order_items_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrderItems.customer_order_id,
        customer_order_id
    )
    customer_order_items_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrderItems.product_gtin14,
        product_gtin14
    )
    selection = get_selected_records(customer_order_items_query_constructor)
    details = selection[1]

    if selection[0] == 1 or (selection[0] == 0 and not details):
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("show_customer_order_details", customer_order_id=customer_order_id))
    else:
        form.customer_order_id_string.data = details[0][0]
        form.product_gtin14_string.data = details[0][1]
        form.qty_bought_string.data = details[0][2]
        return render_template("update/customerOrderItem.html", form=form)


# WEB INTERFACE ROUTING
# Delete Records
@app.route("/customers/<customer_id>/delete", methods=["GET", "POST"])
def delete_customer(customer_id):
    customers_query_constructor.reset()
    customers_query_constructor.add_condition_exact_value(
        DBFields.Customers.id,
        customer_id
    )
    selection = get_selected_records(customers_query_constructor)
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_customers"))
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("list_customers"))

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


@app.route("/customers/<customer_id>/delete-location/<location_id>")
def delete_customer_location(customer_id,  location_id):
    customer_locations_query_constructor.reset()
    customer_locations_query_constructor.add_condition_exact_value(
        DBFields.CustomerLocations.location_id,
        location_id
    )
    customer_locations_query_constructor.add_condition_exact_value(
        DBFields.CustomerLocations.customer_id,
        customer_id
    )
    selection = get_selected_records(customer_locations_query_constructor)
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("show_customer_details", customer_id=customer_id))
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("show_customer_details", customer_id=customer_id))

    customer_locations_query_constructor.reset()
    customer_locations_query_constructor.add_condition_exact_value(DBFields.CustomerLocations.location_id, location_id)
    selection = get_selected_records(customer_locations_query_constructor)
    if selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("show_customer_details", customer_id=customer_id))
    count = len(selection[1])
    customer_locations_query_constructor.add_condition_exact_value(DBFields.CustomerLocations.customer_id, customer_id)
    is_deleted = delete_record(customer_locations_query_constructor)
    if is_deleted[0] == 1:
        flash_danger(FLASH_RECORD_NOT_DELETED)
    else:
        flash_info(FLASH_RECORD_DELETED)
        if not count > 1:
            locations_query_constructor.reset()
            locations_query_constructor.add_condition_exact_value(DBFields.Locations.id, location_id)
            is_deleted = delete_record(locations_query_constructor)
            if is_deleted[0] == 1:
                flash_danger(is_deleted[1])
    return redirect(url_for("show_customer_details", customer_id=customer_id))


@app.route("/products/<product_gtin14>/delete", methods=["GET", "POST"])
def delete_product(product_gtin14):
    products_query_constructor.reset()
    products_query_constructor.add_condition_exact_value(
        DBFields.Products.gtin14,
        product_gtin14
    )
    selection = get_selected_records(products_query_constructor)
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_products"))
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("list_products"))

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
    customer_orders_query_constructor.reset()
    customer_orders_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrders.id,
        customer_order_id
    )
    selection = get_selected_records(customer_orders_query_constructor)
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_customer_orders"))
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("list_customer_orders"))

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


@app.route("/customer-orders/<customer_order_id>/delete-item/<product_gtin14>")
def delete_customer_order_item(customer_order_id, product_gtin14):
    customer_order_items_query_constructor.reset()
    customer_order_items_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrderItems.customer_order_id,
        customer_order_id
    )
    customer_order_items_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrderItems.product_gtin14,
        product_gtin14
    )
    is_deleted = delete_record(customer_order_items_query_constructor)
    if is_deleted[0] == 1:
        flash_danger(FLASH_RECORD_NOT_DELETED)
    else:
        flash_info(FLASH_RECORD_DELETED)
    return redirect(url_for("show_customer_order_details", customer_order_id=customer_order_id))


@app.route("/company-orders/<company_order_id>/delete", methods=["GET", "POST"])
def delete_company_order(company_order_id):
    company_orders_query_constructor.reset()
    company_orders_query_constructor.add_condition_exact_value(
        DBFields.CompanyOrders.id,
        company_order_id
    )
    selection = get_selected_records(company_orders_query_constructor)
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_company_orders"))
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("list_company_orders"))

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


# WEB INTERFACE ROUTING
# Confirm Orders
@app.route("/customer-orders/<customer_order_id>/confirm", methods=["GET", "POST"])
def confirm_customer_order(customer_order_id):
    # ensure that customer order exists
    customer_orders_query_constructor.reset()
    customer_orders_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrders.id,
        customer_order_id
    )
    selection = get_selected_records(customer_orders_query_constructor)
    # if customer order does not exist, redirect to customer order listing and show that it does not exist
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_customer_orders"))
    # else show any other error and stop operation immediately
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("show_customer_order_details", customer_order_id=customer_order_id))

    form = CustomerOrderDetailsForm()

    # also obtain the customer order items involved
    customer_order_items_query_constructor.reset()
    customer_order_items_query_constructor.add_condition_exact_value(
        DBFields.CustomerOrderItems.customer_order_id,
        customer_order_id
    )
    # show any error and stop operation immediately
    selection = get_selected_records(customer_order_items_query_constructor)
    if selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("show_customer_order_details", customer_order_id=customer_order_id))

    # if user submitted the form
    if request.method == "POST":
        result = request.form.to_dict(flat=False)

        # confirm that user intends to confirm customer order
        response_customer_order_id = result["customer_order_id_string"][0]
        # if user submits expected answer
        if customer_order_id == response_customer_order_id:
            # check that all intended order will not deplete product qty in stock to negative
            not_exceeding_stock = True
            qty_after_order = []
            for item in selection[1]:
                products_query_constructor.reset()
                products_query_constructor.add_condition_exact_value(
                    DBFields.Products.gtin14,
                    item[1]
                )
                products_query_constructor.add_field(DBFields.Products.qty_in_stock)
                qty_left = get_selected_records(products_query_constructor)
                if qty_left[0] == 1:
                    flash_danger(FLASH_ERROR.format(qty_left[1]))
                    return redirect(url_for("confirm_customer_order", customer_order_id=customer_order_id))
                elif qty_left[0] == 0 and qty_left[1]:
                    qty = qty_left[1][0][0]
                    if int(qty) < int(item[2]):
                        not_exceeding_stock = False
                        break
                    qty_after_order.append(int(qty) - int(item[2]))

            # if intended order will indeed not deplete product qty in stock to negative
            if not_exceeding_stock:
                # decrease the product qty in stock as the order will involve taking the product(s)
                for item in selection[1]:
                    products_query_constructor.reset()
                    products_query_constructor.add_condition_exact_value(
                        DBFields.Products.gtin14,
                        item[1]
                    )
                    products_query_constructor.add_field_and_value(
                        DBFields.Products.qty_in_stock,
                        str(qty_after_order[0])
                    )
                    qty_after_order.pop(0)
                    is_updated = update_record(products_query_constructor)
                    if is_updated[0] == 1:
                        flash_danger(FLASH_ERROR.format(is_updated[1]))
                        return redirect(url_for("confirm_customer_order", customer_order_id=customer_order_id))

                # then delete the customer order items
                customer_order_items_query_constructor.reset()
                customer_order_items_query_constructor.add_condition_exact_value(
                    DBFields.CustomerOrderItems.customer_order_id,
                    customer_order_id
                )
                is_deleted = delete_record(customer_order_items_query_constructor)
                if is_deleted[0] == 1:
                    flash_danger(FLASH_ERROR.format(is_deleted[1]))

                # finally, delete customer order
                customer_orders_query_constructor.reset()
                customer_orders_query_constructor.add_condition_exact_value(
                    DBFields.CustomerOrders.id,
                    customer_order_id
                )
                is_deleted = delete_record(customer_orders_query_constructor)
                if is_deleted[0] == 0:
                    flash_success(FLASH_ORDER_FULFILLED)
                    return redirect(url_for("list_customer_orders"))
                else:
                    flash_danger(FLASH_ERROR.format(is_deleted[1]))
            else:
                flash_danger(FLASH_NOT_ENOUGH_STOCK)
        # otherwise, show user that he/she did not submit correct answer
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("confirmation/customerOrder.html", field=form.customer_order_id_string,
                           order_type="customer", order_type_capitalised="Customer", id=customer_order_id,
                           customer_order_items=selection[1])


@app.route("/company-orders/<company_order_id>/confirm", methods=["GET", "POST"])
def confirm_company_order(company_order_id):
    # ensure that company order exists
    company_orders_query_constructor.reset()
    company_orders_query_constructor.add_condition_exact_value(
        DBFields.CompanyOrders.id,
        company_order_id
    )
    selection = get_selected_records(company_orders_query_constructor)
    # if company order does not exist, redirect to company order listing and show that it does not exist
    if selection[0] == 0 and not selection[1]:
        flash_danger(FLASH_RECORD_NOT_EXISTS)
        return redirect(url_for("list_company_orders"))
    # else show any other error and stop operation immediately
    elif selection[0] == 1:
        flash_danger(FLASH_ERROR.format(selection[1]))
        return redirect(url_for("show_company_order_details", company_order_id=company_order_id))

    # also obtain the product involved and qty ordered in the company order if it exists
    product_gtin14 = selection[1][0][1]
    qty_ordered = selection[1][0][3]

    form = CompanyOrderDetailsForm()

    # if user submitted the form
    if request.method == "POST":
        result = request.form.to_dict(flat=False)
        # confirm that user intends to confirm company order
        response_company_order_id = result["company_order_id_string"][0]
        # if user submits expected answer
        if company_order_id == response_company_order_id:
            # get current qty in stock of product
            products_query_constructor.reset()
            products_query_constructor.add_condition_exact_value(
                DBFields.Products.gtin14,
                product_gtin14
            )
            products_query_constructor.add_field(DBFields.Products.qty_in_stock)
            selection = get_selected_records(products_query_constructor)
            if selection[0] == 1:
                flash_danger(FLASH_ERROR.format(selection[1]))
                return redirect(url_for("confirm_company_order", company_order_id=company_order_id))

            # then attempt to increase the qty in stock as the company order will add product stockpile
            current_qty = int(selection[1][0][0])
            new_qty = current_qty + qty_ordered
            products_query_constructor.add_value(str(new_qty))
            is_updated = update_record(products_query_constructor)
            if is_updated[0] == 1:
                flash_danger(FLASH_ERROR.format(selection[1]))
                return redirect(url_for("confirm_company_order", company_order_id=company_order_id))

            # finally, delete company order to finish the operation
            company_orders_query_constructor.reset()
            company_orders_query_constructor.add_condition_exact_value(
                DBFields.CompanyOrders.id,
                company_order_id
            )
            is_deleted = delete_record(company_orders_query_constructor)
            if is_deleted[0] == 0:
                flash_success(FLASH_ORDER_FULFILLED)
                return redirect(url_for("list_company_orders"))
            else:
                flash_danger(FLASH_ERROR.format(is_deleted[1]))
        # otherwise, show user that he/she did not submit correct answer
        else:
            flash_danger(FLASH_RECORD_ID_NO_MATCH)
    return render_template("confirmation/companyOrder.html", field=form.company_order_id_string,
                           order_type="company", order_type_capitalised="Company", id=company_order_id,
                           product_gtin14=product_gtin14, qty_ordered=qty_ordered)
