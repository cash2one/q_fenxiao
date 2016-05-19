ALTER TABLE `users_distributor`
ADD COLUMN `shop_id` INT NULL DEFAULT NULL COMMENT '分销商对应的店铺id，默认为NULL' AFTER `parent_id`;



ALTER TABLE `item_detail`
DROP COLUMN `is_abroad`,
DROP COLUMN `product_location`,
DROP COLUMN `location`,
DROP COLUMN `is_abroad_send`,
DROP COLUMN `ware_house_id`,
DROP COLUMN `tax_remark`,
DROP COLUMN `tax_rate`,
DROP COLUMN `is_tax`,
CHANGE COLUMN `bussiness_price` `drp_min_price` FLOAT(10,2) NULL DEFAULT '0.00' COMMENT '分销商最低价' ,
ADD COLUMN `drp_max_price` FLOAT(10,2) NULL DEFAULT '0.00' COMMENT '分销商最高价格' AFTER `drp_min_price`;


ALTER TABLE `item_detail`
ADD COLUMN `inner_price` FLOAT(10,2) NULL DEFAULT '0.00' COMMENT '国内销售价格' AFTER `price`;
