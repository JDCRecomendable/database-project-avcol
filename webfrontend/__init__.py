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
from webfrontend.forms.select_filters import CustomerOrdersDataFilterForm, CompanyOrderDataFilterForm


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

company_orders_query_constructor = QueryConstructor(
    DBSchemaTableNames.company_orders,
    DBSchemaTableNames.schema
)


def get_selected_records(query_constructor: QueryConstructor):
    """Get the select query for a particular table, using the QueryConstructor object assigned to it.
    :type query_constructor: QueryConstructor
    """
    query = query_constructor.render_select_query()
    selection = database_connector.execute_query(
        query,
        select=True
    )
    return selection


@app.route("/customers", methods=["GET", "POST"])
def show_customers():
    customers_query_constructor.reset()
    form = CustomersDataFilterForm()
    if request.method == "GET":
        return render_template("customers.html",
                               selection=get_selected_records(customers_query_constructor),
                               form=form)
    if not form.validate():
        return render_template("customers.html",
                               selection=get_selected_records(customers_query_constructor),
                               form=form)
    result = request.form.to_dict(flat=False)
    if result["first_name_selection"][0] == "filter":
        customers_query_constructor.add_condition_like(
            DBFields.Customers.first_name,
            result["first_name_string"][0],
            at_beginning=("first_name_at_beginning" in result),
            at_end=("first_name_at_end" in result)
        )
    if result["last_name_selection"][0] == "filter":
        customers_query_constructor.add_condition_like(
            DBFields.Customers.last_name,
            result["last_name_string"][0],
            at_beginning=("last_name_at_beginning" in result),
            at_end=("last_name_at_end" in result)
        )
    if result["email_address_selection"][0] == "filter":
        customers_query_constructor.add_condition_exact_value(
            DBFields.Customers.email_address,
            result["email_address_string"][0]
        )
    if result["phone_selection"][0] == "filter":
        customers_query_constructor.add_condition_exact_value(
            DBFields.Customers.phone,
            result["phone_string"][0]
        )
    if result["date_registered_selection"][0] == "filter":
        customers_query_constructor.add_condition_ranged_values(
            DBFields.Customers.date_registered,
            lower_limit=result["date_registered_lower_limit_string"][0],
            upper_limit=result["date_registered_upper_limit_string"][0]
        )
    if result["location_selection"][0] == "filter":
        # Get location IDs
        locations_query_constructor.reset()
        customer_locations_query_constructor.reset()
        locations_query_constructor.add_condition_like(
            DBFields.Locations.place_no,
            result["location_place_no"][0]
        )
        locations_query_constructor.add_condition_like(
            DBFields.Locations.road_name,
            result["location_road_name"][0]
        )
        locations_query_constructor.add_condition_like(
            DBFields.Locations.city,
            result["location_city"][0]
        )
        locations_query_constructor.add_field(DBFields.Locations.id)

        # Get customer IDs if they are in the selected location(s)
        customer_locations_query_constructor.add_nested_query(
            DBFields.CustomerLocations.location_id,
            locations_query_constructor.render_select_query()
        )
        customer_locations_query_constructor.add_field(DBFields.CustomerLocations.customer_id)

        # Get all customer details if their IDs are found in the selected customer locations
        customers_query_constructor.add_nested_query(
            DBFields.Customers.id,
            customer_locations_query_constructor.render_select_query()
        )
    return render_template("customers.html",
                           selection=get_selected_records(customers_query_constructor),
                           form=form)


@app.route("/products", methods=["GET", "POST"])
def show_products():
    products_query_constructor.reset()
    form = ProductsDataFilterForm()
    if request.method == "GET":
        return render_template("products.html",
                               selection=get_selected_records(products_query_constructor),
                               form=form)


@app.route("/customer-orders", methods=["GET", "POST"])
def show_customer_orders():
    customer_orders_query_constructor.reset()
    form = CustomerOrdersDataFilterForm()
    if request.method == "GET":
        return render_template("customerOrders.html",
                               selection=get_selected_records(customer_orders_query_constructor),
                               form=form)


@app.route("/company-orders", methods=["GET", "POST"])
def show_company_orders():
    company_orders_query_constructor.reset()
    form = CompanyOrderDataFilterForm()
    if request.method == "GET":
        return render_template("companyOrders.html",
                               selection=get_selected_records(company_orders_query_constructor),
                               form=form)
