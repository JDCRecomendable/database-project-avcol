#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from base.utils import *
from database.query_constructors import SelectQueryConstructor, UpdateQueryConstructor, DeleteQueryConstructor


class TableAdapter:
    def __init__(self, table_name, insert_query):
        self.select_query_constructor = SelectQueryConstructor(
            table_name,
            schema_name=DatabaseSchemaAndTableName.schema
        )
        self.update_query_constructor = UpdateQueryConstructor(
            table_name,
            schema_name=DatabaseSchemaAndTableName.schema
        )
        self.delete_query_constructor = DeleteQueryConstructor(
            table_name,
            schema_name=DatabaseSchemaAndTableName.schema
        )
        self.insert_query = insert_query

    def insert_data(self, data_list: tuple) -> str:
        """Return a SQL query for inserting data into the table.
        :type data_list: tuple
        """
        return self.insert_query.format(*data_list)

    def add_select_field(self, field: str):
        """Add a field for when selecting data from the table.
        :type field: str
        """
        self.select_query_constructor.add_field(field)

    def add_select_fields(self, field_list: list):
        """Add fields for when selecting data from the table.
        :type field_list: list
        """
        self.select_query_constructor.add_fields(field_list)

    def add_select_condition_nested_query(self, variable: str, nested_query: str):
        """Add a nested query as a condition for SQL select.
        :type variable: str
        :type nested_query: str
        """
        self.select_query_constructor.add_nested_query(variable, nested_query)

    def add_update_field(self, field: str):
        """Add a field for updating in the table.
        The number of fields must match the number of values for updating.
        :type field: str
        """
        self.update_query_constructor.add_field(field)

    def add_update_fields(self, field_list: list):
        """Add a series of fields for updating in the table.
        The number of fields must match the number of values for updating.
        :type field_list: list
        """
        self.update_query_constructor.add_fields(field_list)

    def add_update_value(self, value: str):
        """Add a value to use for updating data in a table.
        The number of values must match the number of fields for updating.
        :type value: str
        """
        self.update_query_constructor.add_value(value)

    def add_update_values(self, value_list: list):
        """Add a series of values to use for updating data in a table.
        The number of values must match the number of fields for updating.
        :type value_list: list
        """

        self.update_query_constructor.add_values(value_list)

    def add_update_or_delete_condition_nested_query(self, variable: str, nested_query: str):
        """Add a nested query as a condition for SQL update or delete.
        :type variable: str
        :type nested_query: str
        """
        self.update_query_constructor.add_nested_query(variable, nested_query)
        self.delete_query_constructor.add_nested_query(variable, nested_query)

    def reset_select_query_constructor(self):
        self.select_query_constructor.reset()

    def reset_update_query_constructor(self):
        self.update_query_constructor.reset()

    def reset_delete_query_constructor(self):
        self.delete_query_constructor.reset()

    def render_select_query(self) -> str:
        """Return a SQL query for selecting data from the table."""
        return self.select_query_constructor.render()

    def render_update_query(self) -> str:
        """Return a SQL query for updating data on the table."""
        return self.update_query_constructor.render()

    def render_delete_query(self) -> str:
        """Return a SQL query for deleting data from the table."""
        return self.delete_query_constructor.render()


class CustomersTableAdapter(TableAdapter):
    def __init__(self):
        super(CustomersTableAdapter, self).__init__(
            DatabaseSchemaAndTableName.customers,
            get_text_file_lines_as_single_line(DatabaseQueryFilePath.add_customer)
        )

    # SQL SELECT
    def add_select_condition_id(self, id_value: str):
        """Add the condition for exact customer `id` for when selecting customer(s).
        :type id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.id,
            id_value
        )

    def add_select_condition_last_name_exact(self, last_name_value: str):
        """Add the condition for exact customer `last_name` for when selecting customer(s).
        :type last_name_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.last_name,
            last_name_value
        )

    def add_select_condition_first_name_exact(self, first_name_value: str):
        """Add the condition for exact customer `first_name` for when selecting customer(s).
        :type first_name_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.first_name,
            first_name_value
        )

    def add_select_condition_last_name_like(self,
                                            last_name_value: str,
                                            at_beginning: bool = False,
                                            at_end: bool = False):
        """Add the condition for customer `last_name` for when selecting customer(s), where the input value
        is a subset of the customer's last name.
        :type last_name_value: str
        :type at_beginning: bool
        :type at_end: bool
        """
        self.select_query_constructor.add_condition_like(
            DatabaseAttributeName.Customers.last_name,
            last_name_value,
            at_beginning=at_beginning,
            at_end=at_end
        )

    def add_select_condition_first_name_like(self,
                                             first_name_value: str,
                                             at_beginning: bool = False,
                                             at_end: bool = False):
        """Add the condition for customer `first_name` for when selecting customer(s), where the input value
        is a subset of the customer's first name.
        :type first_name_value: str
        :type at_beginning: bool
        :type at_end: bool
        """
        self.select_query_constructor.add_condition_like(
            DatabaseAttributeName.Customers.first_name,
            first_name_value,
            at_beginning=at_beginning,
            at_end=at_end
        )

    def add_select_condition_email_address_exact(self, email_address_value: str):
        """Add the condition for the exact customer `email_address` for when selecting customer(s).
        :type email_address_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.email_address,
            email_address_value
        )

    def add_select_condition_email_address_like(self,
                                                email_address_value: str,
                                                at_beginning: bool = False,
                                                at_end: bool = False):
        """Add teh condition for customer `email_address` for when selecting customer(s), where the input email address
        is a subset of the actual customer email address.
        :type email_address_value: str
        :type at_beginning: bool
        :type at_end: bool
        """
        self.select_query_constructor.add_condition_like(
            DatabaseAttributeName.Customers.email_address,
            email_address_value,
            at_beginning=at_beginning,
            at_end=at_end
        )

    def add_select_condition_phone_exact(self, phone_value: str):
        """Add the condition for the exact customer `phone` for when selecting customer(s).
        :type phone_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.phone,
            phone_value
        )

    def add_select_condition_phone_like(self,
                                        phone_value: str,
                                        at_beginning: bool = False,
                                        at_end: bool = False):
        """Add the condition for the customer `phone` for when selecting customer(s), where the input phone is a subset
        of the actual phone of the customer.
        :type phone_value: str
        :type at_beginning: bool
        :type at_end: bool
        """
        self.select_query_constructor.add_condition_like(
            DatabaseAttributeName.Customers.phone,
            phone_value,
            at_beginning=at_beginning,
            at_end=at_end
        )

    def add_select_condition_date_registered_exact(self, date_registered_value: str):
        """Add the condition for the exact customer `date_registered` for when selecting customer(s).
        :type date_registered_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.date_registered,
            date_registered_value
        )

    def add_select_condition_date_registered_ranged(self,
                                                    date_registered_lower_limit: str = "",
                                                    date_registered_upper_limit: str = ""):
        """Add the condition for the customer `date_registered` for when selecting customer(s), where the date
        registered of the customer is between the input lower limit and the input upper limit.
        :type date_registered_lower_limit: str
        :type date_registered_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.Customers.date_registered,
            lower_limit=date_registered_lower_limit,
            upper_limit=date_registered_upper_limit
        )

    # SQL UPDATE

    # SQL UPDATE OR DELETE
    def add_update_or_delete_condition_id(self, id_value: str):
        """Add the condition for exact customer `id` for when updating or deleting a customer.
        :type id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.id,
            id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.id,
            id_value
        )

    def add_update_or_delete_condition_email_address(self, email_address_value: str):
        """Add the condition for exact customer `email_address` for when updating or deleting a customer.
        :type email_address_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.email_address,
            email_address_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.email_address,
            email_address_value
        )


class ProductsTableAdapter(TableAdapter):
    def __init__(self):
        super(ProductsTableAdapter, self).__init__(
            DatabaseSchemaAndTableName.products,
            get_text_file_lines_as_single_line(DatabaseQueryFilePath.add_product)
        )

    # SQL SELECT
    def add_select_condition_gtin14_exact(self, gtin14_value: str):
        """Add the condition for exact product `gtin14` for when selecting product(s).
        :type gtin14_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Products.gtin14,
            gtin14_value
        )

    def add_select_condition_gtin14_like(self,
                                         gtin14_value: str,
                                         at_beginning: bool = False,
                                         at_end: bool = False):
        """Add the condition for product `gtin14` for when selecting product(s), where the input gtin14 is a subset
        of the actual gtin14 of the product.
        :type gtin14_value: str,
        :type at_beginning: bool,
        :type at_end: bool
        """
        self.select_query_constructor.add_condition_like(
            DatabaseAttributeName.Products.gtin14,
            gtin14_value,
            at_beginning=at_beginning,
            at_end=at_end
        )

    def add_select_condition_name_exact(self, name_value: str):
        """Add the condition for exact product `name` for when selecting products.
        :type name_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Products.name,
            name_value
        )

    def add_select_condition_name_like(self,
                                       name_value: str,
                                       at_beginning: bool = False,
                                       at_end: bool = False):
        """Add the condition for product `name` for when selecting product(s), where the input value
        is a subset of the full name of the product.
        :type name_value: str
        :type at_beginning: bool
        :type at_end: bool
        """
        self.select_query_constructor.add_condition_like(
            DatabaseAttributeName.Products.name,
            name_value,
            at_beginning=at_beginning,
            at_end=at_end
        )

    def add_select_condition_price_exact(self, price_value: str):
        """Add the condition for the exact price of a product when selecting product(s).
        :type price_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Products.current_price,
            price_value
        )

    def add_select_condition_price_ranged(self,
                                          price_value_lower_limit: str = "",
                                          price_value_upper_limit: str = ""):
        """Add the condition for the price of a product when selecting product(s), where the input price
        of the product is between the input lower limit and input upper limit.
        :type price_value_lower_limit: str
        :type price_value_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.Products.current_price,
            lower_limit=price_value_lower_limit,
            upper_limit=price_value_upper_limit
        )

    def add_select_condition_qty_in_stock_exact(self, qty_in_stock_value: str):
        """Add the condition for the exact product `qty_in_stock` for when selecting product(s).
        :type qty_in_stock_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Products.qty_in_stock,
            qty_in_stock_value
        )

    def add_select_condition_qty_in_stock_ranged(self,
                                                 qty_in_stock_lower_limit: str = "",
                                                 qty_in_stock_upper_limit: str = ""):
        """Add the condition for the product `qty_in_stock` for when selecting product(s), where the qty in stock
        of the product is between the input lower limit and the input upper limit.
        :type qty_in_stock_lower_limit: str
        :type qty_in_stock_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.Products.qty_in_stock,
            lower_limit=qty_in_stock_lower_limit,
            upper_limit=qty_in_stock_upper_limit
        )

    # SQL UPDATE

    # SQL UPDATE OR DELETE
    def add_update_or_delete_condition_gtin14(self, gtin14_value: str):
        """Add the condition for the exact product `gtin14` for when updating or deleting a product.
        :type gtin14_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Products.gtin14,
            gtin14_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Products.gtin14,
            gtin14_value
        )


class LocationsTableAdapter(TableAdapter):
    def __init__(self):
        super(LocationsTableAdapter, self).__init__(
            DatabaseSchemaAndTableName.locations,
            get_text_file_lines_as_single_line(DatabaseQueryFilePath.add_location)
        )

    def add_select_condition_id(self, id_value: str):
        """Add a condition for exact location `id` for when selecting location(s).
        :type id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Locations.id,
            id_value
        )

    def add_update_or_delete_condition_id(self, id_value: str):
        """Add the condition for exact location `id` for when updating or deleting a location.
        :type id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Locations.id,
            id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Locations.id,
            id_value
        )


class CustomerLocationsTableAdapter(TableAdapter):
    def __init__(self):
        super(CustomerLocationsTableAdapter, self).__init__(
            DatabaseSchemaAndTableName.customer_locations,
            get_text_file_lines_as_single_line(DatabaseQueryFilePath.add_customer_location)
        )

    # SQL SELECT
    def add_select_condition_customer_id(self, customer_id_value: str):
        """Add the condition for exact customer `id` for when selecting customer location(s).
        :type customer_id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerLocations.customer_id,
            customer_id_value
        )

    def add_select_condition_location_id(self, location_id_value: str):
        """Add the condition for exact location `id` for when selecting customer location(s).
        :type location_id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerLocations.location_id,
            location_id_value
        )

    def add_select_condition_customer_email_address(self, customer_email_address_value: str):
        """Add the condition for exact customer `email_address` for when selecting customer location(s).
        :type customer_email_address_value: str
        """
        customer_select_query_constructor = SelectQueryConstructor(
            DatabaseSchemaAndTableName.customers,
            schema_name=DatabaseSchemaAndTableName.schema
        )
        customer_select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.email_address,
            customer_email_address_value
        )
        customer_select_query_constructor.add_field(
            DatabaseAttributeName.Customers.id
        )
        self.select_query_constructor.add_nested_query(
            DatabaseAttributeName.CustomerLocations.customer_id,
            customer_select_query_constructor.render()
        )

    def add_select_condition_customer_name_like(self, last_name_value: str, first_name_value: str):
        """Add the condition for customer's last and first names for when selecting customer location(s), where the
        input last name and input first name are subsets of the customer's last name and first name respectively.
        :type last_name_value: str
        :type first_name_value: str
        """
        customer_select_query_constructor = SelectQueryConstructor(
            DatabaseSchemaAndTableName.customers,
            schema_name=DatabaseSchemaAndTableName.schema
        )
        customer_select_query_constructor.add_condition_like(
            DatabaseAttributeName.Customers.last_name,
            last_name_value
        )
        customer_select_query_constructor.add_condition_like(
            DatabaseAttributeName.Customers.first_name,
            first_name_value
        )
        customer_select_query_constructor.add_field(
            DatabaseAttributeName.Customers.id
        )
        self.select_query_constructor.add_nested_query(
            DatabaseAttributeName.CustomerLocations.customer_id,
            customer_select_query_constructor.render()
        )

    # SQL UPDATE

    # SQL UPDATE OR DELETE
    def add_update_or_delete_condition_customer_id(self, customer_id_value: str):
        """Add a condition for the exact customer location `customer_id` for when updating or deleting customer location(s).
        :type customer_id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerLocations.customer_id,
            customer_id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerLocations.customer_id,
            customer_id_value
        )

    def add_update_or_delete_condition_location_id(self, location_id_value: str):
        """Add a condition for the exact customer location `location_id` for when updating or deleting customer location(s).
        :type location_id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerLocations.location_id,
            location_id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerLocations.location_id,
            location_id_value
        )

    def add_update_or_delete_condition_customer_email_address(self, customer_email_address_value: str):
        """Add the condition for exact customer `email_address` for when updating or deleting a customer location.
        :type customer_email_address_value: str
        """
        customer_select_query_constructor = SelectQueryConstructor(
            DatabaseSchemaAndTableName.customers,
            schema_name=DatabaseSchemaAndTableName.schema
        )
        customer_select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.Customers.email_address,
            customer_email_address_value
        )
        customer_select_query_constructor.add_field(
            DatabaseAttributeName.Customers.id
        )
        self.update_query_constructor.add_nested_query(
            DatabaseAttributeName.CustomerLocations.customer_id,
            customer_select_query_constructor.render()
        )
        self.delete_query_constructor.add_nested_query(
            DatabaseAttributeName.CustomerLocations.customer_id,
            customer_select_query_constructor.render()
        )


class CompanyOrdersTableAdapter(TableAdapter):
    def __init__(self):
        super(CompanyOrdersTableAdapter, self).__init__(
            DatabaseSchemaAndTableName.company_orders,
            get_text_file_lines_as_single_line(DatabaseQueryFilePath.add_company_order)
        )

    # SQL SELECT
    def add_select_condition_id(self, id_value: str):
        """Add the condition for exact company order `id` for when selecting company order(s).
        :type id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.id,
            id_value
        )

    def add_select_condition_product_gtin14(self, product_gtin14_value: str):
        """Add the condition for exact company order `product_gtin14` for when selecting company order(s).
        :type product_gtin14_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.product_gtin14,
            product_gtin14_value
        )

    def add_select_condition_datetime_ordered_exact(self, datetime_ordered_value: str):
        """Add the condition for exact company order `datetime_ordered` for when selecting company order(s).
        :type datetime_ordered_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.datetime_ordered,
            datetime_ordered_value
        )

    def add_select_condition_datetime_ordered_range(self,
                                                    datetime_ordered_lower_limit: str = "",
                                                    datetime_ordered_upper_limit: str = ""):
        """Add the condition for company order `datetime_ordered` for when selecting company order(s), where the
        datetime ordered of the company order is between the input lower limit and the input upper limit.
        :type datetime_ordered_lower_limit: str
        :type datetime_ordered_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.datetime_ordered,
            lower_limit=datetime_ordered_lower_limit,
            upper_limit=datetime_ordered_upper_limit
        )

    def add_select_condition_qty_bought_exact(self, qty_bought_value: str):
        """Add the condition for exact company order `qty_bought` for when selecting company order(s).
        :type qty_bought_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.qty_bought,
            qty_bought_value
        )

    def add_select_condition_qty_bought_ranged(self,
                                               qty_bought_lower_limit: str = "",
                                               qty_bought_upper_limit: str = ""):
        """Add the condition for company order `qty_bought` for when selecting company order(s), where the qty bought
        for the company order is between the input lower limit and the input upper limit.
        :type qty_bought_lower_limit: str
        :type qty_bought_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.qty_bought,
            lower_limit=qty_bought_lower_limit,
            upper_limit=qty_bought_upper_limit
        )

    def add_select_condition_total_price_paid_exact(self, total_price_paid_value: str):
        """Add the condition for exact company order `total_price_paid` for when selecting company order(s).
        :type total_price_paid_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.total_price_paid,
            total_price_paid_value
        )

    def add_select_condition_total_price_paid_ranged(self,
                                                     total_price_paid_lower_limit: str = "",
                                                     total_price_paid_upper_limit: str = ""):
        """Add the condition for company order `total_price_paid` for when selecting company order(s), where the total
        price paid for the company order is between the input lower limit and input upper limit.
        :type total_price_paid_lower_limit: str
        :type total_price_paid_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.total_price_paid,
            lower_limit=total_price_paid_lower_limit,
            upper_limit=total_price_paid_upper_limit
        )

    def add_select_condition_delivery_date_exact(self, delivery_date_value: str):
        """Add the condition for exact company order `delivery_date` for when selecting company order(s).
        :type delivery_date_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.delivery_date,
            delivery_date_value
        )

    def add_select_condition_delivery_date_ranged(self,
                                                  delivery_date_lower_limit: str = "",
                                                  delivery_date_upper_limit: str = ""):
        """Add the condition for company order `delivery_date` for when selecting company order(s), where the delivery
        date of the company order is between the input lower limit and input upper limit.
        :type delivery_date_lower_limit: str
        :type delivery_date_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.delivery_date,
            lower_limit=delivery_date_lower_limit,
            upper_limit=delivery_date_upper_limit
        )

    # SQL UPDATE

    # SQL UPDATE OR DELETE
    def add_update_or_delete_condition_id(self, id_value: str):
        """Add the delete condition for exact company order `id` for when updating or deleting a company order.
        :type id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.id,
            id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.id,
            id_value
        )

    def add_update_or_delete_condition_datetime_ordered_exact(self, datetime_ordered_value: str):
        """Add the condition for exact company order `datetime_ordered` for when updating or deleting a company order.
        :type datetime_ordered_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.datetime_ordered,
            datetime_ordered_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.datetime_ordered,
            datetime_ordered_value
        )

    def add_update_or_delete_condition_datetime_ordered_range(self,
                                                              datetime_ordered_lower_limit: str = "",
                                                              datetime_ordered_upper_limit: str = ""):
        """Add the condition for company order `datetime_ordered` for when updating or deleting company order(s), where the
        datetime ordered of the company order is between the input lower limit and the input upper limit.
        :type datetime_ordered_lower_limit: str
        :type datetime_ordered_upper_limit: str
        """
        self.update_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.datetime_ordered,
            lower_limit=datetime_ordered_lower_limit,
            upper_limit=datetime_ordered_upper_limit
        )
        self.delete_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.datetime_ordered,
            lower_limit=datetime_ordered_lower_limit,
            upper_limit=datetime_ordered_upper_limit
        )

    def add_update_or_delete_condition_delivery_date_exact(self, delivery_date_value: str):
        """Add the condition for exact company order `delivery_date` for when updating or deleting a company order.
        :type delivery_date_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.delivery_date,
            delivery_date_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.delivery_date,
            delivery_date_value
        )

    def add_update_or_delete_condition_delivery_date_ranged(self,
                                                            delivery_date_lower_limit: str = "",
                                                            delivery_date_upper_limit: str = ""):
        """Add the condition for company order `delivery_date` for when updating or deleting company order(s), where the delivery
        date of the company order is between the input lower limit and input upper limit.
        :type delivery_date_lower_limit: str
        :type delivery_date_upper_limit: str
        """
        self.update_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.delivery_date,
            lower_limit=delivery_date_lower_limit,
            upper_limit=delivery_date_upper_limit
        )
        self.delete_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CompanyOrders.delivery_date,
            lower_limit=delivery_date_lower_limit,
            upper_limit=delivery_date_upper_limit
        )

    def add_update_or_delete_condition_product_gtin14(self, product_gtin14_value: str):
        """Add the condition for company order exact `product_gtin14` for when updating or deleting company order(s).
        :type product_gtin14_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.product_gtin14,
            product_gtin14_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CompanyOrders.product_gtin14,
            product_gtin14_value
        )


class CustomerOrdersTableAdapter(TableAdapter):
    def __init__(self):
        super(CustomerOrdersTableAdapter, self).__init__(
            DatabaseSchemaAndTableName.customer_orders,
            get_text_file_lines_as_single_line(DatabaseQueryFilePath.add_customer_order)
        )

    # SQL SELECT
    def add_select_condition_id(self, id_value: str):
        """Add the condition for exact customer order `id` for when selecting customer order(s).
        :type id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.id,
            id_value
        )

    def add_select_condition_customer_id(self, customer_id_value: str):
        """Add the condition for exact customer order `customer_id` for when selecting customer order(s).
        :type customer_id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.customer_id,
            customer_id_value
        )

    def add_select_condition_datetime_ordered_exact(self, datetime_ordered_value: str):
        """Add the condition for exact customer order `datetime_ordered` for when selecting customer order(s).
        :type datetime_ordered_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.datetime_ordered,
            datetime_ordered_value
        )

    def add_select_condition_datetime_ordered_ranged(self,
                                                     datetime_ordered_lower_limit: str,
                                                     datetime_ordered_upper_limit: str):
        """Add the condition for the customer order `datetime_ordered` for when selecting customer order(s), where the
        customer order datetime ordered value is in between the input lower limit and the input upper limit.
        :type datetime_ordered_lower_limit: str
        :type datetime_ordered_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CustomerOrders.datetime_ordered,
            lower_limit=datetime_ordered_lower_limit,
            upper_limit=datetime_ordered_upper_limit
        )

    def add_select_condition_delivery_date_exact(self, delivery_date_value: str):
        """Add the condition for the exact customer order `delivery_date` for when selecting customer order(s).
        :type delivery_date_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.delivery_date,
            delivery_date_value
        )

    def add_select_condition_delivery_date_ranged(self,
                                                  delivery_date_lower_limit: str = "",
                                                  delivery_date_upper_limit: str = ""):
        """Add the condition for the customer order `delivery_date` for when selecting customer order(s), where the
        actual value for the customer order delivery date is in between the input lower limit and input upper limit.
        :type delivery_date_lower_limit: str
        :type delivery_date_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CustomerOrders.delivery_date,
            lower_limit=delivery_date_lower_limit,
            upper_limit=delivery_date_upper_limit
        )

    def add_select_condition_delivery_location(self, delivery_location_id_value: str):
        """Add the condition for the exact customer order `delivery_location` for when selecting customer order(s).
        :type delivery_location_id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.delivery_location,
            delivery_location_id_value
        )

    # SQL UPDATE

    # SQL UPDATE OR DELETE
    def add_update_or_delete_condition_id(self, id_value: str):
        """Add the condition for the exact customer order `id` for when selecting customer order(s).
        :type id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.id,
            id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.id,
            id_value
        )

    def add_update_or_delete_condition_customer_id(self, customer_id_value: str):
        """Add the condition for the exact customer order `customer_id` for when updating or deleting a customer order.
        :type customer_id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.customer_id,
            customer_id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.customer_id,
            customer_id_value
        )

    def add_update_or_delete_condition_datetime_ordered_exact(self, datetime_ordered_value: str):
        """Add the condition for the exact customer order `datetime_ordered` for when updating or deleting a customer order.
        :type datetime_ordered_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.datetime_ordered,
            datetime_ordered_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.datetime_ordered,
            datetime_ordered_value
        )

    def add_update_or_delete_condition_datetime_ordered_ranged(self,
                                                               datetime_ordered_lower_limit: str = "",
                                                               datetime_ordered_upper_limit: str = ""):
        """Add the condition for the customer order `datetime_ordered` for when updating or deleting customer order(s), where the
        actual value for datetime ordered for the customer order is in between the input lower limit and the input upper
        limit.
        :type datetime_ordered_lower_limit: str
        :type datetime_ordered_upper_limit: str
        """
        self.update_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CustomerOrders.datetime_ordered,
            lower_limit=datetime_ordered_lower_limit,
            upper_limit=datetime_ordered_upper_limit
        )
        self.delete_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CustomerOrders.datetime_ordered,
            lower_limit=datetime_ordered_lower_limit,
            upper_limit=datetime_ordered_upper_limit
        )

    def add_update_or_delete_condition_delivery_location(self, delivery_location_value: str):
        """Add the condition for the exact customer order `delivery_location` for when updating or deleting customer order(s).
        :type delivery_location_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.delivery_location,
            delivery_location_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrders.delivery_location,
            delivery_location_value
        )


class CustomerOrderItemsTableAdapter(TableAdapter):
    def __init__(self):
        super(CustomerOrderItemsTableAdapter, self).__init__(
            DatabaseSchemaAndTableName.customer_order_items,
            get_text_file_lines_as_single_line(DatabaseQueryFilePath.add_customer_order_item)
        )

    # SQL SELECT
    def add_select_condition_customer_order_id(self, customer_order_id_value: str):
        """Add the condition for the exact customer order item `customer_order_id` for when selecting customer order
        item(s).
        :type customer_order_id_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.customer_order_id,
            customer_order_id_value
        )

    def add_select_condition_product_gtin14(self, product_gtin14_value: str):
        """Add the condition for the exact customer order item `product_gtin14` for when selecting customer order
        item(s).
        :type product_gtin14_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.product_gtin14,
            product_gtin14_value
        )

    def add_select_condition_qty_bought_exact(self, qty_bought_value: str):
        """Add the condition for the exact customer order item `qty_bought` for when selecting customer order
        item(s).
        :type qty_bought_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.qty_bought,
            qty_bought_value
        )

    def add_select_condition_qty_bought_ranged(self,
                                               qty_bought_lower_limit: str = "",
                                               qty_bought_upper_limit: str = ""):
        """Add the condition for the customer order item `qty_bought` for when selecting customer order item(s), where
        the actual value for the customer order item quantity bought is between the input lower limit and the input
        upper limit.
        :type qty_bought_lower_limit: str
        :type qty_bought_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CustomerOrderItems.qty_bought,
            lower_limit=qty_bought_lower_limit,
            upper_limit=qty_bought_upper_limit
        )

    def add_select_condition_total_price_paid_exact(self, total_price_paid_value: str):
        """Add the condition for the exact customer order item `total_price_paid` for when selecting customer order
        item(s).
        :type total_price_paid_value: str
        """
        self.select_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.total_price_paid,
            total_price_paid_value
        )

    def add_select_condition_total_price_paid_ranged(self,
                                                     total_price_paid_lower_limit: str = "",
                                                     total_price_paid_upper_limit: str = ""):
        """Add the condition for the customer order item `total_price_paid` for when selecting customer order item(s),
        where the actual value for the customer order item total price paid is between the input lower limit and the
        input upper limit.
        :type total_price_paid_lower_limit: str
        :type total_price_paid_upper_limit: str
        """
        self.select_query_constructor.add_condition_ranged_values(
            DatabaseAttributeName.CustomerOrderItems.total_price_paid,
            lower_limit=total_price_paid_lower_limit,
            upper_limit=total_price_paid_upper_limit
        )

    # SQL UPDATE

    # SQL UPDATE OR DELETE
    def add_update_or_delete_condition_customer_order_id(self, customer_order_id_value: str):
        """Add the condition for the exact customer order item `customer_order_id` for when updating or deleting a customer order
        item.
        :type customer_order_id_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.customer_order_id,
            customer_order_id_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.customer_order_id,
            customer_order_id_value
        )

    def add_update_or_delete_condition_product_gtin14(self, product_gtin14_value: str):
        """Add the condition for the exact customer order item `product_gtin14` for when updating or deleting a customer order item.
        :type product_gtin14_value: str
        """
        self.update_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.product_gtin14,
            product_gtin14_value
        )
        self.delete_query_constructor.add_condition_exact_value(
            DatabaseAttributeName.CustomerOrderItems.product_gtin14,
            product_gtin14_value
        )
