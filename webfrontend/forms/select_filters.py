#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.constants import *
from flask_wtf import Form
from wtforms import StringField, RadioField, DateField
from wtforms import validators


class CustomersDataFilterForm(Form):
    first_name_selection = RadioField("Sort by First Name", choices=[("noSort", "Do not sort"), ("sort", "Sort")])
    first_name_text = StringField("First Name")

    last_name_selection = RadioField("Sort by Last Name", choices=[("noSort", "Do not sort"), ("sort", "Sort")])
    last_name_text = StringField("Last Name")

    email_address_selection = RadioField("Sort by Email Address", choices=[("noSort", "Do not sort"), ("sort", "Sort")])
    email_address_text = StringField("Email Address", validators.Email("Invalid email address!"))

    phone_number_selection = RadioField("Sort by First Name", choices=[("noSort", "Do not sort"), ("sort", "Sort")])
    phone_number_text = StringField("Phone Number",
                                    validators.Length(min=9, max=12, message="Invalid phone number length!"))

    date_registered_selection = RadioField("Sort by Date Registered",
                                           choices=[("noSort", "Do not sort"), ("sort", "Sort")])
    date_registered_text = DateField("Date Registered")


class ProductsDataFilterForm(Form):
    pass
