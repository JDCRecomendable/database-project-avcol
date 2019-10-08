#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from wtforms import Form
from wtforms import StringField
from wtforms.fields.html5 import DateField, DateTimeField, EmailField, TelField, IntegerField


class CustomerDetails(Form):
    customer_id_string = IntegerField("ID")
    first_name_string = StringField("First Name")
    last_name_string = StringField("Last Name")
    email_address_string = StringField("Email Address")
    phone_string = TelField("Phone Number")
    date_registered_string = DateField("Date Registered")
