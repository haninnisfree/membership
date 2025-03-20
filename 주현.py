CREATE TABLE `Staff` (
	`Key`	INT	NOT NULL,
	`staff_name`	CHAR((4)	NULL,
	`staff_phone`	INT(11)	NULL,
	`staff_address`	VARCHAR(70)	NULL,
	`staff_gender`	ENUM('M', 'F', 'O')	NULL,
	`staff_position`	VARCHAR(10)	NULL,
	`staff_age`	INT(2)	NULL,
	`store_name`	VARCHAR(50)	NOT NULL
);

CREATE TABLE `Customers` (
	`customer_id`	INT	NOT NULL,
	`name`	VARCHAR(15)	NOT NULL,
	`phone`	CHAR(11)	NOT NULL,
	`gender`	ENUM('M', 'F', 'O')	NOT NULL	DEFAULT 'O',
	`join_date`	DATE	NOT NULL
);

CREATE TABLE `Grade_Tiers` (
	`tier_id`	INT	NOT NULL,
	`grade_name`	VARCHAR(10)	NOT NULL,
	`Key`	INT	NOT NULL
);

CREATE TABLE `Stores` (
	`store_id`	INT	NOT NULL,
	`store_name`	VARCHAR(50)	NOT NULL,
	`location`	VARCHAR(100)	NULL
);

CREATE TABLE `Logs` (
	`log_id`	INT	NOT NULL,
	`customer_id`	INT	NOT NULL,
	`purchase_date`	DATETIME	NOT NULL,
	`account`	DECIMAL(10,)	NOT NULL,
	`store_id`	INT	NOT NULL,
	`store_name`	VARCHAR(50)	NOT NULL
);

CREATE TABLE `Benefit` (
	`Key`	INT	NOT NULL,
	`membership_level`	VARCHAR(50)	NOT NULL,
	`description`	TEXT	NULL,
	`discount_rate`	DECIMAL(5,2)	NULL,
	`points_reward`	INT	NULL,
	`free_shipping`	BOOLEAN	NULL,
	`priority_support`	BOOLEAN	NULL,
	`created_at`	TIMESTAMP	NULL,
	`updated_at`	TIMESTAMP	NULL	DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Grades` (
	`customer_id`	INT	NOT NULL,
	`sum_account`	DECIMAL(10,)	NOT NULL,
	`grade_name`	VARCHAR(10)	NOT NULL,
	`update_date`	DATETIME	NOT NULL,
	`last_calculated_at`	TIMESTAMP	NOT NULL	DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `log` (
	`Key`	VARCHAR(255)	NOT NULL
);

ALTER TABLE `Staff` ADD CONSTRAINT `PK_STAFF` PRIMARY KEY (
	`Key`
);

ALTER TABLE `Customers` ADD CONSTRAINT `PK_CUSTOMERS` PRIMARY KEY (
	`customer_id`
);

ALTER TABLE `Grade_Tiers` ADD CONSTRAINT `PK_GRADE_TIERS` PRIMARY KEY (
	`tier_id`
);

ALTER TABLE `Stores` ADD CONSTRAINT `PK_STORES` PRIMARY KEY (
	`store_id`,
	`store_name`
);

ALTER TABLE `Logs` ADD CONSTRAINT `PK_LOGS` PRIMARY KEY (
	`log_id`
);

ALTER TABLE `Benefit` ADD CONSTRAINT `PK_BENEFIT` PRIMARY KEY (
	`Key`
);

ALTER TABLE `Grades` ADD CONSTRAINT `PK_GRADES` PRIMARY KEY (
	`customer_id`
);

ALTER TABLE `log` ADD CONSTRAINT `PK_LOG` PRIMARY KEY (
	`Key`
);

ALTER TABLE `Grades` ADD CONSTRAINT `FK_Customers_TO_Grades_1` FOREIGN KEY (
	`customer_id`
)
REFERENCES `Customers` (
	`customer_id`
);

