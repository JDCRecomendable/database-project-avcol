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


@app.route("/customers", methods=["GET", "POST"])
def show_customers():
    customers_query_constructor.reset()
    if request.method == "GET":
        query = customers_query_constructor.render_select_query()
        customers_selection = database_connector.execute_query(
            query,
            select=True
        )
        return render_template("customers.html", selection=customers_selection)


@app.route("/products", methods=["GET", "POST"])
def show_products():
    if request.method == "GET":
        query = products_query_constructor.render_select_query()
        products_selection = database_connector.execute_query(
            query,
            select=True
        )
        return render_template("products.html", selection=products_selection)


@app.route("/customer-orders", methods=["GET", "POST"])
def show_customer_orders():
    if request.method == "GET":
        query = customer_orders_query_constructor.render_select_query()
        customer_orders_selection = database_connector.execute_query(
            query,
            select=True
        )
        return render_template("customerOrders.html", selection=customer_orders_selection)


@app.route("/company-orders", methods=["GET", "POST"])
def show_company_orders():
    if request.method == "GET":
        query = company_orders_query_constructor.render_select_query()
        company_orders_selection = database_connector.execute_query(
            query,
            select=True
        )
        return render_template("companyOrders.html", selection=company_orders_selection)
