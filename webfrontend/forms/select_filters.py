#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from flask_wtf import Form
from wtforms import StringField, RadioField, DateField, SelectField, IntegerField
from wtforms import validators


class CustomersDataFilterForm(Form):
    # First Name
    first_name_selection = RadioField("Filter by First Name",
                                      choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    first_name_string = StringField("First Name")
    first_name_at_beginning = SelectField("At beginning")
    first_name_at_end = SelectField("At end")

    # Last Name
    last_name_selection = RadioField("Filter by Last Name",
                                     choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    last_name_string = StringField("Last Name")
    last_name_at_beginning = SelectField("At beginning")
    last_name_at_end = SelectField("At end")

    # Email Address
    email_address_selection = RadioField("Filter by Email Address",
                                         choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    email_address_string = StringField("Email Address", validators.Email("Invalid email address!"))

    # Phone Number
    phone_number_selection = RadioField("Filter by First Name",
                                        choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    phone_number_string = StringField("Phone Number",
                                      validators.Length(min=9, max=12, message="Invalid phone number length!"))

    # Date Registered
    date_registered_selection = RadioField("Filter by Date Registered",
                                           choices=[("noFilter", "Do not filter"), ("filterExact", "Filter Exact"),
                                                    ("filterRanged", "Filter by Range")])
    date_registered_exact_string = DateField("Exact Date Registered")
    date_registered_lower_limit_string = DateField("Date Registered from")
    date_registered_upper_limit_string = DateField("Date Registered to")

    # Location
    location_selection = RadioField("Filter by Location of Customer",
                                    choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    location_place_no = StringField("Place No.")
    location_road_name = StringField("Road Name")
    location_city = StringField("City")

    # In Customer Order? (for e.g. when finding out customers who ordered in a specific date or location) (continue)
    # Bought Specific Product? (continue)


class ProductsDataFilterForm(Form):
    # GTIN-14
    gtin_14_selection = RadioField("Filter by GTIN-14",
                                   choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    gtin14_string = StringField("GTIN-14", validators.Length(min=14, max=14, message="Invalid length!"))

    # Name of Product
    name_selection = RadioField("Filter by Name",
                                choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    name_at_beginning = SelectField("At beginning")
    name_at_end = SelectField("At end")

    # Current Price
    current_price_selection = RadioField("Filter by Current Price",
                                         choices=[("noFilter", "Do not filter"), ("filterExact", "Filter Exact"),
                                                  ("filterRanged", "Filter by Range")])
    current_price_exact_string = IntegerField("Exact Current Price")
    current_price_lower_limit_string = IntegerField("Current Price minimum")
    current_price_upper_limit_string = IntegerField("Current Price maximum")

    # Qty in Stock
    qty_in_stock_selection = RadioField("Filter by Qty in Stock",
                                        choices=[("noFilter", "Do not filter"), ("filterExact", "Filter Exact"),
                                                 ("filterRanged", "Filter by Range")])
    qty_in_stock_exact_string = IntegerField("Exact Qty in Stock")
    qty_in_stock_lower_limit_string = IntegerField("Qty in Stock minimum")
    qty_in_stock_upper_limit_string = IntegerField("Qty in Stock maximum")

    # In Company Orders? (for e.g. when finding products ordered in a specific date) (continue)
    # In Customer Orders? (for e.g. when finding out customers who ordered products in a specific date or location)
    # (continue)
    # Ordered by Customer? (continue)


class OrdersDataFilterForm(Form):
    # Date/Time Ordered
    datetime_ordered_selection = RadioField("Filter by Date/Time Ordered",
                                            choices=[("noFilter", "Do not filter"),
                                                     ("filterExact", "Filter by Exact Date"),
                                                     ("filterRanged", "Filter by Range of Dates")])
    datetime_ordered_exact_string = DateField("Exact Date Ordered")
    datetime_ordered_lower_limit_string = DateField("Date Ordered from")
    datetime_ordered_upper_limit_string = DateField("Date Ordered to")

    # Delivery Date
    delivery_date_selection = RadioField("Filter by Delivery Date",
                                         choices=[("noFilter", "Do not filter"),
                                                  ("filterExact", "Filter by Exact Date"),
                                                  ("filterRanged", "Filter by Range of Dates")])
    delivery_date_exact_string = DateField("Exact Delivery Date")
    delivery_date_lower_limit_string = DateField("Delivery Date from")
    delivery_date_upper_limit_string = DateField("Delivery Date to")


class CustomerOrdersDataFilterForm(OrdersDataFilterForm):
    # # Customer ID
    # customer_id_selection = RadioField("Filter by Customer ID",
    #                                    choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    # customer_id_string = IntegerField("Customer ID")
    #
    # # Customer First Name
    # customer_first_name_selection = RadioField("Filter by Customer First Name",
    #                                            choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    # customer_first_name_string = StringField("Customer First Name")
    # customer_first_name_at_beginning = SelectField("At beginning")
    # customer_first_name_at_end = SelectField("At end")
    #
    # # Customer Last Name
    # customer_last_name_selection = RadioField("Filter by Customer Last Name",
    #                                           choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    # customer_last_name_string = StringField("Customer Last Name")
    # customer_last_name_at_beginning = SelectField("At beginning")
    # customer_last_name_at_end = SelectField("At end")
    #
    # # Customer Email Address
    # customer_email_address_selection = RadioField("Filter by Customer Email Address",
    #                                               choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    # customer_email_address_string = StringField("Customer Email Address", validators.Email("Invalid email address!"))

    # Customer? (continue)

    # Delivery Location
    location_selection = RadioField("Filter by Delivery Location",
                                    choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    location_place_no = StringField("Place No.")
    location_road_name = StringField("Road Name")
    location_city = StringField("City")


class CompanyOrderDataFilter(OrdersDataFilterForm):
    # Product GTIN-14
    product_gtin14_selection = RadioField("Filter by Product Ordered",
                                          choices=[("noFilter", "Do not filter"), ("filter", "Filter")])
    product_gtin14_text = StringField("Product GTIN-14", validators.Length(min=14, max=14, message="Invalid length!"))

    # Qty Bought
    qty_bought_selection = RadioField("Filter by Qty Bought",
                                      choices=[("noFilter", "Do not filter"), ("filterExact", "Filter Exact"),
                                               ("filterRanged", "Filter by Range")])
    qty_bought_exact_string = IntegerField("Exact Qty Bought")
    qty_bought_lower_limit_string = IntegerField("Qty Bought minimum")
    qty_bought_upper_limit_string = IntegerField("Qty Bought maximum")

    # Total Price Paid
    price_paid_selection = RadioField("Filter by Price Paid",
                                      choices=[("noFilter", "Do not filter"), ("filterExact", "Filter Exact"),
                                               ("filterRanged", "Filter by Range")])
    price_paid_exact_string = IntegerField("Exact Price Paid")
    price_paid_lower_limit_string = IntegerField("Price Paid minimum")
    price_paid_upper_limit_string = IntegerField("Price Paid maximum")
