DELETE FROM `online_shop_logistics`.`locations`
WHERE (
  city = "{}" AND
  road_name = "{}" AND
  place_no = "{}"
);
