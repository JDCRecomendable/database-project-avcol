SELECT * FROM `online_shop_logistics`.`customer_order_items`
WHERE (customer_order_id IN (
  SELECT id FROM `online_shop_logistics`.`customer_orders`
  WHERE (delivery_location = {})
  ))
));
