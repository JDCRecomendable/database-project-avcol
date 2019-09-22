SELECT id FROM `online_shop_logistics`.`customer_orders`
WHERE (
  customer_id = {} AND
  datetime_ordered = "{}"
);
