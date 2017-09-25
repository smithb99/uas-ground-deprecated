CREATE TABLE `images` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `image_name` varchar(20) NOT NULL DEFAULT '',
  `confirmed` tinyint(1) DEFAULT NULL,
  `shape` varchar(20) DEFAULT NULL,
  `shape-color` varchar(20) DEFAULT NULL,
  `letter` char(1) DEFAULT NULL,
  `letter-color` varchar(20) DEFAULT NULL,
  `orientation` varchar(20) DEFAULT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;