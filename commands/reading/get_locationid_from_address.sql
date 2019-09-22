SELECT id FROM `online_shop_logistics`.`locations`
WHERE (
  city LIKE "%{}%" AND
  road_name LIKE "{}%" AND
  place_no = {}
);
