# membership
프로그램명 : 편의점 고객 멤버십 계산 프로그램
목표 : 편의점 고객(회원)들의 누적금액을 통해 멤버십 각 범주별 멤버십 등급을 부여한다. 

[테이블]
 
CREATE TABLE `Staff` (
	`Key`	INT	NOT NULL,
	`staff_name`	CHAR((4)	NULL,
	`staff_phone`	INT(11)	NULL,
	`staff_address`	VARCHAR(70)	NULL,
	`staff_gender`	ENUM('M', 'F', 'O')	NULL,
	`staff_position`	VARCHAR(10)	NULL,
	`staff_age`	TINYINT	NULL,
	`store_id`	INT	NOT NULL
);

CREATE TABLE `Customers` (
	`customer_id`	INT	NOT NULL,
	`name`	VARCHAR(15)	NOT NULL,
	`phone`	CHAR(11)	NOT NULL,
	`gender`	ENUM('M', 'F', 'O')	NOT NULL	DEFAULT 'O',
	`join_date`	DATE	NOT NULL,
	`tier_name`	varcher(10)	NULL
);

CREATE TABLE `Grade_Tiers` (
	`tier_name`	varchar(10)	NULL,
	`tier_description`	VARCHAR(10)	NOT NULL
);

CREATE TABLE `Stores` (
	`store_id`	INT	NOT NULL,
	`location`	VARCHAR(100)	NULL,
	`store_name`	VARCHAR(50)	NOT NULL
);

CREATE TABLE `Logs` (
	`log_id`	INT	NOT NULL,
	`customer_id`	INT	NOT NULL,
	`purchase_date`	DATETIME	NOT NULL,
	`account`	DECIMAL(10,)	NOT NULL,
	`store_id`	INT	NOT NULL
);

CREATE TABLE `Benefit` (
	`Key`	INT	NOT NULL,
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
	`update_date`	DATETIME	NOT NULL,
	`tier_name2`	varchar(10)	NULL
);

CREATE TABLE `Benefit_Usage_Logs` (
	`usage_id`	INT	NOT NULL	COMMENT '사용 로그 ID',
	`usage_date`	DATETIME	NOT NULL	DEFAULT CURRENT_TIMESTAMP	COMMENT '사용 일시',
	`Key`	INT	NOT NULL,
	`customer_id`	INT	NOT NULL,
	`log_id2`	INT	NOT NULL
);

ALTER TABLE `Staff` ADD CONSTRAINT `PK_STAFF` PRIMARY KEY (
	`Key`
);

ALTER TABLE `Customers` ADD CONSTRAINT `PK_CUSTOMERS` PRIMARY KEY (
	`customer_id`
);

ALTER TABLE `Grade_Tiers` ADD CONSTRAINT `PK_GRADE_TIERS` PRIMARY KEY (
	`tier_name`
);

ALTER TABLE `Stores` ADD CONSTRAINT `PK_STORES` PRIMARY KEY (
	`store_id`
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

ALTER TABLE `Benefit_Usage_Logs` ADD CONSTRAINT `PK_BENEFIT_USAGE_LOGS` PRIMARY KEY (
	`usage_id`
);

ALTER TABLE `Grades` ADD CONSTRAINT `FK_Customers_TO_Grades_1` FOREIGN KEY (
	`customer_id`
)
REFERENCES `Customers` (
	`customer_id`
);



[내용]
1. 멤버십 등록
2. 방문자 구매액 입력
3. 구매액에 따른 등급 부여

[인터페이스]
[1. 소비자 2.관리자]
- 등록과 검색(소비자) # 소비자인지 관리자인지 선택하는 문구가 필요 > 선택이 되면 선택이 되면 선택에 따른 인터페이스 선택

[인터페이스 1 소비자]
[1. 멤버십등록 2. 검색(등급과 혜택까지) 3. 종료]
# 인터페이스가 나오고 선택하시오. > 만약 1번이 나오면 고객테이블에 있는 열을 입력하도록 한다(input) 
# 2번 선택하면 회원ID를 입력하라고 하고 정보가 테이블에 있다면 정보를 가져오고 없다면 다시 입력하도록 한다
# 3번은 프로그램 종료


[인터페이스 2 관리자]
- 고객 구매앱 입력과 로그 조회(마켓)
[1. 방문자 구매액 입력(로그데이터 입력용) 2. 고객 로그 조회 3. 수정 4. 삭제 5.종료]
 # 인터페이스가 나오고 선택하시오. > 만약 1번이 나온다면 buy_log테이블에서 해당 회원 ID를 가져온다
 # 커스터머 휴대폰 번호 4자리를 입력하세요 > 입력받은 4자리를 가지고 커스터머스 테이블에서 phone열에 뒷 네자리가 똑같은 회원들을 다 불러낸다.
 # 거기서 맞는 이름을 선택하게 하고 이제 구매액과 매장이름을 입력한다.
 # 2번 고객 로그 조회를 하면 성함을 받고 해당 고객의 매장로그를 다 뽑아낸다. 만약 앤터만 누를 시 상위 10개의 데이터만 조회
 # 3번 수정을 선택하면 이름을 검색하고 커스터머테이블에서 이름이 일치하는 회원을 다 불러낸다. > 맞는 이름 선택하고 수정하게 한다.
 # 4번 삭제를 선택하면 이름을 검색하고 삭제하시겠습니까라는 메시지를 띄운 뒤 y/n 를 확인하여 y면 삭제하게 한다.
 # 5번 종료를 선택하면 프로그램을 종료한다.


