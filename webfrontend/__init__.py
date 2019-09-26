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
    if request.method == "GET":
        return render_template("customers.html", selection=get_select_all_records(customers_query_constructor))


@app.route("/products", methods=["GET", "POST"])
def show_products():
    if request.method == "GET":
        return render_template("products.html", selection=get_select_all_records(products_query_constructor))


@app.route("/customer-orders", methods=["GET", "POST"])
def show_customer_orders():
    if request.method == "GET":
        return render_template("customerOrders.html", selection=get_select_all_records(customer_orders_query_constructor))


@app.route("/company-orders", methods=["GET", "POST"])
def show_company_orders():
    if request.method == "GET":
        return render_template("companyOrders.html", selection=get_select_all_records(company_orders_query_constructor))
