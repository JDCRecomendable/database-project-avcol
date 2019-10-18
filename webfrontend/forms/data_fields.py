#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from wtforms import Form
from wtforms import StringField, TextAreaField
from wtforms.fields.html5 import DateField, DateTimeField, EmailField, TelField, IntegerField


class CustomerDetailsForm(Form):
    customer_id_string = IntegerField("ID*")
    first_name_string = StringField("First Name*")
    last_name_string = StringField("Last Name*")
    email_address_string = EmailField("Email Address*")
    phone_string = TelField("Phone Number*")


class CustomerLocationsDetailsForm(Form):
    customer_id_string = IntegerField("Customer ID*")
    city_name_string = StringField("City Name*")
    road_name_string = StringField("Road Name*")
    place_no_string = StringField("Place No*")


class ProductDetailsForm(Form):
    gtin14_string = StringField("GTIN-14*")
    name_string = StringField("Product Name*")
    desc_string = TextAreaField("Product Description")
    qty_in_stock_string = IntegerField("Qty in Stock*")


class CustomerOrderDetailsForm(Form):
    customer_order_id_string = IntegerField("Customer Order ID*")
    customer_id_string = IntegerField("Customer ID*")
    customer_order_datetime_ordered_string = DateTimeField("Date/Time Ordered*")
    customer_order_delivery_date_string = DateField("Delivery Date*")
    delivery_location_string = IntegerField("Delivery Location*")


class CustomerOrderItemDetailsForm(Form):
    customer_order_id_string = IntegerField("Customer Order ID*")
    product_gtin14_string = StringField("GTIN-14*")
    qty_bought_string = IntegerField("Qty Bought*")


class CompanyOrderDetailsForm(Form):
    company_order_id_string = IntegerField("Company Order ID*")
    company_order_product_gtin14_string = StringField("Product GTIN-14*")
    company_order_datetime_ordered_string = DateTimeField("Date/Time Ordered*")
    company_order_qty_bought_string = IntegerField("Qty Bought*")
    company_order_delivery_date_string = DateField("Delivery Date*")
