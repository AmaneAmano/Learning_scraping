CREATE TABLE `writers` (
     `id` int(11) unsigned NOT NULL,
     `is_active` tinyint(1) NOT NULL DEFAULT '1',
     `name` varchar(128) NOT NULL DEFAULT '',
     `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
     `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     PRIMARY KEY (`id`)
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
