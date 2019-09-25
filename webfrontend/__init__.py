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
        return render_template("customers.html", selection=customers_selection,
                               fields=[
                                   WebInterface.DBAttibuteLabels.Customers.id,
                                   WebInterface.DBAttibuteLabels.Customers.first_name,
                                   WebInterface.DBAttibuteLabels.Customers.last_name,
                                   WebInterface.DBAttibuteLabels.Customers.email_address,
                                   WebInterface.DBAttibuteLabels.Customers.phone,
                                   WebInterface.DBAttibuteLabels.Customers.date_registered
                               ])


@app.route("/products", methods=["GET", "POST"])
def show_products():
    if request.method == "GET":
        query = products_query_constructor.render_select_query()
        products_selection = database_connector.execute_query(
            query,
            select=True
        )
        return render_template("products.html", selection=products_selection,
                               fields=[
                                   WebInterface.DBAttibuteLabels.Products.gtin14,
                                   WebInterface.DBAttibuteLabels.Products.name,
                                   WebInterface.DBAttibuteLabels.Products.description,
                                   WebInterface.DBAttibuteLabels.Products.current_price,
                                   WebInterface.DBAttibuteLabels.Products.qty_in_stock
                               ])


@app.route("/customer-orders", methods=["GET", "POST"])
def show_customer_orders():
    if request.method == "GET":
        query = customer_orders_query_constructor.render_select_query()
        customer_orders_selection = database_connector.execute_query(
            query,
            select=True
        )
        return render_template("customerOrders.html", selection=customer_orders_selection,
                               fields=[
                                   WebInterface.DBAttibuteLabels.CustomerOrders.id,
                                   WebInterface.DBAttibuteLabels.CustomerOrders.customer_id,
                                   WebInterface.DBAttibuteLabels.CustomerOrders.datetime_ordered,
                                   WebInterface.DBAttibuteLabels.CustomerOrders.delivery_date,
                                   WebInterface.DBAttibuteLabels.CustomerOrders.delivery_location
                               ])


@app.route("/company-orders", methods=["GET", "POST"])
def show_company_orders():
    if request.method == "GET":
        query = company_orders_query_constructor.render_select_query()
        company_orders_selection = database_connector.execute_query(
            query,
            select=True
        )
        return render_template("companyOrders.html", selection=company_orders_selection,
                               fields=[
                                   WebInterface.DBAttibuteLabels.CompanyOrders.id,
                                   WebInterface.DBAttibuteLabels.CompanyOrders.product_gtin14,
                                   WebInterface.DBAttibuteLabels.CompanyOrders.datetime_ordered,
                                   WebInterface.DBAttibuteLabels.CompanyOrders.qty_bought,
                                   WebInterface.DBAttibuteLabels.CompanyOrders.total_price_paid,
                                   WebInterface.DBAttibuteLabels.CompanyOrders.delivery_date
                               ])
