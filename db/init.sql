create database music_bot charset "utf8";
use music_bot;
CREATE TABLE data (
  `id`          int(11) NOT NULL AUTO_INCREMENT,
  `artist`      tinytext                                           DEFAULT NULL,
  `album`       text                                               DEFAULT NULL,
  `picture_url` text                                               DEFAULT NULL,
  `review_url`  text                                               DEFAULT NULL,
  `genres`      longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `year`        year(4)                                            DEFAULT NULL,
  `tags`        longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET = utf8;
