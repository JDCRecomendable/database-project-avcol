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
    first_name_selection = RadioField(
        WebInterface.DataFilterForm.selection_label(
            DBFields.Customers.first_name
        ),
        choices=[
            (WebInterface.DataFilterForm.Customers.first_name_no_filter_id,
             WebInterface.DataFilterForm.Customers.first_name_no_filter_label),
            (WebInterface.DataFilterForm.Customers.first_name_filter_id,
             WebInterface.DataFilterForm.Customers.first_name_filter_label)
        ]
    )
    first_name_text = StringField(WebInterface.DataFilterForm.entry_label(
        DBFields.Customers.first_name
    ))
    last_name_selection = RadioField(
        WebInterface.DataFilterForm.selection_label(
            DBFields.Customers.last_name
        ),
        choices=[
            (WebInterface.DataFilterForm.Customers.last_name_no_filter_id,
             WebInterface.DataFilterForm.Customers.last_name_no_filter_label),
            (WebInterface.DataFilterForm.Customers.last_name_filter_id,
             WebInterface.DataFilterForm.Customers.last_name_filter_label)
        ]
    )
    last_name_text = StringField(WebInterface.DataFilterForm.entry_label(
        DBFields.Customers.last_name
    ))
    email_address_selection = RadioField(
        WebInterface.DataFilterForm.selection_label(
            DBFields.Customers.email_address
        ),
        choices=[
            (WebInterface.DataFilterForm.Customers.email_address_no_filter_id,
             WebInterface.DataFilterForm.Customers.email_address_no_filter_label),
            (WebInterface.DataFilterForm.Customers.email_address_filter_id,
             WebInterface.DataFilterForm.Customers.email_address_filter_label)
        ]
    )
    email_address_text = StringField(
        WebInterface.DataFilterForm.entry_label(DBFields.Customers.email_address),
        validators.Email(WebInterface.DataFilterForm.Customers.email_address_invalid)
    )
    phone_number_selection = RadioField(
        WebInterface.DataFilterForm.selection_label(
            DBFields.Customers.phone
        ),
        choices=[
            (WebInterface.DataFilterForm.Customers.phone_no_filter_id,
             WebInterface.DataFilterForm.Customers.phone_no_filter_label),
            (WebInterface.DataFilterForm.Customers.phone_filter_id,
             WebInterface.DataFilterForm.Customers.phone_filter_label)
        ]
    )
    phone_number_text = StringField(
        WebInterface.DataFilterForm.entry_label(DBFields.Customers.phone),
        validators.Length(min=9, max=12,
                          message=WebInterface.DataFilterForm.Customers.phone_length_invalid)
    )
    date_registered_selection = RadioField(
        WebInterface.DataFilterForm.selection_label(
            DBFields.Customers.date_registered
        ),
        choices=[
            (WebInterface.DataFilterForm.Customers.date_registered_no_filter_id,
             WebInterface.DataFilterForm.Customers.date_registered_no_filter_label),
            (WebInterface.DataFilterForm.Customers.date_registered_filter_id,
             WebInterface.DataFilterForm.Customers.date_registered_filter_label)
        ]
    )
    date_registered_text = DateField(
        WebInterface.DataFilterForm.entry_label(
            DBFields.Customers.date_registered
        )
    )


class ProductsDataFilterForm(Form):
    pass
