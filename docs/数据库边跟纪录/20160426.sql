---商品表添加分销商信息
    ALTER TABLE `item_detail` ADD COLUMN `is_drp_item` boolean DEFAULT 0 COMMENT '是否分销商自己的商品 1:是 0:否' AFTER `is_online`;
    ALTER TABLE `item_detail` ADD COLUMN `drp_user_id` INT COMMENT '分销商ID' AFTER `is_drp_item`;

---订单商品表添加分销商信息
    ALTER TABLE `item_orders` ADD COLUMN `is_drp_item` boolean DEFAULT 0 COMMENT '是否分销商自己的商品 1:是 0:否' AFTER `item_id`;
    ALTER TABLE `item_orders` ADD COLUMN `drp_user_id` INT COMMENT '分销商ID' AFTER `is_drp_item`;

ALTER TABLE `invoice_orders` ADD COLUMN `supply_id` int  DEFAULT 0 COMMENT '供应商id'

ALTER TABLE `invoice_orders` ADD COLUMN `drp_user_id` INT(11) NULL DEFAULT '0' COMMENT '分销商id' AFTER `supply_id`;




