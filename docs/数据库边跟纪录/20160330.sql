-- 支付列表增加结算字段
ALTER TABLE `pay_orders`
ADD COLUMN `settlement` int  DEFAULT 0 COMMENT '是否已结算' AFTER `recevie_address`;

-- 佣金
ALTER TABLE `pay_orders`
ADD COLUMN `brokerage` FLOAT(10,2) NULL DEFAULT '0.00' COMMENT '佣金' AFTER `amount`;

ALTER TABLE `orders`
ADD COLUMN `brokerage` FLOAT(10,2) NULL DEFAULT '0.00' COMMENT '佣金' AFTER `voucher`;

-- 去除保税仓
DROP TABLE `ware_house`;

-- 分销商ID 供应商ID
ALTER TABLE `pay_orders`
ADD COLUMN `drp_usere_id` INT NULL COMMENT '分销商id' AFTER `order_id`,
ADD COLUMN `supply_user_id` INT NULL COMMENT '供应商id' AFTER `drp_usere_id`;

-- 结算编号
ALTER TABLE `pay_orders`
ADD COLUMN `settlement_no` VARCHAR(128) NULL DEFAULT '' COMMENT '结算编号' AFTER `exchange`;

-- 去除订单表里不用的字段
ALTER TABLE `orders`
DROP COLUMN `is_asyn`,
DROP COLUMN `is_abroad`,
DROP COLUMN `house_ware_name`,
DROP COLUMN `house_ware_id`,
DROP COLUMN `tax_amount`;


ALTER TABLE `orders`
ADD COLUMN `drp_usere_id` INT NULL DEFAULT 0 COMMENT '分销商id' AFTER `user_id`,
ADD COLUMN `supply_user_id` INT NULL DEFAULT 0 COMMENT '供应商id' AFTER `drp_usere_id`,
ADD COLUMN `brokerage` FLOAT(10,2) NULL DEFAULT '0.00' COMMENT '' AFTER `real_amount`;

