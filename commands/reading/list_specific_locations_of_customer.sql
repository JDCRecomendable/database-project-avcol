SELECT * FROM `online_shop_logistics`.`locations`
WHERE (id IN (
  SELECT location_id FROM `online_shop_logistics`.`customer_locations`
  WHERE (customer_id = {})
));
