SELECT id FROM `online_shop_logistics`.`company_orders`
WHERE (
  product_gtin14 = "{}" AND
  datetime_ordered = "{}"
);
