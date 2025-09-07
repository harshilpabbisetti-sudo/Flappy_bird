DROP DATABASE IF EXISTS `Flappy_Bird`;
CREATE DATABASE `Flappy_Bird`; 
USE `Flappy_Bird`;

CREATE TABLE `login_credentials` (
  `sno` int(11) NOT NULL, 
  `username` char(50) NOT NULL unique,
  `password` varchar(50) NOT NULL unique,
  `easy_high_score` int(11),
  `moderate_high_score` int(11),
  `hard_high_score` int(11),
  PRIMARY KEY (`sno`)
);

INSERT INTO `login_credentials` VALUES (1,'harshil','harshil',12);
INSERT INTO `login_credentials` VALUES (2,'kunal','kunal',11);


