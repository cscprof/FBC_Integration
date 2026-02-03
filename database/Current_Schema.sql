/*
MySQL Backup
Database: flourish_bc
Backup Time: 2026-01-17 14:16:46
*/

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `flourish_bc`.`content_types`;
DROP TABLE IF EXISTS `flourish_bc`.`event_tags`;
DROP TABLE IF EXISTS `flourish_bc`.`events`;
DROP TABLE IF EXISTS `flourish_bc`.`partners`;
DROP TABLE IF EXISTS `flourish_bc`.`resource_tags`;
DROP TABLE IF EXISTS `flourish_bc`.`resources`;
DROP TABLE IF EXISTS `flourish_bc`.`roles`;
DROP TABLE IF EXISTS `flourish_bc`.`tags`;
DROP TABLE IF EXISTS `flourish_bc`.`users`;
CREATE TABLE `content_types` (
  `content_type_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `event_tags` (
  `event_tag_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`event_tag_id`),
  KEY `event_tags_tags_fk` (`tag_id`),
  KEY `event_tags_event_fk` (`event_id`),
  CONSTRAINT `event_tags_event_fk` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `event_tags_tags_fk` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `content_type` int DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `posting_date` datetime DEFAULT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime DEFAULT NULL,
  `registration_deadline` datetime DEFAULT NULL,
  `user_id` int NOT NULL,
  `status` enum('pending','approved','cancelled') NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `partners` (
  `partner_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `contact_name` varchar(128) DEFAULT NULL,
  `address1` varchar(128) DEFAULT NULL,
  `address2` varchar(128) DEFAULT NULL,
  `city` varchar(128) DEFAULT NULL,
  `state` varchar(32) DEFAULT NULL,
  `zip` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`partner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `resource_tags` (
  `resource_tag_id` int NOT NULL AUTO_INCREMENT,
  `resource_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`resource_tag_id`),
  KEY `resource_tag_resources_fk` (`resource_id`),
  KEY `resource_tag_tags_fk` (`tag_id`),
  CONSTRAINT `resource_tag_resources_fk` FOREIGN KEY (`resource_id`) REFERENCES `resources` (`resource_id`),
  CONSTRAINT `resource_tag_tags_fk` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `resources` (
  `resource_id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(255) DEFAULT NULL,
  `content_type_id` int DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `contact_name` varchar(255) DEFAULT NULL,
  `contact_email` varchar(128) DEFAULT NULL,
  `contact_phone` varchar(32) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`resource_id`),
  KEY `content_types_fk` (`content_type_id`),
  CONSTRAINT `content_types_fk` FOREIGN KEY (`content_type_id`) REFERENCES `content_types` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role` enum('Student','Parent','Guardian','Admin','Partner') NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `tags` (
  `tag_id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(64) NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `middle_name` varchar(64) DEFAULT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `grdauation_year` int DEFAULT NULL,
  `role_id` int NOT NULL,
  `partner_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `users_roles_fk` (`role_id`),
  KEY `partners_roles_fk` (`partner_id`),
  CONSTRAINT `partners_roles_fk` FOREIGN KEY (`partner_id`) REFERENCES `partners` (`partner_id`),
  CONSTRAINT `users_roles_fk` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
BEGIN;
LOCK TABLES `flourish_bc`.`content_types` WRITE;
DELETE FROM `flourish_bc`.`content_types`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`event_tags` WRITE;
DELETE FROM `flourish_bc`.`event_tags`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`events` WRITE;
DELETE FROM `flourish_bc`.`events`;
INSERT INTO `flourish_bc`.`events` (`event_id`,`name`,`description`,`content_type`,`url`,`posting_date`,`start_date`,`end_date`,`registration_deadline`,`user_id`,`status`) VALUES (1, 'Fridays @Geneva', 'campus visit for high school students', NULL, 'https://apply.geneva.edu/portal/campus_visit_events', '2026-01-15 00:00:00', '2026-01-23 09:30:00', '2025-01-23 13:30:00', '2026-01-22 00:00:00', 1, 'approved'),(2, 'Spring Open House', 'Hear from campus leadership, meet faculty and students, tour campus and residence halls. Learn all about about life as a Golden Tornado, from academics and athletics to career outcomes, financial aid, and the student experience.', NULL, 'https://apply.geneva.edu/register/?id=dbc9904c-066e-43d3-834e-dc00a62f9ffa', '2026-01-10 08:30:00', '2026-03-20 08:30:00', '2026-03-20 14:00:00', '2026-03-18 00:00:00', 1, 'approved');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`partners` WRITE;
DELETE FROM `flourish_bc`.`partners`;
INSERT INTO `flourish_bc`.`partners` (`partner_id`,`name`,`description`,`phone`,`email`,`contact_name`,`address1`,`address2`,`city`,`state`,`zip`) VALUES (1, 'Geneva College', 'Liberal arts college located in Beaver Falls', '7246466717', 'admisions@geneva.eduu', 'Kathleen Grehl', '3200 College Ave', NULL, 'Beaver Falls', 'PA', '15010');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`resource_tags` WRITE;
DELETE FROM `flourish_bc`.`resource_tags`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`resources` WRITE;
DELETE FROM `flourish_bc`.`resources`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`roles` WRITE;
DELETE FROM `flourish_bc`.`roles`;
INSERT INTO `flourish_bc`.`roles` (`role_id`,`role`,`description`) VALUES (1, 'Student', 'A student'),(2, 'Parent', 'A parent'),(3, 'Guardian', 'A guardian'),(4, 'Admin', 'An administrator'),(5, 'Partner', 'A third-party user');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`tags` WRITE;
DELETE FROM `flourish_bc`.`tags`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`users` WRITE;
DELETE FROM `flourish_bc`.`users`;
INSERT INTO `flourish_bc`.`users` (`user_id`,`first_name`,`last_name`,`middle_name`,`username`,`password`,`email`,`grdauation_year`,`role_id`,`partner_id`) VALUES (1, 'Kathleen', 'Grehl', NULL, 'kgehl', 'asdfasdf', 'kgrehl@genevaa.edu', NULL, 5, 1);
UNLOCK TABLES;
COMMIT;
