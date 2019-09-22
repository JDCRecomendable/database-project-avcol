SELECT * FROM `online_shop_logistics`.`customer_orders`
WHERE (
  customer_id = {} AND
  delivery_location = {}
);
