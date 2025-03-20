/*
*********************************************************************
편의점 고객 멤버십 계산 프로그램 데이터베이스
버전: 1.0
날짜: 2025-03-19
*********************************************************************
*/

/*!40101 SET NAMES utf8mb4 */;
/*!40101 SET SQL_MODE='' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `membership_db`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE `membership_db`;

-- 1. Staff 테이블
CREATE TABLE `Staff` (
    `staff_id` INT NOT NULL AUTO_INCREMENT,
    `staff_name` CHAR(4) NULL,
    `staff_phone` CHAR(11) NULL,
    `staff_address` VARCHAR(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
    `staff_gender` ENUM('M', 'F', 'O')  NOT NULL DEFAULT 'O',
    `staff_position` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
    `staff_age` TINYINT NULL,
    `store_id` INT NOT NULL,
    PRIMARY KEY (`staff_id`),
    CONSTRAINT `FK_Stores_TO_Staff` FOREIGN KEY (`store_id`) REFERENCES `Stores` (`store_id`)
);


-- 2. Customers 테이블
CREATE TABLE `Customers` (
    `customer_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    `phone` CHAR(11) NOT NULL UNIQUE,
    `gender` ENUM('M', 'F', 'O') NOT NULL DEFAULT 'O',
    `join_date` DATE NOT NULL DEFAULT (CURRENT_DATE),
    `tier_name` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
    PRIMARY KEY (`customer_id`)
);




-- 3. Grade_Tiers 테이블
CREATE TABLE `Grade_Tiers` (
    `tier_name` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    `tier_description` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (`tier_name`)
);

-- 4. Stores 테이블
CREATE TABLE `Stores` (
    `store_id` INT NOT NULL AUTO_INCREMENT,
    `store_name` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    `location` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
    PRIMARY KEY (`store_id`)
);

-- 5. Logs 테이블
CREATE TABLE `Logs` (
    `log_id` INT NOT NULL AUTO_INCREMENT,
    `customer_id` INT NOT NULL,
    `purchase_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `account` INT NOT NULL,
    `store_id` INT NOT NULL, 
    PRIMARY KEY (`log_id`),
    CONSTRAINT `FK_Customers_TO_Logs` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`),
    CONSTRAINT `FK_Stores_TO_Logs` FOREIGN KEY (`store_id`) REFERENCES `Stores` (`store_id`)
);

-- 6. Benefit 테이블
CREATE TABLE `Benefit` (
    `benefit_id` INT NOT NULL AUTO_INCREMENT,
    `description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
    `discount_rate` INT NULL,
    `points_reward` INT NULL,
    `free_shipping` BOOLEAN NULL,
    `priority_support` BOOLEAN NULL,
    `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`benefit_id`)
);

-- 7. Grades 테이블
CREATE TABLE `Grades` (
    `customer_id` INT NOT NULL,
    `sum_account` INT NOT NULL,
    `update_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `tier_name` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Silver',
    PRIMARY KEY (`customer_id`),
    CONSTRAINT `FK_Customers_TO_Grades` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`),
    CONSTRAINT `FK_Grade_Tiers_TO_Grades` FOREIGN KEY (`tier_name`) REFERENCES `Grade_Tiers` (`tier_name`)
);

-- 8. Benefit_Usage_Logs 테이블
CREATE TABLE `Benefit_Usage_Logs` (
    `usage_id` INT NOT NULL AUTO_INCREMENT COMMENT '사용 로그 ID',
    `usage_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '사용 일시',
    `benefit_id` INT NOT NULL,
    `customer_id` INT NOT NULL,
    `log_id` INT NOT NULL,
    PRIMARY KEY (`usage_id`),
    CONSTRAINT `FK_Benefit_TO_Benefit_Usage_Logs` FOREIGN KEY (`benefit_id`) REFERENCES `Benefit` (`benefit_id`),
    CONSTRAINT `FK_Customers_TO_Benefit_Usage_Logs` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`),
    CONSTRAINT `FK_Logs_TO_Benefit_Usage_Logs` FOREIGN KEY (`log_id`) REFERENCES `Logs` (`log_id`)
);


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- foreign key 제약조건 해제 및 테이블 데이터삭제용
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE Stores;
TRUNCATE TABLE Logs;
TRUNCATE TABLE customers;
TRUNCATE TABLE grades;
TRUNCATE TABLE grade_tiers;
SET FOREIGN_KEY_CHECKS = 1;

select * from customers;
select * from grade_tiers;
select * from  grades;
select * from logs;
select * from stores;
select * from staff;
select * from Benefit_Usage_Logs;

INSERT INTO Staff (staff_name, staff_phone, staff_address, staff_gender, staff_position, staff_age, store_id) VALUES
('김민수', '01012345678', '서울시 강남구', 'M', '매니저', 35, 1),
('이영희', '01023456789', '서울시 서초구', 'F', '캐셔', 28, 2),
('박지훈', '01034567890', '서울시 송파구', 'M', '점장', 42, 3),
('정은지', '01045678901', '서울시 마포구', 'F', '알바', 23, 4),
('최준호', '01056789012', '서울시 노원구', 'M', '알바', 26, 5),
('한지혜', '01067890123', '부산시 해운대구', 'F', '점장', 38, 6),
('강동원', '01078901234', '부산시 서구', 'M', '매니저', 30, 7),
('윤미래', '01089012345', '부산시 남구', 'F', '캐셔', 27, 8),
('배수지', '01090123456', '대구시 중구', 'F', '알바', 24, 9),
('강호동', '01112341234', '대구시 동구', 'M', '점장', 45, 10),
('김희철', '01123452345', '대전시 서구', 'M', '매니저', 34, 11),
('이소라', '01134563456', '대전시 유성구', 'F', '캐셔', 29, 12),
('신동엽', '01145674567', '광주시 동구', 'M', '점장', 41, 13),
('한예슬', '01156785678', '광주시 남구', 'F', '알바', 25, 14),
('김태희', '01167896789', '울산시 중구', 'F', '매니저', 36, 15),
('정우성', '01178907890', '울산시 남구', 'M', '점장', 39, 16),
('이정재', '01189018901', '경기도 성남시', 'M', '매니저', 37, 17),
('송혜교', '01190129012', '경기도 수원시', 'F', '캐셔', 31, 18),
('조인성', '01201230123', '강원도 춘천시', 'M', '알바', 22, 19),
('이병헌', '01212341234', '제주도 제주시', 'M', '점장', 48, 20);

INSERT INTO Customers (name, phone, gender, join_date, tier_name) VALUES
('김철수', '01011112222', 'M', '2024-01-10', 'Silver'),
('이영미', '01022223333', 'F', '2024-02-15', 'Gold'),
('박현우', '01033334444', 'M', '2024-03-20', 'Silver'),
('최유리', '01044445555', 'F', '2024-04-25', 'Vip'),
('정수빈', '01055556666', 'O', '2024-05-05', 'VVip'),
('한세영', '01066667777', 'M', '2023-12-12', 'Gold'),
('이준호', '01077778888', 'M', '2024-01-30', 'Silver'),
('서지민', '01088889999', 'F', '2024-02-14', 'Gold'),
('신민아', '01099990000', 'F', '2024-03-22', 'Vip'),
('강다니엘', '01000001111', 'M', '2024-04-10', 'VVip'),
('김지원', '01111112222', 'F', '2023-11-15', 'Silver'),
('이기광', '01122223333', 'M', '2023-10-05', 'Vip'),
('손나은', '01133334444', 'F', '2024-01-25', 'Gold'),
('차은우', '01144445555', 'M', '2024-02-28', 'VVip'),
('황민현', '01155556666', 'M', '2023-12-20', 'Silver'),
('엄정화', '01166667777', 'F', '2023-09-30', 'Gold'),
('이동욱', '01177778888', 'M', '2024-03-01', 'Vip'),
('전지현', '01188889999', 'F', '2024-04-15', 'VVip'),
('송강호', '01199990000', 'M', '2023-08-10', 'Silver'),
('유재석', '01200001111', 'M', '2023-07-05', 'Gold');

INSERT INTO Logs (customer_id, purchase_date, account, store_id) VALUES
(1, '2024-03-01 14:30:00', 15000, 1),
(2, '2024-03-02 10:15:00', 25000, 2),
(3, '2024-03-05 16:45:00', 50000, 3),
(4, '2024-03-07 18:00:00', 75000, 4),
(5, '2024-03-10 19:30:00', 200000, 5),
(6, '2024-03-12 11:45:00', 120000, 6),
(7, '2024-03-15 15:20:00', 18000, 7),
(8, '2024-03-17 20:30:00', 40000, 8),
(9, '2024-03-18 13:00:00', 90000, 9),
(10, '2024-03-19 17:45:00', 300000, 10),
(11, '2024-03-20 09:30:00', 10000, 11),
(12, '2024-03-21 14:00:00', 220000, 12),
(13, '2024-03-22 16:10:00', 350000, 13),
(14, '2024-03-23 18:45:00', 450000, 14),
(15, '2024-03-24 20:00:00', 50000, 15),
(16, '2024-03-25 21:30:00', 60000, 16),
(17, '2024-03-26 12:15:00', 80000, 17),
(18, '2024-03-27 15:40:00', 95000, 18),
(19, '2024-03-28 19:20:00', 120000, 19),
(20, '2024-03-29 22:00:00', 250000, 20);


INSERT INTO Grade_Tiers (tier_name, tier_description) VALUES
('Silver', '기본 등급'),
('Gold', '누적 10만원 이상'),
('Vip', '누적 20만원 이상'),
('VVip', '누적 50만원 이상');

INSERT INTO Stores (store_name, location) VALUES
('강남점', '서울 강남구 테헤란로 12'),
('서초점', '서울 서초구 반포대로 34'),
('송파점', '서울 송파구 올림픽로 55'),
('마포점', '서울 마포구 독막로 78'),
('노원점', '서울 노원구 동일로 101'),
('해운대점', '부산 해운대구 달맞이길 25'),
('서구점', '부산 서구 충무대로 36'),
('남구점', '부산 남구 대연로 47'),
('중구점', '대구 중구 국채보상로 58'),
('동구점', '대구 동구 신암로 69'),
('서구점', '대전 서구 둔산로 80'),
('유성구점', '대전 유성구 온천로 91'),
('광주 동구점', '광주 동구 문화로 102'),
('광주 남구점', '광주 남구 백운로 113'),
('울산 중구점', '울산 중구 태화로 124'),
('울산 남구점', '울산 남구 문수로 135'),
('성남점', '경기도 성남시 분당구 탄천로 146'),
('수원점', '경기도 수원시 영통구 영통로 157'),
('춘천점', '강원도 춘천시 중앙로 168'),
('제주점', '제주특별자치도 제주시 중앙로 179');

INSERT INTO Benefit (description, discount_rate, points_reward, free_shipping, priority_support) VALUES
('기본 멤버십 혜택', 5, 1000, FALSE, FALSE),
('골드 멤버십 할인', 10, 2000, TRUE, FALSE),
('VIP 멤버십 특별 할인', 15, 5000, TRUE, TRUE),
('VVip 멤버십 전용 혜택', 20, 10000, TRUE, TRUE);

INSERT INTO Grades (customer_id, sum_account, update_date, tier_name) VALUES
(1, 50000, '2024-03-01', 'Silver'),
(2, 150000, '2024-03-02', 'Gold'),
(3, 20000, '2024-03-05', 'Silver'),
(4, 75000, '2024-03-07', 'Silver'),
(5, 230000, '2024-03-10', 'Vip'),
(6, 120000, '2024-03-12', 'Gold'),
(7, 18000, '2024-03-15', 'Silver'),
(8, 40000, '2024-03-17', 'Silver'),
(9, 90000, '2024-03-18', 'Silver'),
(10, 350000, '2024-03-19', 'Vip'),
(11, 10000, '2024-03-20', 'Silver'),
(12, 220000, '2024-03-21', 'Vip'),
(13, 380000, '2024-03-22', 'Vip'),
(14, 600000, '2024-03-23', 'VVip'),
(15, 55000, '2024-03-24', 'Silver'),
(16, 80000, '2024-03-25', 'Silver'),
(17, 95000, '2024-03-26', 'Silver'),
(18, 150000, '2024-03-27', 'Gold'),
(19, 320000, '2024-03-28', 'Vip'),
(20, 600000, '2024-03-29', 'VVip');

INSERT INTO Benefit_Usage_Logs (usage_date, benefit_id, customer_id, log_id) VALUES
('2024-03-01 12:30:00', 1, 1, 1),
('2024-03-02 13:15:00', 2, 2, 2),
('2024-03-05 14:45:00', 1, 3, 3),
('2024-03-07 16:00:00', 1, 4, 4),
('2024-03-10 17:30:00', 3, 5, 5),
('2024-03-12 18:45:00', 2, 6, 6),
('2024-03-15 19:20:00', 1, 7, 7),
('2024-03-17 20:30:00', 1, 8, 8),
('2024-03-18 21:00:00', 1, 9, 9),
('2024-03-19 22:45:00', 4, 10, 10),
('2024-03-20 10:30:00', 1, 11, 11),
('2024-03-21 11:00:00', 3, 12, 12),
('2024-03-22 12:10:00', 3, 13, 13),
('2024-03-23 13:45:00', 4, 14, 14),
('2024-03-24 15:00:00', 1, 15, 15),
('2024-03-25 16:30:00', 1, 16, 16),
('2024-03-26 17:15:00', 1, 17, 17),
('2024-03-27 18:40:00', 2, 18, 18),
('2024-03-28 19:20:00', 3, 19, 19),
('2024-03-29 20:00:00', 4, 20, 20);

