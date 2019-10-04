#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from wtforms import Form
from wtforms import StringField, RadioField, BooleanField
from wtforms.fields.html5 import DateField, EmailField, TelField, IntegerField


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
    # ID
    customer_id_selection = gen_selection("Customer ID")
    customer_id_string = IntegerField("ID")

    # First Name
    first_name_selection = gen_selection("First Name")
    first_name_string = StringField("First Name")
    first_name_at_beginning, first_name_at_end = gen_beg_end_bool_fields()

    # Last Name
    last_name_selection = gen_selection("Last Name")
    last_name_string = StringField("Last Name")
    last_name_at_beginning, last_name_at_end = gen_beg_end_bool_fields()

    # Email Address
    email_address_selection = gen_selection("Email Address")
    email_address_string = EmailField("Email Address")

    # Phone Number
    phone_selection = gen_selection("Phone Number")
    phone_string = TelField("Phone Number")

    # Date Registered
    date_registered_selection = gen_selection("Date Registered", ranged=True)
    date_registered_lower_limit_string, date_registered_upper_limit_string = gen_ranged_date_fields("Date Registered")


class LocationDataBasicForm(Form):
    # Location
    location_selection = gen_selection("Location")
    location_place_no = StringField("Place No.")
    location_road_name = StringField("Road Name")
    location_city = StringField("City")


class ProductsDataBasicForm(Form):
    # GTIN-14
    gtin14_selection = gen_selection("GTIN-14")
    gtin14_string = StringField("GTIN-14")
    gtin14_at_beginning, gtin14_at_end = gen_beg_end_bool_fields()

    # Name of Product
    name_selection = gen_selection("Product Name")
    name_string = StringField("Product Name")
    name_at_beginning, name_at_end = gen_beg_end_bool_fields()

    # Description of Product
    desc_selection = gen_selection("Description")
    desc_string = StringField("Product Description")
    desc_at_beginning, desc_at_end = gen_beg_end_bool_fields()

    # Current Price
    current_price_selection = gen_selection("Price", ranged=True)
    current_price_lower_limit_string, current_price_upper_limit_string = gen_ranged_fields("Current Price")

    # Qty in Stock
    qty_in_stock_selection = gen_selection("Qty in Stock", ranged=True)
    qty_in_stock_lower_limit_string, qty_in_stock_upper_limit_string = gen_ranged_fields("Qty in Stock")


class CustomerOrdersDataBasicForm(Form):
    # ID
    customer_order_id_selection = gen_selection("Customer Order ID")
    customer_order_id_string = IntegerField("Customer Order ID")

    # Date/Time Ordered
    customer_datetime_ordered_selection = gen_selection("Date Ordered", ranged=True)
    customer_datetime_ordered_lower_limit_string, customer_datetime_ordered_upper_limit_string =\
        gen_ranged_date_fields("Date Ordered")

    # Delivery Date
    customer_delivery_date_selection = gen_selection("Delivery Date", ranged=True)
    customer_delivery_date_lower_limit_string, customer_delivery_date_upper_limit_string =\
        gen_ranged_date_fields("Delivery Date")


class CompanyOrderDataBasicForm(Form):
    # ID
    company_order_id_selection = gen_selection("Company Order ID")
    company_order_id_string = IntegerField("Company Order ID")

    # Date/Time Ordered
    company_datetime_ordered_selection = gen_selection("Date Ordered by Company", ranged=True)
    company_datetime_ordered_lower_limit_string, company_datetime_ordered_upper_limit_string =\
        gen_ranged_date_fields("Date Ordered")

    # Delivery Date
    company_delivery_date_selection = gen_selection("Delivery Date to Company", ranged=True)
    company_delivery_date_lower_limit_string, company_delivery_date_upper_limit_string =\
        gen_ranged_date_fields("Delivery Date")

    # Qty Bought
    qty_bought_selection = gen_selection("Qty Bought by Company", ranged=True)
    qty_bought_lower_limit_string, qty_bought_upper_limit_string = gen_ranged_fields("Qty Bought")

    # Total Price Paid
    total_price_paid_selection = gen_selection("Price Paid by Company", ranged=True)
    total_price_paid_lower_limit_string, total_price_paid_upper_limit_string = gen_ranged_fields("Total Price Paid")


class CustomersDataFilterForm(CustomersDataBasicForm, LocationDataBasicForm,
                              CustomerOrdersDataBasicForm, ProductsDataBasicForm):
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
