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


def get_select_all_records(query_constructor: QueryConstructor):
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
                               selection=get_select_all_records(customers_query_constructor),
                               form=form)


@app.route("/products", methods=["GET", "POST"])
def show_products():
    products_query_constructor.reset()
    form = ProductsDataFilterForm()
    if request.method == "GET":
        return render_template("products.html",
                               selection=get_select_all_records(products_query_constructor),
                               form=form)


@app.route("/customer-orders", methods=["GET", "POST"])
def show_customer_orders():
    customer_orders_query_constructor.reset()
    form = CustomerOrdersDataFilterForm()
    if request.method == "GET":
        return render_template("customerOrders.html",
                               selection=get_select_all_records(customer_orders_query_constructor),
                               form=form)


@app.route("/company-orders", methods=["GET", "POST"])
def show_company_orders():
    company_orders_query_constructor.reset()
    form = CompanyOrderDataFilterForm()
    if request.method == "GET":
        return render_template("companyOrders.html",
                               selection=get_select_all_records(company_orders_query_constructor),
                               form=form)
