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


class CustomersDataForm(Form):
    # First Name
    first_name_selection = RadioField("Filter by First Name",
                                      choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                      default="noFilter")
    first_name_string = StringField("First Name")
    first_name_at_beginning = BooleanField("String at beginning")
    first_name_at_end = BooleanField("String at end")

    # Last Name
    last_name_selection = RadioField("Filter by Last Name",
                                     choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                     default="noFilter")
    last_name_string = StringField("Last Name")
    last_name_at_beginning = BooleanField("String at beginning")
    last_name_at_end = BooleanField("String at end")

    # Email Address
    email_address_selection = RadioField("Filter by Email Address",
                                         choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                         default="noFilter")
    email_address_string = EmailField("Email Address")

    # Phone Number
    phone_selection = RadioField("Filter by Phone Number",
                                 choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                 default="noFilter")
    phone_string = TelField("Phone Number")

    # Date Registered
    date_registered_selection = RadioField("Filter by Date Registered",
                                           choices=[("noFilter", "Do not filter"), ("filter", "Filter by Range")],
                                           default="noFilter")
    date_registered_lower_limit_string = DateField("Date Registered from", format="%Y-%m-d")
    date_registered_upper_limit_string = DateField("Date Registered to", format="%Y-%m-d")

    # Location
    location_selection = RadioField("Filter by Location of Customer",
                                    choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                    default="noFilter")
    location_place_no = StringField("Place No.")
    location_road_name = StringField("Road Name")
    location_city = StringField("City")

    # In Customer Order? (for e.g. when finding out customers who ordered in a specific date or location) (continue)
    # Bought Specific Product? (continue)


class ProductsDataForm(Form):
    # GTIN-14
    gtin_14_selection = RadioField("Filter by GTIN-14",
                                   choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                   default="noFilter")
    gtin14_string = StringField("GTIN-14")

    # Name of Product
    name_selection = RadioField("Filter by Name",
                                choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                default="noFilter")
    name_at_beginning = BooleanField("String at beginning")
    name_at_end = BooleanField("String at end")

    # Current Price
    current_price_selection = RadioField("Filter by Current Price",
                                         choices=[("noFilter", "Do not filter"), ("filter", "Filter by Range")],
                                         default="noFilter")
    current_price_lower_limit_string = IntegerField("Current Price minimum")
    current_price_upper_limit_string = IntegerField("Current Price maximum")

    # Qty in Stock
    qty_in_stock_selection = RadioField("Filter by Qty in Stock",
                                        choices=[("noFilter", "Do not filter"), ("filter", "Filter by Range")],
                                        default="noFilter")
    qty_in_stock_lower_limit_string = IntegerField("Qty in Stock minimum")
    qty_in_stock_upper_limit_string = IntegerField("Qty in Stock maximum")

    # In Company Orders? (for e.g. when finding products ordered in a specific date) (continue)
    # In Customer Orders? (for e.g. when finding out customers who ordered products in a specific date or location)
    # (continue)
    # Ordered by Customer? (continue)


class OrdersDataForm(Form):
    # Date/Time Ordered
    datetime_ordered_selection = RadioField("Filter by Date/Time Ordered",
                                            choices=[("noFilter", "Do not filter"),
                                                     ("filter", "Filter by Range of Dates")],
                                            default="noFilter")
    datetime_ordered_lower_limit_string = DateField("Date Ordered from", format="%Y-%m-d")
    datetime_ordered_upper_limit_string = DateField("Date Ordered to", format="%Y-%m-d")

    # Delivery Date
    delivery_date_selection = RadioField("Filter by Delivery Date",
                                         choices=[("noFilter", "Do not filter"),
                                                  ("filter", "Filter by Range of Dates")],
                                         default="noFilter")
    delivery_date_lower_limit_string = DateField("Delivery Date from", format="%Y-%m-d")
    delivery_date_upper_limit_string = DateField("Delivery Date to", format="%Y-%m-d")


class CustomerOrdersDataForm(OrdersDataForm):
    # # Customer ID
    # customer_id_selection = RadioField("Filter by Customer ID",
    #                                    choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
    #                                    default="noFilter")
    # customer_id_string = IntegerField("Customer ID")
    #
    # # Customer First Name
    # customer_first_name_selection = RadioField("Filter by Customer First Name",
    #                                            choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
    #                                            default="noFilter")
    # customer_first_name_string = StringField("Customer First Name")
    # customer_first_name_at_beginning = BooleanField("String at beginning")
    # customer_first_name_at_end = BooleanField("String at end")
    #
    # # Customer Last Name
    # customer_last_name_selection = RadioField("Filter by Customer Last Name",
    #                                           choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
    #                                           default="noFilter")
    # customer_last_name_string = StringField("Customer Last Name")
    # customer_last_name_at_beginning = BooleanField("String at beginning")
    # customer_last_name_at_end = BooleanField("String at end")
    #
    # # Customer Email Address
    # customer_email_address_selection = RadioField("Filter by Customer Email Address",
    #                                               choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
    #                                               default="noFilter")
    # customer_email_address_string = EmailField("Customer Email Address", validators.Email("Invalid email address!"))

    # Customer? (continue)

    # Delivery Location
    location_selection = RadioField("Filter by Delivery Location",
                                    choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                    default="noFilter")
    location_place_no = StringField("Place No.")
    location_road_name = StringField("Road Name")
    location_city = StringField("City")


class CompanyOrderDataForm(OrdersDataForm):
    # Product GTIN-14
    product_gtin14_selection = RadioField("Filter by Product Ordered",
                                          choices=[("noFilter", "Do not filter"), ("filter", "Filter")],
                                          default="noFilter")
    product_gtin14_text = StringField("Product GTIN-14")

    # Qty Bought
    qty_bought_selection = RadioField("Filter by Qty Bought",
                                      choices=[("noFilter", "Do not filter"), ("filter", "Filter by Range")],
                                      default="noFilter")
    qty_bought_lower_limit_string = IntegerField("Qty Bought minimum")
    qty_bought_upper_limit_string = IntegerField("Qty Bought maximum")

    # Total Price Paid
    price_paid_selection = RadioField("Filter by Price Paid",
                                      choices=[("noFilter", "Do not filter"), ("filter", "Filter by Range")],
                                      default="noFilter")
    price_paid_lower_limit_string = IntegerField("Price Paid minimum")
    price_paid_upper_limit_string = IntegerField("Price Paid maximum")
