SELECT * FROM `online_shop_logistics`.`customers`
WHERE (id IN (
  SELECT customer_id FROM `online_shop_logistics`.`customer_locations`
  WHERE (location_id = {})
));
