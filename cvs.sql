/*
*********************************************************************
http://www.mysqltutorial.org
*********************************************************************
Name: MySQL Sample Database for Python
Link: http://www.mysqltutorial.org/
Version 1.1
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- 1. 데이터베이스 생성 (한글 지원 설정)
CREATE DATABASE convenience_store_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 2. 생성한 데이터베이스 사용
USE convenience_store_db;

-- 3. Stores 테이블
CREATE TABLE `Stores` (
    `store_id` INT NOT NULL AUTO_INCREMENT COMMENT '매장 ID',
    `store_name` VARCHAR(50) NOT NULL COMMENT '매장 이름',
    `location` VARCHAR(100) NULL COMMENT '매장 위치',
    PRIMARY KEY (`store_id`),
    UNIQUE KEY `uk_store_name` (`store_name`)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 4. Customers 테이블
CREATE TABLE `Customers` (
    `customer_id` INT NOT NULL AUTO_INCREMENT COMMENT '회원번호',
    `name` VARCHAR(15) NOT NULL COMMENT '이름',
    `phone` CHAR(11) NOT NULL COMMENT '전화번호 (01012345678 형식)',
    `gender` ENUM('M', 'F', 'O') NOT NULL DEFAULT 'O' COMMENT '성별 (Male, Female, Other)',
    `join_date` DATE NOT NULL COMMENT '가입 날짜',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시각',
    PRIMARY KEY (`customer_id`),
    UNIQUE KEY `uk_phone` (`phone`)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 5. Logs 테이블
CREATE TABLE `Logs` (
    `log_id` INT NOT NULL AUTO_INCREMENT COMMENT '로그 ID',
    `customer_id` INT NOT NULL COMMENT '회원번호',
    `store_id` INT NOT NULL COMMENT '매장 ID',
    `purchase_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '구매 일시',
    `account` DECIMAL(10) NOT NULL DEFAULT 0 COMMENT '구매 금액',
    PRIMARY KEY (`log_id`),
    FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`) ON DELETE RESTRICT,
    FOREIGN KEY (`store_id`) REFERENCES `Stores` (`store_id`) ON DELETE RESTRICT,
    INDEX `idx_customer_date` (`customer_id`, `purchase_date`)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 6. Grade_Tiers 테이블
CREATE TABLE `Grade_Tiers` (
    `tier_id` INT NOT NULL AUTO_INCREMENT COMMENT '등급 기준 ID',
    `grade_name` VARCHAR(10) NOT NULL COMMENT '등급 이름 (Bronze, Silver, Gold 등)',
    `min_amount` DECIMAL(10) NOT NULL DEFAULT 0.00 COMMENT '최소 누적 금액',
    `max_amount` DECIMAL(10) NULL COMMENT '최대 누적 금액 (NULL이면 상한 없음)',
    `benefit` VARCHAR(255) NULL COMMENT '혜택 설명',
    PRIMARY KEY (`tier_id`),
    UNIQUE KEY `uk_grade_name` (`grade_name`)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 7. Grades 테이블
CREATE TABLE `Grades` (
    `customer_id` INT NOT NULL COMMENT '회원번호',
    `sum_account` DECIMAL(10) NOT NULL DEFAULT 0.00 COMMENT '누적 구매 금액',
    `grade_name` VARCHAR(10) NOT NULL COMMENT '등급 이름',
    `update_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '갱신 일시',
    `last_calculated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '마지막 계산 시각',
    PRIMARY KEY (`customer_id`),
    FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`) ON DELETE CASCADE,
    FOREIGN KEY (`grade_name`) REFERENCES `Grade_Tiers` (`grade_name`) ON DELETE RESTRICT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 8. 샘플 데이터 삽입 (한글 테스트)
INSERT INTO `Stores` (`store_name`, `location`) VALUES
('강남점', '서울 강남구'),
('신촌점', '서울 서대문구');

INSERT INTO `Grade_Tiers` (`grade_name`, `min_amount`, `max_amount`, `benefit`) VALUES
('브론즈', 0, 100000, '5% 할인'),
('실버', 100001, 500000, '10% 할인'),
('골드', 500001, NULL, '15% 할인 + 무료 배송');

INSERT INTO `Customers` (`name`, `phone`, `gender`, `join_date`) VALUES
('김민수', '01012345678', 'M', '2025-01-01'),
('이영희', '01087654321', 'F', '2025-02-01');

INSERT INTO `Logs` (`customer_id`, `store_id`, `purchase_date`, `account`) VALUES
(1, 1, '2025-03-19 14:30:00', 50000),
(2, 2, '2025-03-19 15:00:00', 150000);

INSERT INTO `Grades` (`customer_id`, `sum_account`, `grade_name`, `update_date`) VALUES
(1, 50000, '브론즈', '2025-03-19 14:30:00'),
(2, 150000, '실버', '2025-03-19 15:00:00');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
