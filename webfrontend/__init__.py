#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from flask import Flask, render_template


app = Flask(__name__)
customers_selection = []
products_selection = []
customer_orders_selection = []
company_orders_selection = []


@app.route("/customers")
def show_customers():
    return render_template("customers.html", selection=customers_selection)


@app.route("/products")
def show_products():
    return render_template("products.html", selection=products_selection)


@app.route("/customer-orders")
def show_customer_orders():
    return render_template("customerOrders.html", selection=customer_orders_selection)


@app.route("/company-orders")
def show_company_orders():
    return render_template("companyOrders.html", selection=company_orders_selection)
