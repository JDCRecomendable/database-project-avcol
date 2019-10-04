#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from wtforms import Form
from wtforms import StringField, RadioField, BooleanField
from wtforms.fields.html5 import DateField, IntegerField, EmailField, TelField


def gen_beg_end_bool_fields() -> tuple:
    return (BooleanField("String at beginning"),
            BooleanField("String at end"))


def gen_selection(label: str, ranged: bool = False) -> RadioField:
    if ranged:
        filter_label = "Filter by Range"
    else:
        filter_label = "Filter"
    return RadioField(label,
                      choices=[("noFilter", "Do not filter"), ("filter", filter_label)],
                      default="noFilter")


def gen_ranged_fields(field_name: str) -> tuple:
    return (IntegerField("{} minimum".format(field_name)),
            IntegerField("{} maximum".format(field_name)))


def gen_ranged_date_fields(field_name: str) -> tuple:
    return (DateField("{} from".format(field_name), format="%Y-%m-d"),
            DateField("{} to".format(field_name), format="%Y-%m-d"))


class CustomersDataBasicForm(Form):
    # First Name
    first_name_selection = gen_selection("Filter by First Name")
    first_name_string = StringField("First Name")
    first_name_at_beginning, first_name_at_end = gen_beg_end_bool_fields()

    # Last Name
    last_name_selection = gen_selection("Filter by Last Name")
    last_name_string = StringField("Last Name")
    last_name_at_beginning, last_name_at_end = gen_beg_end_bool_fields()

    # Email Address
    email_address_selection = gen_selection("Filter by Email Address")
    email_address_string = EmailField("Email Address")

    # Phone Number
    phone_selection = gen_selection("Filter by Phone Number")
    phone_string = TelField("Phone Number")

    # Date Registered
    date_registered_selection = gen_selection("Filter by Date Registered", ranged=True)
    date_registered_lower_limit_string, date_registered_upper_limit_string = gen_ranged_date_fields("Date Registered")


class LocationDataBasicForm(Form):
    # Location
    location_selection = gen_selection("Filter by Location")
    location_place_no = StringField("Place No.")
    location_road_name = StringField("Road Name")
    location_city = StringField("City")


class ProductsDataBasicForm(Form):
    # GTIN-14
    gtin_14_selection = gen_selection("Filter by Product GTIN-14")
    gtin14_string = StringField("GTIN-14")

    # Name of Product
    name_selection = gen_selection("Filter by Product Name")
    name_at_beginning, name_at_end = gen_beg_end_bool_fields()

    # Description of Product
    desc_selection = gen_selection("Filter by Product Description")
    desc_at_beginning, desc_at_end = gen_beg_end_bool_fields()

    # Current Price
    current_price_selection = gen_selection("Filter by Current Price", ranged=True)
    current_price_lower_limit_string, current_price_upper_limit_string = gen_ranged_fields("Current Price")

    # Qty in Stock
    qty_in_stock_selection = gen_selection("Filter by Qty in Stock", ranged=True)
    qty_in_stock_lower_limit_string, qty_in_stock_upper_limit_string = gen_ranged_fields("Qty in Stock")


class OrdersDataBasicForm(Form):
    # Date/Time Ordered
    datetime_ordered_selection = gen_selection("Filter by Date Ordered", ranged=True)
    datetime_ordered_lower_limit_string, datetime_ordered_upper_limit_string = gen_ranged_date_fields("Date Ordered")

    # Delivery Date
    delivery_date_selection = gen_selection("Filter by Delivery Date", ranged=True)
    delivery_date_lower_limit_string, delivery_date_upper_limit_string = gen_ranged_date_fields("Delivery Date")


class CustomerOrdersDataBasicForm(OrdersDataBasicForm):
    pass


class CompanyOrderDataBasicForm(OrdersDataBasicForm):
    # Qty Bought
    qty_bought_selection = gen_selection("Filter by Qty Bought", ranged=True)
    qty_bought_lower_limit_string, qty_bought_upper_limit_string = gen_ranged_fields("Qty Bought")

    # Total Price Paid
    price_paid_selection = gen_selection("Filter by Price Paid", ranged=True)
    price_paid_lower_limit_string, price_paid_upper_limit_string = gen_ranged_fields("Price Paid")


class CustomersDataFilterForm(CustomersDataBasicForm, LocationDataBasicForm):
    pass


class ProductsDataFilterForm(ProductsDataBasicForm, CustomersDataBasicForm,
                             LocationDataBasicForm, CustomerOrdersDataBasicForm,
                             CompanyOrderDataBasicForm):
    pass


class CustomerOrdersDataFilterForm(CustomerOrdersDataBasicForm, CustomersDataBasicForm,
                                   LocationDataBasicForm, ProductsDataBasicForm):
    pass


class CompanyOrdersDataFilterForm(CompanyOrderDataBasicForm, ProductsDataBasicForm):
    pass
