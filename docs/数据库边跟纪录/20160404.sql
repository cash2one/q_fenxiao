ALTER TABLE `merchant`
ADD COLUMN `account` VARCHAR(128) NOT NULL COMMENT '供应商登陆账号' AFTER `deleted`;

--结算流水表
CREATE TABLE `settlement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gmt_created` datetime DEFAULT NULL,
  `gmt_modified` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `drp_usere_id` int(11) DEFAULT NULL,
  `settlement_no` varchar(128) DEFAULT NULL,
  `settlement_amount` float DEFAULT NULL,
  `payment_no` varchar(128) DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `content` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



ALTER TABLE `item_orders`
ADD COLUMN `supply_user_id` INT NULL DEFAULT 0 COMMENT '供应商id' AFTER `order_no`,
ADD COLUMN `drp_usere_id` INT NULL DEFAULT 0 COMMENT '分销商id' AFTER `supply_user_id`;


ALTER TABLE `refund_orders`
ADD COLUMN `drp_usere_id` INT NULL DEFAULT 0 COMMENT '分销商id' AFTER `order_id`;
