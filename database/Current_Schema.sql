/*
MySQL Backup
Database: flourish_bc
Backup Time: 2026-03-04 15:36:30
*/

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `flourish_bc`.`alembic_version`;
DROP TABLE IF EXISTS `flourish_bc`.`content_types`;
DROP TABLE IF EXISTS `flourish_bc`.`event_tags`;
DROP TABLE IF EXISTS `flourish_bc`.`events`;
DROP TABLE IF EXISTS `flourish_bc`.`partners`;
DROP TABLE IF EXISTS `flourish_bc`.`resource_category`;
DROP TABLE IF EXISTS `flourish_bc`.`resource_tags`;
DROP TABLE IF EXISTS `flourish_bc`.`resources`;
DROP TABLE IF EXISTS `flourish_bc`.`roles`;
DROP TABLE IF EXISTS `flourish_bc`.`saved_resources`;
DROP TABLE IF EXISTS `flourish_bc`.`tags`;
DROP TABLE IF EXISTS `flourish_bc`.`users`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `contact_name` varchar(128) DEFAULT NULL,
  `contact_phone` varchar(32) DEFAULT NULL,
  `contact_email` varchar(128) DEFAULT NULL,
  `event_address1` varchar(255) DEFAULT NULL,
  `event_address2` varchar(255) DEFAULT NULL,
  `event_city` varchar(64) DEFAULT NULL,
  `event_state` varchar(64) DEFAULT NULL,
  `event_postal_code` varchar(32) DEFAULT NULL,
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
CREATE TABLE `resource_category` (
  `resource_category_id` int NOT NULL AUTO_INCREMENT,
  `resource_category_name` varchar(32) NOT NULL,
  PRIMARY KEY (`resource_category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `resource_tags` (
  `resource_tag_id` int NOT NULL AUTO_INCREMENT,
  `resource_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`resource_tag_id`),
  KEY `resource_tag_resources_fk` (`resource_id`),
  KEY `resource_tag_tags_fk` (`tag_id`),
  CONSTRAINT `resource_tag_resources_fk` FOREIGN KEY (`resource_id`) REFERENCES `resources` (`resource_id`),
  CONSTRAINT `resource_tag_tags_fk` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `resources` (
  `resource_id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(255) DEFAULT NULL,
  `content_type_id` int DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `contact_name` varchar(255) DEFAULT NULL,
  `contact_email` varchar(128) DEFAULT NULL,
  `contact_phone` varchar(32) DEFAULT NULL,
  `user_id` int NOT NULL,
  `resource_category_id` int NOT NULL,
  PRIMARY KEY (`resource_id`),
  KEY `content_types_fk` (`content_type_id`),
  KEY `resource_category_fk` (`resource_category_id`),
  CONSTRAINT `content_types_fk` FOREIGN KEY (`content_type_id`) REFERENCES `content_types` (`content_type_id`),
  CONSTRAINT `resource_category_fk` FOREIGN KEY (`resource_category_id`) REFERENCES `resource_category` (`resource_category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role` enum('Student','Parent','Guardian','Admin','Partner') NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `saved_resources` (
  `saved_resource_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `resource_id` int DEFAULT NULL,
  PRIMARY KEY (`saved_resource_id`),
  KEY `users__saved_resources_fk` (`user_id`),
  KEY `resourse_saved_resource_id` (`resource_id`),
  CONSTRAINT `resourse_saved_resource_id` FOREIGN KEY (`resource_id`) REFERENCES `resources` (`resource_id`) ON DELETE RESTRICT,
  CONSTRAINT `users__saved_resources_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `tags` (
  `tag_id` int NOT NULL AUTO_INCREMENT,
  `tag` varchar(64) NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `middle_name` varchar(64) DEFAULT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `graduation_year` int DEFAULT NULL,
  `role_id` int NOT NULL,
  `partner_id` int DEFAULT NULL,
  `email_is_verified` BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (`user_id`),
  KEY `users_roles_fk` (`role_id`),
  KEY `partners_roles_fk` (`partner_id`),
  CONSTRAINT `partners_roles_fk` FOREIGN KEY (`partner_id`) REFERENCES `partners` (`partner_id`),
  CONSTRAINT `users_roles_fk` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
BEGIN;
LOCK TABLES `flourish_bc`.`alembic_version` WRITE;
DELETE FROM `flourish_bc`.`alembic_version`;
INSERT INTO `flourish_bc`.`alembic_version` (`version_num`) VALUES ('2da33ec21a26');
UNLOCK TABLES;
COMMIT;
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
INSERT INTO `flourish_bc`.`events` (`event_id`,`name`,`description`,`content_type`,`url`,`posting_date`,`start_date`,`end_date`,`registration_deadline`,`user_id`,`status`,`contact_name`,`contact_phone`,`contact_email`,`event_address1`,`event_address2`,`event_city`,`event_state`,`event_postal_code`) VALUES (1, 'Fridays @Geneva', 'campus visit for high school students', NULL, 'https://apply.geneva.edu/portal/campus_visit_events', '2026-01-15 00:00:00', '2026-01-23 09:30:00', '2025-01-23 13:30:00', '2026-01-22 00:00:00', 1, 'approved', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),(2, 'Spring Open House', 'Hear from campus leadership, meet faculty and students, tour campus and residence halls. Learn all about about life as a Golden Tornado, from academics and athletics to career outcomes, financial aid, and the student experience.', NULL, 'https://apply.geneva.edu/register/?id=dbc9904c-066e-43d3-834e-dc00a62f9ffa', '2026-01-10 08:30:00', '2026-03-20 08:30:00', '2026-03-20 14:00:00', '2026-03-18 00:00:00', 1, 'approved', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`partners` WRITE;
DELETE FROM `flourish_bc`.`partners`;
INSERT INTO `flourish_bc`.`partners` (`partner_id`,`name`,`description`,`phone`,`email`,`contact_name`,`address1`,`address2`,`city`,`state`,`zip`) VALUES (1, 'Geneva College', 'Liberal arts college located in Beaver Falls', '7246466717', 'admisions@geneva.eduu', 'Kathleen Grehl', '3200 College Ave', NULL, 'Beaver Falls', 'PA', '15010');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`resource_category` WRITE;
DELETE FROM `flourish_bc`.`resource_category`;
INSERT INTO `flourish_bc`.`resource_category` (`resource_category_id`,`resource_category_name`) VALUES (1, 'college'),(2, 'scholarship'),(3, 'mental'),(4, 'job'),(5, 'activities'),(6, 'other');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`resource_tags` WRITE;
DELETE FROM `flourish_bc`.`resource_tags`;
INSERT INTO `flourish_bc`.`resource_tags` VALUES (28,15,1),(29,16,2),(30,17,2),(31,18,2),(32,19,2),(33,20,3),(34,21,3),(35,22,4),(36,23,4),(37,24,4),(38,25,4),(39,26,4),(40,27,5),(41,28,5),(42,29,5),(43,30,6),(44,31,6),(45,32,6),(46,33,6),(47,34,7),(48,35,7),(49,36,8),(50,37,8),(51,38,8),(52,39,9),(53,40,9),(54,41,9);
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`resources` WRITE;
DELETE FROM `flourish_bc`.`resources`;
INSERT INTO `flourish_bc`.`resources` VALUES (1,'Geneva College',NULL,'https://www.geneva.edu/',NULL,NULL,NULL,1,1),(2,'Geneva College Counseling Service',NULL,'https://www.geneva.edu/student-life/wellness/counseling/','Amy Solman','alsolman@geneva.edu','724-847-4082',1,3),(3,'Suicide Hotline',NULL,'https://988lifeline.org/',NULL,NULL,'988',1,3),(4,'College Applications (CommonApp)',NULL,'https://www.commonapp.org/',NULL,NULL,NULL,1,1),(5,'NCAA Athletic Eligibility',NULL,'https://web3.ncaa.org/ecwr3/',NULL,NULL,NULL,1,1),(6,'Linkedin',NULL,'https://www.linkedin.com/',NULL,NULL,NULL,1,4),(7,'Handshake for Students',NULL,'https://joinhandshake.com/',NULL,NULL,NULL,1,4),(8,'SuperProf Tutoring',NULL,'https://www.superprof.com/',NULL,NULL,NULL,1,5),(9,'Free Application For Federal Student Aid (FAFSA)',NULL,'https://studentaid.gov/h/apply-for-aid/fafsa',NULL,NULL,NULL,1,1),(10,'Tutor.com',NULL,'https://www.tutor.com/',NULL,NULL,NULL,1,5),(11,'Geneva Campus Visit Events',NULL,'https://apply.geneva.edu/portal/campus_visit_events',NULL,NULL,NULL,1,5),(12,'Scholarships.com',NULL,'https://www.scholarships.com/',NULL,NULL,NULL,1,2),(13,'Geneva College Center for Calling & Career',NULL,'https://www.geneva.edu/calling-career/',NULL,NULL,'724.847.6572',1,4),(15,'Beaver Area High School College in High School',NULL,'https://www.basd.k12.pa.us/CHSCoursesCollegeinHS.aspx',NULL,NULL,NULL,1,1),(16,'Beaver Falls High School Scholarships',NULL,'https://www.tigerweb.org/departments/high-school-guidance-department/college-scholarships-available',NULL,NULL,NULL,1,2),(17,'Beaver Falls High School College Information',NULL,'https://www.tigerweb.org/homepage-links/college-information',NULL,NULL,NULL,1,1),(18,'Beaver Falls High School Stiver Virtual College Exploration',NULL,'https://www.tigerweb.org/our-schools/beaver-falls-high-school/strive-virtual-college-exploration',NULL,NULL,NULL,1,1),(19,'Beaver Falls High School Athletic Eligibility',NULL,'https://www.tigerweb.org/departments/high-school-guidance-department/athletic-eligibility',NULL,NULL,NULL,1,1),(20,'Western Beaver High School Scholarships',NULL,'https://www.westernbeaver.org/o/high-school/page/scholarships',NULL,NULL,NULL,1,2),(21,'Western Beaver High School Dual Enrollment',NULL,'https://www.westernbeaver.org/o/high-school/page/dual-enrollment',NULL,NULL,NULL,1,1),(22,'BlackHawk High School Guidance Department',NULL,'https://www.bsd.k12.pa.us/GuidanceDepartment.aspx',NULL,NULL,'(724) 846-9600',1,3),(23,'BlackHawk High School College and Career Testing',NULL,'https://www.bsd.k12.pa.us/CollegeandCareerTesting.aspx',NULL,NULL,NULL,1,1),(24,'BlackHawk High School Scholarship Opportunities',NULL,'https://www.bsd.k12.pa.us/ScholarshipOpportunities.aspx',NULL,NULL,NULL,1,2),(25,'BlackHawk High School Financial Aid',NULL,'https://www.bsd.k12.pa.us/FinancialAid1.aspx',NULL,NULL,NULL,1,1),(26,'BlackHawk High School Transcript Requests',NULL,'https://www.bsd.k12.pa.us/TranscriptRequests.aspx',NULL,NULL,NULL,1,1),(27,'Rochester High School College in High School',NULL,'https://www.rasd.org/our-district/middle-high/guidance-office/college-in-high-school',NULL,NULL,NULL,1,1),(28,'Rochester High School College Information',NULL,'https://www.rasd.org/our-district/middle-high/guidance-office/college-information-for-students',NULL,NULL,NULL,1,1),(29,'Rochester High School College Fair',NULL,'https://www.rasd.org/toreview/2022-summer-choral-and-instrumental-academy/college-fair',NULL,NULL,NULL,1,1),(30,'Freedom Area Senior High School College in High School',NULL,'https://www.freedomareaschools.org/CollegeinHighSchoolCiHSPrograms.aspx',NULL,NULL,NULL,1,1),(31,'Freedom Area Senior High School College Plannning',NULL,'https://www.freedomareaschools.org/CollegePlanning.aspx',NULL,NULL,NULL,1,1),(32,'Freedom Area Senior High School Transcripts',NULL,'https://www.freedomareaschools.org/HowtoAccessCollegeTranscripts.aspx',NULL,NULL,NULL,1,1),(33,'Freedom Area Senior High School NCAA',NULL,'https://www.freedomareaschools.org/NCAA.aspx',NULL,NULL,NULL,1,1),(34,'Central Valley High School Guidance',NULL,'https://www.centralvalleysd.org/MSGuidance.aspx','Ms. April Marocco',NULL,'724-775-5600 x 13088',1,3),(35,'Central Valley High School Pennsylvania Department of Education Standards',NULL,'https://www.centralvalleysd.org/PDESTANDARDS.aspx',NULL,NULL,NULL,1,1),(36,'Beaver Local High School Guidance Office',NULL,'https://blhs.beaver.k12.oh.us/quick-links/guidance-office',NULL,NULL,'330-386-8700',1,3),(37,'Beaver Local High School Senior Info/Fact Sheet',NULL,'https://docs.google.com/document/d/1a9n3curKzGdQvydKdYngM1wvZiwtEPzCUt7smNL4WQk/edit?tab=t.0',NULL,NULL,NULL,1,1),(38,'Beaver Local High School Transcript Request Form',NULL,'https://docs.google.com/document/d/1A_lYYSiaIY4vqjdIJL2GJW-B6yA_ca4kxkG-t0Ovv0g/edit?tab=t.0',NULL,NULL,NULL,1,1),(39,'Aliquippa Junior/Senior High School College Information',NULL,'https://www.quipsd.org/College.aspx',NULL,NULL,NULL,1,1),(40,'Aliquippa Junior/Senior High School Talent Search Program',NULL,'https://www.quipsd.org/TalentSearchProgram.aspx',NULL,NULL,NULL,1,1),(41,'Aliquippa Junior/Senior High School Scholarships Financial Aid',NULL,'https://www.quipsd.org/ScholarshipsFinancialAid.aspx',NULL,NULL,NULL,1,2);
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`roles` WRITE;
DELETE FROM `flourish_bc`.`roles`;
INSERT INTO `flourish_bc`.`roles` (`role_id`,`role`,`description`) VALUES (1, 'Student', 'A student'),(2, 'Parent', 'A parent'),(3, 'Guardian', 'A guardian'),(4, 'Admin', 'An administrator'),(5, 'Partner', 'A third-party user');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`saved_resources` WRITE;
DELETE FROM `flourish_bc`.`saved_resources`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`tags` WRITE;
DELETE FROM `flourish_bc`.`tags`;
INSERT INTO `flourish_bc`.`tags` (`tag_id`,`tag`) VALUES (1, 'Beaver Area High School'),(2, 'Beaver Falls High School'),(3, 'Western Beaver High School'),(4, 'BlackHawk High School'),(5, 'Rochester'),(6, 'Freedom Area'),(7, 'Central Vally High School'),(8, 'Beaver Local High School'),(9, 'Aliquippa High School');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `flourish_bc`.`users` WRITE;
DELETE FROM `flourish_bc`.`users`;
INSERT INTO `flourish_bc`.`users` (`user_id`,`first_name`,`last_name`,`middle_name`,`username`,`password`,`email`,`graduation_year`,`role_id`,`partner_id`) VALUES (1, 'Kathleen', 'Grehl', NULL, 'kgehl', 'asdfasdf', 'kgrehl@genevaa.edu', NULL, 5, 1);
UNLOCK TABLES;
COMMIT;
