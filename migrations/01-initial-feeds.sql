-- 00 syncdb dump
CREATE TABLE `actioncounters_actioncounterunique` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content_type_id` integer NOT NULL,
    `object_pk` varchar(32) NOT NULL,
    `name` varchar(64) NOT NULL,
    `total` integer NOT NULL,
    `ip` varchar(40),
    `session_key` varchar(40),
    `user_agent` varchar(255),
    `user_id` integer,
    `modified` datetime NOT NULL
)
;
-- The following references should be added but depend on non-existent tables:
-- ALTER TABLE `actioncounters_actioncounterunique` ADD CONSTRAINT `user_id_refs_id_48ad09db` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
-- ALTER TABLE `actioncounters_actioncounterunique` ADD CONSTRAINT `content_type_id_refs_id_5e04cd6f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
CREATE INDEX `actioncounters_actioncounterunique_content_type_ididx` ON `actioncounters_actioncounterunique` (`content_type_id`);
CREATE INDEX `actioncounters_actioncounterunique_name_idx` ON `actioncounters_actioncounterunique` (`name`);
CREATE INDEX `actioncounters_actioncounterunique_ip_idx` ON `actioncounters_actioncounterunique` (`ip`);
CREATE INDEX `actioncounters_actioncounterunique_session_key_idx` ON `actioncounters_actioncounterunique` (`session_key`);
CREATE INDEX `actioncounters_actioncounterunique_user_agent_idx` ON `actioncounters_actioncounterunique` (`user_agent`);
CREATE INDEX `actioncounters_actioncounterunique_user_id_idx` ON `actioncounters_actioncounterunique` (`user_id`);

CREATE TABLE `user_profiles` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `deki_user_id` integer UNSIGNED NOT NULL,
    `homepage` varchar(255) NOT NULL,
    `location` varchar(255) NOT NULL,
    `user_id` integer
)
;
-- The following references should be added but depend on non-existent tables:
-- ALTER TABLE `user_profiles` ADD CONSTRAINT `user_id_refs_id_69a818e9` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `user_profiles_idx` ON `user_profiles` (`user_id`);
CREATE TABLE `feeder_bundle_feeds` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `bundle_id` integer NOT NULL,
    `feed_id` integer NOT NULL,
    UNIQUE (`bundle_id`, `feed_id`)
)
;
CREATE TABLE `feeder_bundle` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `shortname` varchar(50) NOT NULL UNIQUE
)
;
ALTER TABLE `feeder_bundle_feeds` ADD CONSTRAINT `bundle_id_refs_id_1a46350d` FOREIGN KEY (`bundle_id`) REFERENCES `feeder_bundle` (`id`);
CREATE TABLE `feeder_feed` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `shortname` varchar(50) NOT NULL UNIQUE,
    `title` varchar(140) NOT NULL,
    `url` varchar(2048) NOT NULL,
    `etag` varchar(140) NOT NULL,
    `last_modified` datetime NOT NULL,
    `enabled` bool NOT NULL,
    `disabled_reason` varchar(2048) NOT NULL,
    `keep` integer UNSIGNED NOT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL
)
;
ALTER TABLE `feeder_bundle_feeds` ADD CONSTRAINT `feed_id_refs_id_55f1514b` FOREIGN KEY (`feed_id`) REFERENCES `feeder_feed` (`id`);
CREATE TABLE `feeder_entry` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `feed_id` integer NOT NULL,
    `guid` varchar(255) NOT NULL,
    `raw` longtext NOT NULL,
    `visible` bool NOT NULL,
    `last_published` datetime NOT NULL,
    `created` datetime NOT NULL,
    `updated` datetime NOT NULL,
    UNIQUE (`feed_id`, `guid`)
)
;
ALTER TABLE `feeder_entry` ADD CONSTRAINT `feed_id_refs_id_3323b4e` FOREIGN KEY (`feed_id`) REFERENCES `feeder_feed` (`id`);
CREATE INDEX `feeder_entry_idx` ON `feeder_entry` (`feed_id`);
-- end 00

INSERT INTO `feeder_feed` (`id`, `shortname`, `url`, `enabled`, `keep`, `created`, `updated`) VALUES
(1, 'moz-hacks', 'http://hacks.mozilla.org/feed/', 1, 50, NOW(), NOW()),
(2, 'tw-mozhacks', 'http://twitter.com/statuses/user_timeline/45496942.rss', 1, 50, NOW(), NOW()),
(3, 'tw-mozillaweb', 'http://twitter.com/statuses/user_timeline/38209403.rss', 1, 50, NOW(), NOW()),
(4, 'tw-mozmobile', 'http://twitter.com/statuses/user_timeline/67033966.rss', 1, 50, NOW(), NOW()),
(5, 'tw-mozillaqa', 'http://twitter.com/statuses/user_timeline/24752152.rss', 1, 50, NOW(), NOW()),
(6, 'planet-mobile', 'http://planet.firefox.com/mobile/rss20.xml', 1, 50, NOW(), NOW()),
(7, 'tw-mozamo', 'http://twitter.com/statuses/user_timeline/15383463.rss', 1, 50, NOW(), NOW()),
(8, 'tw-planetmozilla', 'http://twitter.com/statuses/user_timeline/39292665.rss', 1, 50, NOW(), NOW())
;
