/*
 Navicat MySQL Data Transfer

 Source Server         : 10.69.58.195
 Source Server Type    : MySQL
 Source Server Version : 50718
 Source Host           : 10.69.58.195
 Source Database       : doraemon_nirvana

 Target Server Type    : MySQL
 Target Server Version : 50718
 File Encoding         : utf-8

 Date: 09/26/2018 10:16:04 AM
*/

CREATE DATABASE `team_vision` DEFAULT character SET utf8 collate utf8_general_ci;

use team_vision;

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `agent`
-- ----------------------------
DROP TABLE IF EXISTS `agent`;
CREATE TABLE `agent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `IP` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `OS` int(11) NOT NULL,
  `Status` int(11) NOT NULL,
  `AgentWorkSpace` varchar(255) NOT NULL,
  `AgentTags` varchar(255) NOT NULL,
  `AgentPort` int(11) NOT NULL,
  `Executors` int(11) NOT NULL,
  `RunningExecutors` int(11) NOT NULL,
  `BuildToolsDir` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_group`
-- ----------------------------
BEGIN;
INSERT INTO `auth_group` VALUES ('27', 'Admin'), ('28', 'Manager'), ('29', 'User');
COMMIT;

-- ----------------------------
--  Table structure for `auth_group_extend`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_extend`;
CREATE TABLE `auth_group_extend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `backcolor` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `group_priority` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_group_extend`
-- ----------------------------
BEGIN;
INSERT INTO `auth_group_extend` VALUES ('20', '27', '#32be77', '系统管理员组，拥有所有权限.', '1'), ('21', '28', '#32be77', null, '2'), ('22', '29', '#32be77', '普通用户角色,新建用户的默认组', '3');
COMMIT;

-- ----------------------------
--  Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_13acf6f62506d836_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_13acf6f62506d836_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_33a12a5a8a5bcd3d_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth_p_content_type_id_97df4e2810921f1_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=268 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_permission`
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry'), ('2', 'Can change log entry', '1', 'change_logentry'), ('3', 'Can delete log entry', '1', 'delete_logentry'), ('4', 'Can add permission', '2', 'add_permission'), ('5', 'Can change permission', '2', 'change_permission'), ('6', 'Can delete permission', '2', 'delete_permission'), ('7', 'Can add group', '3', 'add_group'), ('8', 'Can change group', '3', 'change_group'), ('9', 'Can delete group', '3', 'delete_group'), ('10', 'Can add user', '4', 'add_user'), ('11', 'Can change user', '4', 'change_user'), ('12', 'Can delete user', '4', 'delete_user'), ('13', 'Can add content type', '5', 'add_contenttype'), ('14', 'Can change content type', '5', 'change_contenttype'), ('15', 'Can delete content type', '5', 'delete_contenttype'), ('16', 'Can add session', '6', 'add_session'), ('17', 'Can change session', '6', 'change_session'), ('18', 'Can delete session', '6', 'delete_session'), ('19', 'Can add auto task', '7', 'add_autotask'), ('20', 'Can change auto task', '7', 'change_autotask'), ('21', 'Can delete auto task', '7', 'delete_autotask'), ('22', 'Can add auto test config', '8', 'add_autotestconfig'), ('23', 'Can change auto test config', '8', 'change_autotestconfig'), ('24', 'Can delete auto test config', '8', 'delete_autotestconfig'), ('25', 'Can add auto agent', '9', 'add_autoagent'), ('26', 'Can change auto agent', '9', 'change_autoagent'), ('27', 'Can delete auto agent', '9', 'delete_autoagent'), ('28', 'Can add auto mobile device', '10', 'add_automobiledevice'), ('29', 'Can change auto mobile device', '10', 'change_automobiledevice'), ('30', 'Can delete auto mobile device', '10', 'delete_automobiledevice'), ('31', 'Can add auto run result', '11', 'add_autorunresult'), ('32', 'Can change auto run result', '11', 'change_autorunresult'), ('33', 'Can delete auto run result', '11', 'delete_autorunresult'), ('34', 'Can add auto case result', '12', 'add_autocaseresult'), ('35', 'Can change auto case result', '12', 'change_autocaseresult'), ('36', 'Can delete auto case result', '12', 'delete_autocaseresult'), ('37', 'Can add auto service host', '13', 'add_autoservicehost'), ('38', 'Can change auto service host', '13', 'change_autoservicehost'), ('39', 'Can delete auto service host', '13', 'delete_autoservicehost'), ('40', 'Can add auto task queue', '14', 'add_autotaskqueue'), ('41', 'Can change auto task queue', '14', 'change_autotaskqueue'), ('42', 'Can delete auto task queue', '14', 'delete_autotaskqueue'), ('43', 'Can add dic type', '15', 'add_dictype'), ('44', 'Can change dic type', '15', 'change_dictype'), ('45', 'Can delete dic type', '15', 'delete_dictype'), ('46', 'Can add dic data', '16', 'add_dicdata'), ('47', 'Can change dic data', '16', 'change_dicdata'), ('48', 'Can delete dic data', '16', 'delete_dicdata'), ('49', 'Can add test job', '17', 'add_testjob'), ('50', 'Can change test job', '17', 'change_testjob'), ('51', 'Can delete test job', '17', 'delete_testjob'), ('52', 'Can add test project submition', '18', 'add_testprojectsubmition'), ('53', 'Can change test project submition', '18', 'change_testprojectsubmition'), ('54', 'Can delete test project submition', '18', 'delete_testprojectsubmition'), ('55', 'Can add test build history', '19', 'add_testbuildhistory'), ('56', 'Can change test build history', '19', 'change_testbuildhistory'), ('57', 'Can delete test build history', '19', 'delete_testbuildhistory'), ('58', 'Can add test job history', '20', 'add_testjobhistory'), ('59', 'Can change test job history', '20', 'change_testjobhistory'), ('60', 'Can delete test job history', '20', 'delete_testjobhistory'), ('61', 'Can add code commit log', '21', 'add_codecommitlog'), ('62', 'Can change code commit log', '21', 'change_codecommitlog'), ('63', 'Can delete code commit log', '21', 'delete_codecommitlog'), ('64', 'Can add test project', '22', 'add_testproject'), ('65', 'Can change test project', '22', 'change_testproject'), ('66', 'Can delete test project', '22', 'delete_testproject'), ('67', 'Can add project version', '23', 'add_projectversion'), ('68', 'Can change project version', '23', 'change_projectversion'), ('69', 'Can delete project version', '23', 'delete_projectversion'), ('70', 'Can add bug free mapping', '24', 'add_bugfreemapping'), ('71', 'Can change bug free mapping', '24', 'change_bugfreemapping'), ('72', 'Can delete bug free mapping', '24', 'delete_bugfreemapping'), ('73', 'Can add web apps', '25', 'add_webapps'), ('74', 'Can change web apps', '25', 'change_webapps'), ('75', 'Can delete web apps', '25', 'delete_webapps'), ('76', 'Can add dic type', '26', 'add_dictype'), ('77', 'Can change dic type', '26', 'change_dictype'), ('78', 'Can delete dic type', '26', 'delete_dictype'), ('79', 'Can add dic data', '27', 'add_dicdata'), ('80', 'Can change dic data', '27', 'change_dicdata'), ('81', 'Can delete dic data', '27', 'delete_dicdata'), ('82', 'Can add task', '28', 'add_task'), ('83', 'Can change task', '28', 'change_task'), ('84', 'Can delete task', '28', 'delete_task'), ('85', 'Can add version', '29', 'add_version'), ('86', 'Can change version', '29', 'change_version'), ('87', 'Can delete version', '29', 'delete_version'), ('97', 'Can add web hook', '33', 'add_webhook'), ('98', 'Can change web hook', '33', 'change_webhook'), ('99', 'Can delete web hook', '33', 'delete_webhook'), ('100', 'Can add project member', '34', 'add_projectmember'), ('101', 'Can change project member', '34', 'change_projectmember'), ('102', 'Can delete project member', '34', 'delete_projectmember'), ('103', 'Can add project', '35', 'add_project'), ('104', 'Can change project', '35', 'change_project'), ('105', 'Can delete project', '35', 'delete_project'), ('106', 'Can add tag', '36', 'add_tag'), ('107', 'Can change tag', '36', 'change_tag'), ('108', 'Can delete tag', '36', 'delete_tag'), ('109', 'Can add project role', '37', 'add_projectrole'), ('110', 'Can change project role', '37', 'change_projectrole'), ('111', 'Can delete project role', '37', 'delete_projectrole'), ('112', 'Can add user_ extend', '38', 'add_user_extend'), ('113', 'Can change user_ extend', '38', 'change_user_extend'), ('114', 'Can delete user_ extend', '38', 'delete_user_extend'), ('115', 'Can add action log', '39', 'add_actionlog'), ('116', 'Can change action log', '39', 'change_actionlog'), ('117', 'Can delete action log', '39', 'delete_actionlog'), ('118', 'Can add product', '40', 'add_product'), ('119', 'Can change product', '40', 'change_product'), ('120', 'Can delete product', '40', 'delete_product'), ('121', 'Can add file info', '41', 'add_fileinfo'), ('122', 'Can change file info', '41', 'change_fileinfo'), ('123', 'Can delete file info', '41', 'delete_fileinfo'), ('124', 'Can add user_ group_ extend', '42', 'add_user_group_extend'), ('125', 'Can change user_ group_ extend', '42', 'change_user_group_extend'), ('126', 'Can delete user_ group_ extend', '42', 'delete_user_group_extend'), ('127', 'Can add user_ permission_ extend', '43', 'add_user_permission_extend'), ('128', 'Can change user_ permission_ extend', '43', 'change_user_permission_extend'), ('129', 'Can delete user_ permission_ extend', '43', 'delete_user_permission_extend'), ('130', 'Can add device', '44', 'add_device'), ('131', 'Can change device', '44', 'change_device'), ('132', 'Can delete device', '44', 'delete_device'), ('133', 'Can add device management history', '45', 'add_devicemanagementhistory'), ('134', 'Can change device management history', '45', 'change_devicemanagementhistory'), ('135', 'Can delete device management history', '45', 'delete_devicemanagementhistory'), ('142', 'Can add user groups', '51', 'add_usergroups'), ('143', 'Can change user groups', '51', 'change_usergroups'), ('144', 'Can delete user groups', '51', 'delete_usergroups'), ('145', 'Can add Token', '52', 'add_token'), ('146', 'Can change Token', '52', 'change_token'), ('147', 'Can delete Token', '52', 'delete_token'), ('148', 'Can add cors model', '53', 'add_corsmodel'), ('149', 'Can change cors model', '53', 'change_corsmodel'), ('150', 'Can delete cors model', '53', 'delete_corsmodel'), ('151', 'Can add agent', '54', 'add_agent'), ('152', 'Can change agent', '54', 'change_agent'), ('153', 'Can delete agent', '54', 'delete_agent'), ('154', 'Can add error message', '55', 'add_errormessage'), ('155', 'Can change error message', '55', 'change_errormessage'), ('156', 'Can delete error message', '55', 'delete_errormessage'), ('157', 'Can add project module', '56', 'add_projectmodule'), ('158', 'Can change project module', '56', 'change_projectmodule'), ('159', 'Can delete project module', '56', 'delete_projectmodule'), ('163', 'Can add case tag', '58', 'add_casetag'), ('164', 'Can change case tag', '58', 'change_casetag'), ('165', 'Can delete case tag', '58', 'delete_casetag'), ('166', 'Can add task queue', '59', 'add_taskqueue'), ('167', 'Can change task queue', '59', 'change_taskqueue'), ('168', 'Can delete task queue', '59', 'delete_taskqueue'), ('172', 'Can add test application', '61', 'add_testapplication'), ('173', 'Can change test application', '61', 'change_testapplication'), ('174', 'Can delete test application', '61', 'delete_testapplication'), ('175', 'Can add project issue', '62', 'add_projectissue'), ('176', 'Can change project issue', '62', 'change_projectissue'), ('177', 'Can delete project issue', '62', 'delete_projectissue'), ('178', 'Can add mock api', '69', 'add_mockapi'), ('179', 'Can change mock api', '69', 'change_mockapi'), ('180', 'Can delete mock api', '69', 'delete_mockapi'), ('181', 'Can add mock handler', '70', 'add_mockhandler'), ('182', 'Can change mock handler', '70', 'change_mockhandler'), ('183', 'Can delete mock handler', '70', 'delete_mockhandler'), ('184', 'Can add mock response', '71', 'add_mockresponse'), ('185', 'Can change mock response', '71', 'change_mockresponse'), ('186', 'Can delete mock response', '71', 'delete_mockresponse'), ('187', 'Can add ci task flow section', '72', 'add_citaskflowsection'), ('188', 'Can change ci task flow section', '72', 'change_citaskflowsection'), ('189', 'Can delete ci task flow section', '72', 'delete_citaskflowsection'), ('190', 'Can add ci server', '67', 'add_ciserver'), ('191', 'Can change ci server', '67', 'change_ciserver'), ('192', 'Can delete ci server', '67', 'delete_ciserver'), ('193', 'Can add auto case result', '73', 'add_autocaseresult'), ('194', 'Can change auto case result', '73', 'change_autocaseresult'), ('195', 'Can delete auto case result', '73', 'delete_autocaseresult'), ('196', 'Can add ci task flow', '68', 'add_citaskflow'), ('197', 'Can change ci task flow', '68', 'change_citaskflow'), ('198', 'Can delete ci task flow', '68', 'delete_citaskflow'), ('199', 'Can add ci credentials', '65', 'add_cicredentials'), ('200', 'Can change ci credentials', '65', 'change_cicredentials'), ('201', 'Can delete ci credentials', '65', 'delete_cicredentials'), ('202', 'Can add ci task', '63', 'add_citask'), ('203', 'Can change ci task', '63', 'change_citask'), ('204', 'Can delete ci task', '63', 'delete_citask'), ('205', 'Can add ci task flow history', '74', 'add_citaskflowhistory'), ('206', 'Can change ci task flow history', '74', 'change_citaskflowhistory'), ('207', 'Can delete ci task flow history', '74', 'delete_citaskflowhistory'), ('208', 'Can add auto case', '75', 'add_autocase'), ('209', 'Can change auto case', '75', 'change_autocase'), ('210', 'Can delete auto case', '75', 'delete_autocase'), ('211', 'Can add service host', '76', 'add_servicehost'), ('212', 'Can change service host', '76', 'change_servicehost'), ('213', 'Can delete service host', '76', 'delete_servicehost'), ('214', 'Can add ci task plugin', '77', 'add_citaskplugin'), ('215', 'Can change ci task plugin', '77', 'change_citaskplugin'), ('216', 'Can delete ci task plugin', '77', 'delete_citaskplugin'), ('217', 'Can add unit test case result', '78', 'add_unittestcaseresult'), ('218', 'Can change unit test case result', '78', 'change_unittestcaseresult'), ('219', 'Can delete unit test case result', '78', 'delete_unittestcaseresult'), ('220', 'Can add ci deploy service', '66', 'add_cideployservice'), ('221', 'Can change ci deploy service', '66', 'change_cideployservice'), ('222', 'Can delete ci deploy service', '66', 'delete_cideployservice'), ('223', 'Can add auto testing task result', '79', 'add_autotestingtaskresult'), ('224', 'Can change auto testing task result', '79', 'change_autotestingtaskresult'), ('225', 'Can delete auto testing task result', '79', 'delete_autotestingtaskresult'), ('226', 'Can add ci task history', '80', 'add_citaskhistory'), ('227', 'Can change ci task history', '80', 'change_citaskhistory'), ('228', 'Can delete ci task history', '80', 'delete_citaskhistory'), ('229', 'Can add issue filter', '81', 'add_issuefilter'), ('230', 'Can change issue filter', '81', 'change_issuefilter'), ('231', 'Can delete issue filter', '81', 'delete_issuefilter'), ('232', 'Can add project issue resolved result', '82', 'add_projectissueresolvedresult'), ('233', 'Can change project issue resolved result', '82', 'change_projectissueresolvedresult'), ('234', 'Can delete project issue resolved result', '82', 'delete_projectissueresolvedresult'), ('235', 'Can add project issue status', '83', 'add_projectissuestatus'), ('236', 'Can change project issue status', '83', 'change_projectissuestatus'), ('237', 'Can delete project issue status', '83', 'delete_projectissuestatus'), ('238', 'Can add project issue daily statistics', '84', 'add_projectissuedailystatistics'), ('239', 'Can change project issue daily statistics', '84', 'change_projectissuedailystatistics'), ('240', 'Can delete project issue daily statistics', '84', 'delete_projectissuedailystatistics'), ('241', 'Can add project archive', '85', 'add_projectarchive'), ('242', 'Can change project archive', '85', 'change_projectarchive'), ('243', 'Can delete project archive', '85', 'delete_projectarchive'), ('244', 'Can add project issue category', '86', 'add_projectissuecategory'), ('245', 'Can change project issue category', '86', 'change_projectissuecategory'), ('246', 'Can delete project issue category', '86', 'delete_projectissuecategory'), ('247', 'Can add project os version', '87', 'add_projectosversion'), ('248', 'Can change project os version', '87', 'change_projectosversion'), ('249', 'Can delete project os version', '87', 'delete_projectosversion'), ('250', 'Can add project os', '88', 'add_projectos'), ('251', 'Can change project os', '88', 'change_projectos'), ('252', 'Can delete project os', '88', 'delete_projectos'), ('253', 'Can add project code url', '89', 'add_projectcodeurl'), ('254', 'Can change project code url', '89', 'change_projectcodeurl'), ('255', 'Can delete project code url', '89', 'delete_projectcodeurl'), ('256', 'Can add project issue version statistics', '90', 'add_projectissueversionstatistics'), ('257', 'Can change project issue version statistics', '90', 'change_projectissueversionstatistics'), ('258', 'Can delete project issue version statistics', '90', 'delete_projectissueversionstatistics'), ('259', 'Can add issue activity', '64', 'add_issueactivity'), ('260', 'Can change issue activity', '64', 'change_issueactivity'), ('261', 'Can delete issue activity', '64', 'delete_issueactivity'), ('262', 'Can add project phase', '91', 'add_projectphase'), ('263', 'Can change project phase', '91', 'change_projectphase'), ('264', 'Can delete project phase', '91', 'delete_projectphase'), ('265', 'Can add project issue severity', '92', 'add_projectissueseverity'), ('266', 'Can change project issue severity', '92', 'change_projectissueseverity'), ('267', 'Can delete project issue severity', '92', 'delete_projectissueseverity');
COMMIT;

-- ----------------------------
--  Table structure for `auth_permission_extend`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission_extend`;
CREATE TABLE `auth_permission_extend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) NOT NULL,
  `PermissionType` int(11) NOT NULL,
  `Description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `auth_user`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_user`
-- ----------------------------
BEGIN;
INSERT INTO `auth_user` VALUES ('1', 'pbkdf2_sha256$100000$r5or5rIt7Whg$c+6efLZNgOZ4802kSnMgBSJSyOWmjlWjwnjf3A0K4WU=', '2016-06-24 07:39:47', '1', 'admin', '理员', '管', 'teamcat@teamcat.cn', '1', '1', '2014-10-16 09:42:16');
COMMIT;

-- ----------------------------
--  Table structure for `auth_user_extend`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_extend`;
CREATE TABLE `auth_user_extend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `avatar` varchar(255) DEFAULT NULL,
  `side_bars` varchar(255) DEFAULT NULL,
  `dashboard_tools` varchar(255) DEFAULT NULL,
  `shortcuts` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `auth_user_extend_user_id_3f904c19_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `auth_user_groups`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_37d011e4146809f1_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_37d011e4146809f1_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_30233bef851f1278_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=177 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_user_groups`
-- ----------------------------
BEGIN;
INSERT INTO `auth_user_groups` VALUES ('1', '1', '27');
COMMIT;

-- ----------------------------
--  Table structure for `auth_user_groups_teamcat`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups_teamcat`;
CREATE TABLE `auth_user_groups_teamcat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_37d011e4146809f1_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_teamcat_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_teamcat_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=177 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_user_groups_teamcat`
-- ----------------------------
BEGIN;
INSERT INTO `auth_user_groups_teamcat` VALUES ('1', '1', '27');
COMMIT;

-- ----------------------------
--  Table structure for `auth_user_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_7543a650240f224d_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_7543a650240f224d_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_46d89bc6ea1b4ae5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `authtoken_token`
-- ----------------------------
DROP TABLE IF EXISTS `authtoken_token`;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `autotesting_case_result`
-- ----------------------------
DROP TABLE IF EXISTS `autotesting_case_result`;
CREATE TABLE `autotesting_case_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `TestCaseID` int(11) DEFAULT NULL,
  `TaskResultID` int(11) DEFAULT NULL,
  `StartTime` datetime(6) DEFAULT NULL,
  `EndTime` datetime(6) DEFAULT NULL,
  `Result` int(11) DEFAULT NULL,
  `Error` varchar(1000) DEFAULT NULL,
  `StackTrace` mediumtext CHARACTER SET utf8 COLLATE utf8_bin,
  `BugID` int(11) DEFAULT NULL,
  `FailCategoryID` int(11) DEFAULT NULL,
  `ReRunID` int(11) DEFAULT NULL,
  `FailType` int(11) DEFAULT NULL,
  `FailNote` varchar(255) DEFAULT NULL,
  `CaseVersion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=524680 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `autotesting_task_result`
-- ----------------------------
DROP TABLE IF EXISTS `autotesting_task_result`;
CREATE TABLE `autotesting_task_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `TaskHistoryID` int(11) DEFAULT NULL,
  `Total` int(11) DEFAULT '0',
  `Pass` int(11) DEFAULT '0',
  `Fail` int(11) DEFAULT '0',
  `Aborted` int(11) DEFAULT '0',
  `TaskUUID` varchar(128) DEFAULT NULL,
  `ParentResultID` int(11) DEFAULT '0',
  `RuntimeEnv` int(11) DEFAULT '0',
  `AgentID` int(11) DEFAULT NULL,
  `MobileDeviceID` int(11) DEFAULT '0',
  `BuildMessage` varchar(255) DEFAULT NULL,
  `Status` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7699 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `autotesting_testcase`
-- ----------------------------
DROP TABLE IF EXISTS `autotesting_testcase`;
CREATE TABLE `autotesting_testcase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `PackageName` varchar(255) COLLATE utf8_bin NOT NULL,
  `ClassName` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `CaseName` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `CaseType` int(11) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  `ModuleID` int(11) DEFAULT NULL,
  `InterfaceID` int(11) DEFAULT NULL,
  `CaseTag` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `Version` int(11) DEFAULT NULL,
  `Desc` varchar(500) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10279 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



-- ----------------------------
--  Table structure for `case_tag`
-- ----------------------------
DROP TABLE IF EXISTS `case_tag`;
CREATE TABLE `case_tag` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime NOT NULL,
  `IsActive` bit(1) NOT NULL,
  `TagName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `TagDesc` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `case_tag`
-- ----------------------------
BEGIN;
INSERT INTO `case_tag` VALUES ('1', '2017-07-19 15:11:19', b'1', 'ALL', '全部'), ('2', '2017-07-19 14:48:44', b'1', 'EC', '环境检测'), ('3', '2017-07-19 14:49:08', b'1', 'MF', '业务主流程'), ('4', '2017-07-19 14:47:59', b'1', 'BVT', 'BVT 测试');
COMMIT;

-- ----------------------------
--  Table structure for `ci_credentials`
-- ----------------------------
DROP TABLE IF EXISTS `ci_credentials`;
CREATE TABLE `ci_credentials` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `UserName` varchar(100) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `SSHKey` varchar(1000) DEFAULT NULL,
  `Scope` int(11) NOT NULL,
  `CredentialType` int(11) NOT NULL,
  `Creator` int(11) NOT NULL,
  `Description` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `ci_deploy_service`
-- ----------------------------
DROP TABLE IF EXISTS `ci_deploy_service`;
CREATE TABLE `ci_deploy_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ServiceName` varchar(100) NOT NULL,
  `DeployDir` varchar(500) NOT NULL,
  `AccessLog` varchar(1000) DEFAULT NULL,
  `ErrorLog` varchar(1000) DEFAULT NULL,
  `StartCommand` varchar(500) DEFAULT NULL,
  `StopCommand` varchar(500) DEFAULT NULL,
  `RestartCommand` varchar(500) DEFAULT NULL,
  `RelatedFiles` varchar(500) DEFAULT NULL,
  `DeployScripts` varchar(500) DEFAULT NULL,
  `AdvanceConfig` varchar(50) DEFAULT NULL,
  `Project` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `ci_flowsection_history`
-- ----------------------------
DROP TABLE IF EXISTS `ci_flowsection_history`;
CREATE TABLE `ci_flowsection_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `TaskFlow` int(11) NOT NULL,
  `Status` int(11) NOT NULL,
  `StartTime` datetime(6) DEFAULT NULL,
  `EndTime` datetime(6) DEFAULT NULL,
  `StartedBy` int(11) NOT NULL,
  `TQUUID` varchar(500) DEFAULT NULL,
  `TaskFlowHistory` int(11) DEFAULT NULL,
  `Section` int(11) DEFAULT NULL,
  `BuildMessage` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `ci_server`
-- ----------------------------
DROP TABLE IF EXISTS `ci_server`;
CREATE TABLE `ci_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ServerName` varchar(100) NOT NULL,
  `Host` varchar(100) NOT NULL,
  `RemoteDir` varchar(200) DEFAULT NULL,
  `Port` int(11) NOT NULL,
  `Scope` int(11) NOT NULL,
  `Description` varchar(100) DEFAULT NULL,
  `Creator` int(11) NOT NULL,
  `Credential` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `ci_servicehost`
-- ----------------------------
DROP TABLE IF EXISTS `ci_servicehost`;
CREATE TABLE `ci_servicehost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `EnvID` int(11) NOT NULL,
  `HostIP` varchar(20) NOT NULL,
  `HostService` varchar(255) NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `IsActive` bit(1) NOT NULL,
  `CreateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `ci_servicehost`
-- ----------------------------
BEGIN;
INSERT INTO `ci_servicehost` VALUES ('1', '1', '123.58.180.8', '163.com', null, b'1', null);
COMMIT;

-- ----------------------------
--  Table structure for `ci_task`
-- ----------------------------
DROP TABLE IF EXISTS `ci_task`;
CREATE TABLE `ci_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `TaskName` varchar(150) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Project` int(11) NOT NULL,
  `TaskType` int(11) NOT NULL,
  `TaskConfig` varchar(50) NOT NULL,
  `DeployService` int(11) NOT NULL,
  `TaskHistory` int(11) NOT NULL,
  `Tags` varchar(50) DEFAULT NULL,
  `LastRunTime` datetime(6) DEFAULT NULL,
  `Schedule` varchar(30) DEFAULT NULL,
  `Creator` int(11) NOT NULL,
  `Description` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `BuildVersion` int(11) NOT NULL,
  `HistoryCleanStrategy` int(11) NOT NULL,
  `LastHistory` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `ci_task_history`
-- ----------------------------
DROP TABLE IF EXISTS `ci_task_history`;
CREATE TABLE `ci_task_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `CITaskID` int(11) NOT NULL,
  `StartTime` datetime(6) DEFAULT NULL,
  `EndTime` datetime(6) DEFAULT NULL,
  `Tags` varchar(50) DEFAULT NULL,
  `PackageID` varchar(500) DEFAULT NULL,
  `LogFileID` varchar(500) DEFAULT NULL,
  `ChangeLog` varchar(1000) DEFAULT NULL,
  `BuildStatus` int(11) NOT NULL,
  `BuildLogID` int(11) NOT NULL,
  `TaskQueueID` int(11) NOT NULL,
  `BuildMessage` varchar(255) DEFAULT NULL,
  `BuildErrorCode` int(11) DEFAULT '0',
  `CodeVersion` varchar(255) DEFAULT NULL,
  `StartedBy` int(11) NOT NULL,
  `BuildVersion` int(11) NOT NULL,
  `ProjectVersion` int(11) NOT NULL,
  `PackageInfo` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `BuildParameterID` varchar(30) DEFAULT NULL,
  `AgentID` int(11) DEFAULT '0',
  `TaskUUID` varchar(255) DEFAULT NULL,
  `FlowSectionHistory` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7194 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `ci_task_plugin`
-- ----------------------------
DROP TABLE IF EXISTS `ci_task_plugin`;
CREATE TABLE `ci_task_plugin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `PluginName` varchar(50) NOT NULL,
  `PluginSection` varchar(50) NOT NULL,
  `PluginLabelColor` varchar(10) NOT NULL,
  `Description` varchar(500) DEFAULT NULL,
  `TaskType` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `ci_task_plugin`
-- ----------------------------
BEGIN;
INSERT INTO `ci_task_plugin` VALUES ('1', '2016-07-01 11:48:14', '1', '    SVN', '2,', 'green', 'SVN插件', '1,4,5'), ('2', '2016-07-01 11:48:48', '1', '    GIT', '2,', 'red', 'GIT插件', '1,4,5'), ('3', '2016-07-01 11:49:10', '1', '    Shell 命令行', '1,2,3,4', 'orange', 'Shell命令行', '1,4,5'), ('4', '2016-10-17 11:51:07', '1', '    命令行构建', '3,', '#87481f', '命令行构建工具', '1,4,5'), ('5', '2016-10-31 14:48:33', '1', '    Gradle构建', '3,', '#faa755', 'Gradle构建', '1,4,5'), ('6', '2016-10-31 14:50:00', '1', '    IOS构建', '3,', '#f26522', 'IOS构建', '1,4,5'), ('7', '2016-10-31 15:25:53', '1', '    Ant构建', '3,', '#102b6a', 'Ant构建', '1,4,5'), ('8', '2016-11-02 13:44:53', '1', '    SSH文件替换', '3,', '#de773f', '服务文件替换', '1,4,5,'), ('9', '2016-11-03 13:40:41', '1', '    SSH部署', '3,', '#8f4b2e', '服务部署', '1,4,5,'), ('10', '2016-11-04 11:58:24', '1', '    IOS命令行构建', '3,', '#585eaa', 'IOS命令行构建', '1,4,5'), ('11', '2016-12-13 11:24:01', '1', '    Copy to Server', '1,2,3,4', '#80752c', 'Copy2Server', '1,4,5'), ('12', '2017-02-08 11:47:33', '1', '     接口测试', '3,4', '#f15b6c', '接口测试', '1,4,5'), ('13', '2017-03-21 14:38:40', '1', '     XCode配置检查', '2,3,4', '#454926', 'XCode配置检查', '1,4,5'), ('14', '2018-01-10 14:14:17', '1', '     XCTest测试', '2,3,4', '#6b473c', 'XCTest测试', '1,4,5'), ('15', '2018-03-02 14:32:04', '1', '     Selenium', '2,3,4', '#b7ba6b', 'WebUI测试', '1,4,5');
COMMIT;

-- ----------------------------
--  Table structure for `ci_taskflow`
-- ----------------------------
DROP TABLE IF EXISTS `ci_taskflow`;
CREATE TABLE `ci_taskflow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `FlowName` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Project` int(11) NOT NULL,
  `LastRunStatus` int(11) NOT NULL,
  `LastRunTime` datetime(6) DEFAULT NULL,
  `Creator` int(11) NOT NULL,
  `Description` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `LastHistory` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `ci_taskflow_history`
-- ----------------------------
DROP TABLE IF EXISTS `ci_taskflow_history`;
CREATE TABLE `ci_taskflow_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `TaskFlow` int(11) NOT NULL,
  `Status` int(11) NOT NULL,
  `StartTime` datetime(6) DEFAULT NULL,
  `EndTime` datetime(6) DEFAULT NULL,
  `StartedBy` int(11) NOT NULL,
  `TQUUID` varchar(500) DEFAULT NULL,
  `BuildMessage` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `ci_taskflow_section`
-- ----------------------------
DROP TABLE IF EXISTS `ci_taskflow_section`;
CREATE TABLE `ci_taskflow_section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `SectionName` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `TaskFlow` int(11) NOT NULL,
  `SectionOrder` int(11) NOT NULL,
  `CITasks` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `device_management`
-- ----------------------------
DROP TABLE IF EXISTS `device_management`;
CREATE TABLE `device_management` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceNumber` varchar(10) NOT NULL,
  `DeviceName` varchar(100) NOT NULL,
  `DeviceOS` int(11) NOT NULL,
  `DeviceOSVersion` int(11) NOT NULL,
  `DeviceScreenSize` int(11) NOT NULL,
  `DeviceStatus` int(11) NOT NULL,
  `DeviceType` int(11) NOT NULL,
  `DeviceSerialNum` varchar(100) DEFAULT NULL,
  `DeviceAvatar` int(11) NOT NULL,
  `DeviceBorrower` int(11) NOT NULL,
  `DeviceBorrorwTime` datetime DEFAULT NULL,
  `DeviceReturnTime` datetime DEFAULT NULL,
  `IsActive` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8;



-- ----------------------------
--  Table structure for `device_management_history`
-- ----------------------------
DROP TABLE IF EXISTS `device_management_history`;
CREATE TABLE `device_management_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` int(11) NOT NULL,
  `DeviceBorrower` int(11) NOT NULL,
  `DeviceBorrorwTime` datetime NOT NULL,
  `DeviceReturnTime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=239 DEFAULT CHARSET=utf8;



-- ----------------------------
--  Table structure for `dicdata`
-- ----------------------------
DROP TABLE IF EXISTS `dicdata`;
CREATE TABLE `dicdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DicType_id` int(11) NOT NULL,
  `DicDataName` varchar(500) NOT NULL,
  `DicDataValue` int(11) NOT NULL,
  `DicDataDesc` varchar(500) DEFAULT NULL,
  `DicDataIsActive` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dicdata_DicType_id_74ecac2420247de7_fk_dictype_id` (`DicType_id`),
  CONSTRAINT `dicdata_DicType_id_74ecac2420247de7_fk_dictype_id` FOREIGN KEY (`DicType_id`) REFERENCES `dictype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=315 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `dicdata`
-- ----------------------------
BEGIN;
INSERT INTO `dicdata` VALUES ('3', '2', 'SDK', '1', 'SDKQA', '1'), ('4', '2', '媒体', '2', 'MediaQA', '1'), ('5', '2', '接口', '3', 'InterfaceQA', '1'), ('9', '4', '新建', '1', '', '1'), ('10', '4', '已提测', '2', '', '1'), ('11', '4', '开始测试', '3', '', '1'), ('12', '5', 'Android', '1', '', '1'), ('13', '5', 'WindowsPhone', '2', '', '0'), ('14', '5', 'IOS', '3', '', '1'), ('15', '6', '10.3.254.114:8080', '1', '10.3.254.114', '1'), ('16', '6', '10.3.254.34:8080', '2', '10.3.254.34', '1'), ('17', '7', 'smtp.teamcat.com', '1', 'emailhost', '1'), ('18', '7', 'gedqa', '2', 'user', '1'), ('19', '7', '', '3', 'password', '1'), ('20', '7', 'teamcat.com', '4', 'postfix', '1'), ('23', '7', '/web/www/teamcat/doraemon/static/project/contents/commit_testing_emailtemplate.html', '5', 'emailsubmitiontemplatepath', '1'), ('25', '7', '/web/www/teamcat/doraemon/static/project/contents/build_package_emailtemplate.html', '6', 'emailbuildtemplatepath', '1'), ('26', '7', 'zhangtiande@teamcat.com,lusiyuan@teamcat.com,yuanqingrong@teamcat.com', '7', 'defautrecivers', '1'), ('41', '2', '自测', '4', 'DevTest', '1'), ('52', '7', '/web/www/doraemon_rtm/doraemon/static/testjob/contents/testjob_emailtemplate.html', '8', 'email_testjob_template', '1'), ('53', '5', 'PC', '4', '', '1'), ('85', '1', 'Completed', '1', '', '1'), ('86', '1', 'Fail', '2', '', '1'), ('87', '1', 'TimeOut', '4', '', '1'), ('88', '1', 'Aborted', '3', '', '1'), ('89', '12', 'Android', '1', 'APP', '1'), ('90', '12', 'IOS', '2', 'APP', '1'), ('91', '12', 'IE6', '3', 'WEB', '1'), ('92', '12', 'IE7', '4', 'WEB', '1'), ('93', '12', 'IE8', '5', 'WEB', '1'), ('94', '12', 'IE9', '6', 'WEB', '1'), ('95', '12', 'IE10', '7', 'WEB', '1'), ('96', '12', 'IE11', '8', 'WEB', '1'), ('97', '12', 'Edge', '9', 'WEB', '1'), ('98', '12', 'Chrome', '10', 'WEB', '1'), ('99', '12', 'FireFox', '11', 'WEB', '1'), ('100', '13', 'Interface', '1', '', '1'), ('101', '13', 'WebUI', '2', '', '1'), ('102', '13', 'APPUI', '3', '', '1'), ('103', '14', 'Win8', '1', '', '1'), ('104', '14', 'Linux', '2', '', '1'), ('105', '14', 'Win7', '3', '', '1'), ('106', '14', 'WinXP', '4', '', '1'), ('107', '14', 'Win10', '5', '', '1'), ('108', '15', 'Running', '1', '', '1'), ('109', '15', 'Online', '2', '', '1'), ('110', '15', 'Offline', '3', '', '1'), ('111', '16', 'TaskWaitTimeout', '7200000', '', '1'), ('112', '16', 'TaskRunTimeout', '7200000', '', '1'), ('113', '17', 'NoProcess', '1', '', '1'), ('114', '18', 'DefautAndroidUI', '1', '', '1'), ('115', '18', 'DefaultWebUI', '2', '', '1'), ('116', '18', 'DefaultInterface', '3', '', '1'), ('117', '19', 'Start', '1', '', '1'), ('118', '19', 'Stop', '2', '', '1'), ('119', '17', 'NoAssign', '2', '', '1'), ('120', '17', 'Assigned', '3', '', '1'), ('121', '17', 'AssignFail', '6', '', '1'), ('122', '17', 'Aborted', '7', '', '1'), ('123', '17', 'Complete', '5', '', '1'), ('124', '17', 'Error', '9', '', '1'), ('125', '20', 'NotRun', '0', '', '1'), ('126', '20', 'Ignore', '1', '', '1'), ('127', '20', 'Fail', '2', '', '1'), ('128', '20', 'Pass', '3', '', '1'), ('129', '21', 'VEDQA-AutoTest', '1', '', '1'), ('130', '21', '226', '2', '', '0'), ('131', '21', '227', '3', '', '0'), ('132', '22', '4.0', '1', '', '1'), ('133', '22', '2.3', '2', '', '1'), ('134', '23', '6.0', '1', '', '1'), ('135', '23', '6.1', '2', '', '1'), ('136', '15', 'Assigned', '4', '', '1'), ('137', '19', 'Timeout', '3', '', '1'), ('138', '17', 'Timeout', '8', '', '1'), ('139', '24', 'SplitCount', '3', '', '1'), ('140', '17', 'Running', '4', '', '1'), ('141', '24', 'TimerInterval', '5000', '', '1'), ('142', '24', 'ControllerInterval', '10000', '', '1'), ('143', '24', 'AgentDetcterInterval', '60000', '', '1'), ('144', '25', 'Running', '1', '', '1'), ('145', '25', 'Online', '2', '', '1'), ('146', '25', 'Offline', '3', '', '1'), ('147', '25', 'Assigned', '4', '', '1'), ('148', '26', 'DevScanInterval', '30000', '', '1'), ('149', '26', 'TaskScanInterval', '5000', '', '1'), ('150', '26', 'AgentDefaultPort', '8099', '', '1'), ('151', '26', 'AgentDefaultSpace', '0', './workspace', '1'), ('152', '26', 'FtpServer', '0', '10.2.45.50', '1'), ('153', '26', 'FtpPort', '21', '', '1'), ('154', '26', 'FtpUser', '0', 'root', '1'), ('155', '26', 'FtpPasswd', '0', '123456', '1'), ('156', '26', 'FtpRootDir', '0', 'archives', '1'), ('157', '19', 'SendResultEmail', '4', '', '1'), ('158', '26', 'WifiConnectTimeout', '180000', '', '1'), ('159', '26', 'rerunTimeDefualt', '1', '', '1'), ('160', '26', 'rerunIsUpdateResult', '1', '', '1'), ('161', '19', 'RerunCase', '5', '', '1'), ('162', '16', 'LockTimeout', '180000', '', '1'), ('163', '27', 'Bug', '1', null, '1'), ('164', '27', 'Home', '2', null, '1'), ('165', '27', 'Project', '3', null, '1'), ('166', '27', 'Task', '4', null, '1'), ('167', '27', 'ForTesting', '5', null, '1'), ('168', '27', 'User', '6', null, '1'), ('169', '27', 'UserGroup', '7', null, '1'), ('170', '27', 'Permission', '8', null, '1'), ('171', '27', 'Device', '9', null, '1'), ('172', '28', 'Android', '1', null, '1'), ('173', '28', 'IOS', '2', null, '1'), ('174', '28', 'WP', '3', null, '1'), ('175', '29', '8.0', '1', null, '1'), ('176', '29', '10.0', '2', null, '1'), ('177', '30', '1024x768', '8', '', '1'), ('178', '30', '1080*1920', '19', '', '1'), ('179', '30', '1136*640', '15', '', '1'), ('180', '30', '1280*720', '16', '', '1'), ('181', '30', '1280*768', '20', '', '1'), ('182', '30', '1280×800', '10', '', '1'), ('183', '30', '13334x750', '4', '', '1'), ('184', '30', '1800*1080', '11', '', '1'), ('185', '30', '1920*1080', '7', '', '1'), ('186', '30', '1920*1152', '1', '', '1'), ('187', '30', '2048×1536', '9', '', '1'), ('188', '30', '2048x1536', '3', '', '1'), ('189', '30', '2048x1536', '17', '', '1'), ('190', '30', '2560×1440', '2', '', '1'), ('191', '30', '480*320', '13', '', '1'), ('192', '30', '480*800', '18', '', '1'), ('193', '30', '480*854', '12', '', '1'), ('194', '30', '720x1280', '6', '', '1'), ('195', '30', '960x540', '5', '', '1'), ('196', '30', '960x640', '14', '', '1'), ('197', '31', '测试设备', '1', null, '1'), ('198', '31', '开发设备', '2', null, '1'), ('199', '31', 'Android配件', '4', null, '1'), ('200', '31', 'IOS配件', '5', null, '1'), ('201', '31', '其他配件', '6', null, '1'), ('202', '28', 'None', '0', null, '1'), ('203', '30', 'None', '0', null, '1'), ('204', '22', 'None', '0', null, '1'), ('205', '23', 'None', '0', null, '1'), ('206', '29', 'None', '0', null, '1'), ('207', '32', '可用', '1', null, '1'), ('208', '32', '出借', '2', null, '1'), ('209', '32', '预定', '3', null, '1'), ('211', '33', '设备', '-1', '设备的统一项目ID', '1'), ('212', '27', 'Bug', '1', null, '1'), ('213', '22', '4.4', '3', null, '1'), ('214', '22', '4.3', '4', null, '1'), ('215', '23', '9.2', '4', null, '1'), ('216', '23', '8.0', '5', null, '1'), ('217', '23', '7.0.4', '6', null, '1'), ('218', '23', '9.1', '7', null, '1'), ('219', '23', '8.3', '8', null, '1'), ('220', '23', '8.1.3', '9', null, '1'), ('221', '23', '9.3', '10', null, '1'), ('222', '22', '4.4.4', '5', null, '1'), ('223', '22', '2.3.3', '6', null, '1'), ('224', '22', '2.3.7', '7', null, '1'), ('225', '30', '320x240', '21', null, '1'), ('226', '22', '5.0.1', '8', null, '1'), ('227', '22', '4.4.2', '9', null, '1'), ('228', '22', '6.0', '10', null, '1'), ('229', '22', '2.3.6', '11', null, '1'), ('230', '22', '6.0.1', '12', null, '1'), ('231', '30', '2208x1242', '22', null, '1'), ('232', '23', '9.2.1', '11', null, '1'), ('233', '23', '6.0.1', '12', null, '1'), ('234', '23', '8.1', '13', null, '1'), ('235', '23', '5.1.1', '14', null, '1'), ('236', '23', '8.1.2', '15', null, '1'), ('237', '23', '10.0', '16', null, '1'), ('238', '34', '通用标签', '1', null, '1'), ('239', '34', 'CI标签', '2', null, '1'), ('240', '34', 'AgentFilterTag', '3', null, '1'), ('241', '35', 'UserPassword', '1', '用户名密码形式', '1'), ('242', '35', 'SSH Key', '2', 'SSH Key with username', '1'), ('243', '13', 'Build', '4', null, '1'), ('244', '13', 'Deploy', '5', null, '1'), ('245', '36', 'CI', '1', null, '1'), ('246', '37', '\'zip\',\'apk\',\'ipa\',\'py\',\'sh\',\'war\',\'jsp\',\'txt\'', '1', null, '1'), ('247', '37', '600*1024*1024', '2', null, '1'), ('248', '14', 'Mac', '6', null, '1'), ('249', '39', 'Always check out a fresh copy', '1', null, '1'), ('250', '39', 'Use svn update as much as possible', '2', null, '1'), ('251', '38', 'Wipe out & shallow clone (无变更日志,耗时短)', '1', null, '1'), ('252', '38', 'Wipe out & full clone (有变更日志,耗时长)', '2', null, '1'), ('253', '17', 'Disaster', '10', null, '1'), ('254', '40', 'Default', '20', 'JDK', '1'), ('255', '40', 'JDK6', '1', 'JDK', '1'), ('256', '40', 'JDK7', '2', 'JDK', '1'), ('257', '40', 'JDK8', '3', 'JDK', '1'), ('258', '40', 'Default', '22', 'GRADLE', '1'), ('259', '40', 'Gradle-1.10', '5', 'GRADLE', '0'), ('260', '40', 'Gradle-2.1', '6', 'GRADLE', '0'), ('261', '40', 'Gradle-2.2.1', '7', 'GRADLE', '0'), ('262', '40', 'Gradle-2.4', '8', 'GRADLE', '0'), ('263', '40', 'Gradle-2.7', '9', 'GRADLE', '0'), ('264', '40', 'Gradle-2.10', '10', 'GRADLE', '0'), ('265', '40', 'Gradle-3.4.1', '11', 'GRADLE', '1'), ('266', '40', 'Default', '21', 'XCODE', '1'), ('267', '40', 'Xcode-6', '13', 'XCODE', '1'), ('268', '40', 'Xcode-7', '14', 'XCODE', '1'), ('269', '24', 'DisasterInterval', '3600000', null, '1'), ('270', '40', '忽略', '19', 'PODS', '1'), ('271', '40', '安装且编译', '16', 'PODS', '1'), ('272', '40', '仅安装', '17', 'PODS', '1'), ('273', '40', '仅编译', '18', 'PODS', '1'), ('274', '5', 'Web', '6', null, '1'), ('275', '38', 'revert & update(有变更日志)', '3', null, '1'), ('276', '40', 'JDK9', '4', 'JDK', '1'), ('277', '40', 'Xcode-8', '15', 'XCODE', '1'), ('278', '40', 'Gradle-3.1', '12', 'GRADLE', '1'), ('279', '24', 'TaskLimit', '4', null, '1'), ('280', '16', 'SocketTimeout', '180000', null, '1'), ('281', '23', '10.0.1', '17', null, '1'), ('282', '23', '10.0.2', '18', null, '1'), ('283', '23', '10.1.1', '19', null, '1'), ('284', '23', '8.4.1', '20', null, '1'), ('285', '22', '7.0', '13', null, '1'), ('286', '22', '5.0.2', '14', null, '1'), ('287', '22', '5.1', '15', null, '1'), ('288', '22', '5.1.1', '16', null, '1'), ('289', '23', '7.1.2', '21', null, '1'), ('290', '23', '8.1', '22', null, '1'), ('291', '23', '9.3', '23', null, '1'), ('292', '23', '8.2', '25', null, '1'), ('293', '23', '9.3.1', '26', null, '1'), ('294', '31', '长期借用', '7', null, '0'), ('295', '23', '8.4', '27', null, '1'), ('296', '23', '8.1.3', '28', null, '1'), ('300', '23', '10.3.1', '30', null, '1'), ('301', '23', '10.2.1', '31', null, '1'), ('302', '40', 'Gradle-3.3', '23', 'GRADLE', '1'), ('303', '21', 'EDU', '4', null, '0'), ('304', '5', '服务端', '7', null, '1'), ('305', '4', '测试完成', '4', null, '1'), ('306', '40', 'Gradle-4.1', '24', 'GRADLE', '1'), ('307', '5', '数据', '8', null, '1'), ('308', '24', 'IssueInterval', '3600000', '', '1'), ('309', '26', 'RedisAddress', '1', '10.69.58.195', '1'), ('310', '26', 'RedisPort', '1', '8803', '1'), ('311', '24', 'IssueVersionlimited', '5', '问题统计版本限制', '1'), ('312', '26', 'AgentTimeOutMileSec', '7200000', 'Agent超时时间单位毫秒', '1'), ('313', '13', 'TaskFlow', '6', null, '1'), ('314', '13', 'FlowSection', '7', null, '1');
COMMIT;

-- ----------------------------
--  Table structure for `dictype`
-- ----------------------------
DROP TABLE IF EXISTS `dictype`;
CREATE TABLE `dictype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DicTypeName` varchar(50) NOT NULL,
  `DicTypeIsActive` tinyint(1) NOT NULL,
  `DicTypeValue` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `dictype`
-- ----------------------------
BEGIN;
INSERT INTO `dictype` VALUES ('1', 'TaskStatus', '1', '1'), ('2', 'ProjectType', '1', '2'), ('3', 'ProjectName', '1', '3'), ('4', 'TestSubmitionStatus', '1', '4'), ('5', 'Platform', '1', '5'), ('6', 'JenkinsServer', '1', '6'), ('7', 'EmailConfig', '1', '7'), ('8', 'BuildStatus', '1', '8'), ('9', 'JobType', '1', '9'), ('10', 'JobStatus', '1', '10'), ('11', 'SCMInfo', '1', '11'), ('12', 'AutoTaskRuntime', '1', '12'), ('13', 'TaskType', '1', '13'), ('14', 'AgentOSType', '1', '14'), ('15', 'AutoAgentStatus', '1', '15'), ('16', 'ControllerTimeout', '1', '16'), ('17', 'TaskInQueueStatus', '1', '17'), ('18', 'AutoAgentExecDriver', '1', '18'), ('19', 'TQCommandType', '1', '19'), ('20', 'AutoCaseStatus', '1', '20'), ('21', 'TestEnv', '1', '21'), ('22', 'AndroidVersion', '1', '22'), ('23', 'IOSVersion', '1', '23'), ('24', 'ControllerGlobalConfig', '1', '24'), ('25', 'MobileDeviceStatus', '1', '25'), ('26', 'AgentGlobalConfig', '1', '26'), ('27', 'AuthPermissionType', '1', '27'), ('28', 'DeviceOS', '1', '28'), ('29', 'WPVersion', '1', '29'), ('30', 'ScreenSize', '1', '30'), ('31', 'DeviceType', '1', '31'), ('32', 'DeviceStatus', '1', '32'), ('33', 'NoProject', '1', '33'), ('34', 'TagType', '1', '34'), ('35', 'CICredentialType', '1', '35'), ('36', 'ActionLogType', '1', '36'), ('37', 'CIUploadFileLimit', '1', '37'), ('38', 'GitCheckOutStrategy', '1', '38'), ('39', 'SvnCheckOutStrategy', '1', '39'), ('40', 'BuildTools', '1', '40');
COMMIT;

-- ----------------------------
--  Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_content_type_id_fe83c5c1338e4b7_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_406fefeb411c6376_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_406fefeb411c6376_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_content_type_id_fe83c5c1338e4b7_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_44ce737007467da7_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `django_content_type`
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry'), ('44', 'administrate', 'device'), ('45', 'administrate', 'devicemanagementhistory'), ('3', 'auth', 'group'), ('2', 'auth', 'permission'), ('4', 'auth', 'user'), ('52', 'authtoken', 'token'), ('9', 'automationtesting', 'autoagent'), ('12', 'automationtesting', 'autocaseresult'), ('10', 'automationtesting', 'automobiledevice'), ('11', 'automationtesting', 'autorunresult'), ('13', 'automationtesting', 'autoservicehost'), ('7', 'automationtesting', 'autotask'), ('14', 'automationtesting', 'autotaskqueue'), ('8', 'automationtesting', 'autotestconfig'), ('16', 'automationtesting', 'dicdata'), ('15', 'automationtesting', 'dictype'), ('75', 'ci', 'autocase'), ('73', 'ci', 'autocaseresult'), ('79', 'ci', 'autotestingtaskresult'), ('58', 'ci', 'casetag'), ('65', 'ci', 'cicredentials'), ('66', 'ci', 'cideployservice'), ('67', 'ci', 'ciserver'), ('63', 'ci', 'citask'), ('68', 'ci', 'citaskflow'), ('74', 'ci', 'citaskflowhistory'), ('72', 'ci', 'citaskflowsection'), ('80', 'ci', 'citaskhistory'), ('77', 'ci', 'citaskplugin'), ('76', 'ci', 'servicehost'), ('78', 'ci', 'unittestcaseresult'), ('5', 'contenttypes', 'contenttype'), ('53', 'corsheaders', 'corsmodel'), ('69', 'env', 'mockapi'), ('70', 'env', 'mockhandler'), ('71', 'env', 'mockresponse'), ('54', 'home', 'agent'), ('27', 'home', 'dicdata'), ('26', 'home', 'dictype'), ('55', 'home', 'errormessage'), ('41', 'home', 'fileinfo'), ('59', 'home', 'taskqueue'), ('25', 'home', 'webapps'), ('24', 'productquality', 'bugfreemapping'), ('64', 'project', 'issueactivity'), ('81', 'project', 'issuefilter'), ('40', 'project', 'product'), ('35', 'project', 'project'), ('85', 'project', 'projectarchive'), ('89', 'project', 'projectcodeurl'), ('62', 'project', 'projectissue'), ('86', 'project', 'projectissuecategory'), ('84', 'project', 'projectissuedailystatistics'), ('82', 'project', 'projectissueresolvedresult'), ('92', 'project', 'projectissueseverity'), ('83', 'project', 'projectissuestatus'), ('90', 'project', 'projectissueversionstatistics'), ('34', 'project', 'projectmember'), ('56', 'project', 'projectmodule'), ('88', 'project', 'projectos'), ('87', 'project', 'projectosversion'), ('91', 'project', 'projectphase'), ('37', 'project', 'projectrole'), ('36', 'project', 'tag'), ('28', 'project', 'task'), ('61', 'project', 'testapplication'), ('29', 'project', 'version'), ('33', 'project', 'webhook'), ('6', 'sessions', 'session'), ('21', 'testjob', 'codecommitlog'), ('23', 'testjob', 'projectversion'), ('19', 'testjob', 'testbuildhistory'), ('17', 'testjob', 'testjob'), ('20', 'testjob', 'testjobhistory'), ('22', 'testjob', 'testproject'), ('18', 'testjob', 'testprojectsubmition'), ('39', 'user', 'actionlog'), ('51', 'user', 'usergroups'), ('38', 'user', 'user_extend'), ('42', 'user', 'user_group_extend'), ('43', 'user', 'user_permission_extend');
COMMIT;

-- ----------------------------
--  Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `django_migrations`
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2015-12-03 07:57:34'), ('2', 'auth', '0001_initial', '2015-12-03 07:57:39'), ('3', 'admin', '0001_initial', '2015-12-03 07:57:40'), ('4', 'contenttypes', '0002_remove_content_type_name', '2015-12-03 07:57:41'), ('5', 'auth', '0002_alter_permission_name_max_length', '2015-12-03 07:57:41'), ('6', 'auth', '0003_alter_user_email_max_length', '2015-12-03 07:57:42'), ('7', 'auth', '0004_alter_user_username_opts', '2015-12-03 07:57:42'), ('8', 'auth', '0005_alter_user_last_login_null', '2015-12-03 07:57:42'), ('9', 'auth', '0006_require_contenttypes_0002', '2015-12-03 07:57:42'), ('10', 'auth', '0007_user_profiles', '2015-12-03 07:57:43'), ('11', 'auth', '0008_delete_user_profiles', '2015-12-03 07:57:43'), ('12', 'sessions', '0001_initial', '2015-12-03 07:57:43'), ('13', 'admin', '0002_logentry_remove_auto_add', '2016-03-28 06:32:59'), ('14', 'administrate', '0001_initial', '2016-03-28 06:33:00'), ('15', 'auth', '0007_alter_validators_add_error_messages', '2016-03-28 06:33:00'), ('16', 'administrate', '0002_auto_20160328_1434', '2016-03-28 06:35:08'), ('17', 'administrate', '0002_auto_20160330_1107', '2016-05-31 08:56:29'), ('18', 'administrate', '0003_merge', '2016-05-31 08:56:29'), ('19', 'auth', '0008_alter_user_username_max_length', '2017-06-09 08:05:08'), ('20', 'authtoken', '0001_initial', '2017-06-09 08:05:08'), ('21', 'authtoken', '0002_auto_20160226_1747', '2017-06-09 08:05:08'), ('22', 'project', '0001_initial', '2017-06-09 08:19:03'), ('23', 'user', '0001_initial', '2017-06-09 08:28:24'), ('24', 'home', '0001_initial', '2017-06-09 08:35:51'), ('25', 'ci', '0001_initial', '2017-07-12 05:39:49'), ('28', 'env', '0001_initial', '2018-08-06 01:56:06');
COMMIT;

-- ----------------------------
--  Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



-- ----------------------------
--  Table structure for `error_message`
-- ----------------------------
DROP TABLE IF EXISTS `error_message`;
CREATE TABLE `error_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ErrorType` int(11) NOT NULL,
  `ErrorCode` int(11) NOT NULL,
  `ErrorName` varchar(25) DEFAULT NULL,
  `ErrorMessage` varchar(100) DEFAULT NULL,
  `IsActive` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `file_info`
-- ----------------------------
DROP TABLE IF EXISTS `file_info`;
CREATE TABLE `file_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `FileName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `FileUUID` varchar(50) DEFAULT NULL,
  `FilePath` varchar(500) DEFAULT NULL,
  `FileType` int(11) NOT NULL,
  `FileFolder` int(11) NOT NULL,
  `FileSuffixes` varchar(10) DEFAULT NULL,
  `FileCreator` int(11) NOT NULL,
  `FileSize` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9309 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `home_webapps`
-- ----------------------------
DROP TABLE IF EXISTS `home_webapps`;
CREATE TABLE `home_webapps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `app_title` varchar(50) NOT NULL,
  `app_key` varchar(10) NOT NULL,
  `app_url` varchar(500) NOT NULL,
  `app_avatar` varchar(255) DEFAULT NULL,
  `app_desc` varchar(500) DEFAULT NULL,
  `app_visable_level` int(11) NOT NULL,
  `app_creator` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `interface_mock_api`
-- ----------------------------
DROP TABLE IF EXISTS `interface_mock_api`;
CREATE TABLE `interface_mock_api` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `ApiTitle` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `ApiType` int(11) NOT NULL,
  `ApiPath` varchar(1000) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `HttpMethod` int(11) DEFAULT NULL,
  `CallBackUrl` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `CallBackMethod` int(11) DEFAULT NULL,
  `MockHandler` int(11) DEFAULT NULL,
  `MockResponse` int(11) DEFAULT NULL,
  `MockServer` int(11) DEFAULT NULL,
  `MatchParten` varchar(20) DEFAULT NULL,
  `Enable` tinyint(1) DEFAULT NULL,
  `Parent` int(11) DEFAULT NULL,
  `Description` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `interface_mock_handler`
-- ----------------------------
DROP TABLE IF EXISTS `interface_mock_handler`;
CREATE TABLE `interface_mock_handler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `HandlerName` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `HandlerFile` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `HandlerFileName` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Description` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `interface_mock_response`
-- ----------------------------
DROP TABLE IF EXISTS `interface_mock_response`;
CREATE TABLE `interface_mock_response` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `ApiID` int(11) NOT NULL,
  `Response` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Enable` tinyint(1) NOT NULL,
  `Description` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `CallBackMethod` int(11) DEFAULT NULL,
  `CallBackUrl` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `issue_activity`
-- ----------------------------
DROP TABLE IF EXISTS `issue_activity`;
CREATE TABLE `issue_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Issue` int(11) NOT NULL,
  `OldValue` varchar(2500) COLLATE utf8_bin DEFAULT NULL,
  `NewValue` varchar(2500) COLLATE utf8_bin DEFAULT NULL,
  `FieldName` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `FieldDesc` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `ActionType` int(11) NOT NULL,
  `Creator` int(11) NOT NULL,
  `Message` varchar(2500) COLLATE utf8_bin DEFAULT NULL,
  `ActionFlag` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2912 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



-- ----------------------------
--  Table structure for `issue_daily_statistics`
-- ----------------------------
DROP TABLE IF EXISTS `issue_daily_statistics`;
CREATE TABLE `issue_daily_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  `StatisticsDate` date NOT NULL,
  `OpenedTotal` int(11) NOT NULL,
  `ClosedTotal` int(11) NOT NULL,
  `FixedTotal` int(11) NOT NULL,
  `OpenedToday` int(11) NOT NULL,
  `FixedToday` int(11) NOT NULL,
  `ReopenedToday` int(11) NOT NULL,
  `VersionID` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4462 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `issue_filter`
-- ----------------------------
DROP TABLE IF EXISTS `issue_filter`;
CREATE TABLE `issue_filter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Project` int(11) NOT NULL,
  `Creator` int(11) NOT NULL,
  `Scope` int(11) NOT NULL,
  `FilterString` varchar(500) COLLATE utf8_bin DEFAULT NULL,
  `FilterUIConfig` varchar(500) COLLATE utf8_bin DEFAULT NULL,
  `FilterName` varchar(50) COLLATE utf8_bin NOT NULL,
  `FilterCacheString` varchar(500) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



-- ----------------------------
--  Table structure for `issue_version_statistics`
-- ----------------------------
DROP TABLE IF EXISTS `issue_version_statistics`;
CREATE TABLE `issue_version_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  `StatisticsDate` date NOT NULL,
  `IssueTotal` int(11) NOT NULL,
  `DimensionValue` int(11) NOT NULL,
  `VersionID` int(11) NOT NULL,
  `Dimension` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2612 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `logcat_logger`
-- ----------------------------
DROP TABLE IF EXISTS `logcat_logger`;
CREATE TABLE `logcat_logger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `deviceName` varchar(255) DEFAULT NULL,
  `regTime` datetime(6) NOT NULL,
  `deviceId` varchar(100) NOT NULL,
  `extra` varchar(255) DEFAULT NULL,
  `logFiles` varchar(50) DEFAULT NULL,
  `appId` int(11) DEFAULT NULL,
  `userAgent` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8;



-- ----------------------------
--  Table structure for `product`
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `PTitle` varchar(100) NOT NULL,
  `PKey` varchar(10) NOT NULL,
  `PDescription` varchar(255) DEFAULT NULL,
  `PVisiableLevel` int(11) NOT NULL,
  `LabelColor` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Records of `product`
-- ----------------------------
BEGIN;
INSERT INTO `product` VALUES ('1', '2017-06-13 10:08:53.000000', '1', 'Teamcat', 'Teamcat', 'Teamcat', '1', null);
COMMIT;


-- ----------------------------
--  Table structure for `project`
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `PBTitle` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `PBKey` varchar(10) NOT NULL,
  `PBDescription` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `PBVisiableLevel` int(11) NOT NULL,
  `PBPlatform` int(11) NOT NULL,
  `PBHttpUrl` varchar(255) DEFAULT NULL,
  `PBLead` int(11) NOT NULL,
  `PBAvatar` varchar(255) DEFAULT NULL,
  `Product` int(11) NOT NULL,
  `PBCreator` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `project_archive`
-- ----------------------------
DROP TABLE IF EXISTS `project_archive`;
CREATE TABLE `project_archive` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `VersionID` int(11) DEFAULT NULL,
  `ProjectID` int(11) NOT NULL,
  `HistoryID` int(11) NOT NULL,
  `Archives` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `project_code_url`
-- ----------------------------
DROP TABLE IF EXISTS `project_code_url`;
CREATE TABLE `project_code_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ApplicationID` int(11) NOT NULL,
  `CodeRepertory` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Branch` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=272 DEFAULT CHARSET=latin1;






-- ----------------------------
--  Table structure for `project_issue`
-- ----------------------------
DROP TABLE IF EXISTS `project_issue`;
CREATE TABLE `project_issue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Project` int(11) NOT NULL,
  `Version` int(11) NOT NULL,
  `Status` int(11) NOT NULL,
  `Processor` int(11) NOT NULL,
  `Creator` int(11) NOT NULL,
  `Severity` int(11) NOT NULL,
  `Solution` int(11) NOT NULL,
  `Title` varchar(500) COLLATE utf8_bin NOT NULL,
  `Desc` varchar(2000) COLLATE utf8_bin DEFAULT NULL,
  `Module` int(11) NOT NULL,
  `ProjectPhase` int(11) NOT NULL,
  `IssueCategory` int(11) NOT NULL,
  `DeviceOS` int(11) DEFAULT NULL,
  `OSVersion` int(11) DEFAULT NULL,
  `Attachments` varchar(500) COLLATE utf8_bin DEFAULT NULL,
  `ResolvedTime` datetime(6) DEFAULT NULL,
  `ClosedTime` datetime(6) DEFAULT NULL,
  `ReopenCounts` int(11) DEFAULT NULL,
  `UpdateTime` datetime(6) DEFAULT NULL,
  `Solver` int(11) DEFAULT NULL,
  `Team` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=657 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



-- ----------------------------
--  Table structure for `project_issue_category`
-- ----------------------------
DROP TABLE IF EXISTS `project_issue_category`;
CREATE TABLE `project_issue_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `IsActive` bit(1) DEFAULT NULL,
  `Project` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_issue_category`
-- ----------------------------
BEGIN;
INSERT INTO `project_issue_category` VALUES ('1', '1', null, '功能', b'1', '0'), ('2', '2', null, '性能', b'1', '0'), ('3', '3', null, 'UI', b'1', '0'), ('4', '4', null, '兼容性', b'1', '0'), ('5', '5', null, '服务端兼容性', b'1', '0'), ('6', '6', null, '服务端功能', b'1', '0'), ('7', '7', null, '修复问题引发', b'1', '0');
COMMIT;

-- ----------------------------
--  Table structure for `project_issue_resolved_result`
-- ----------------------------
DROP TABLE IF EXISTS `project_issue_resolved_result`;
CREATE TABLE `project_issue_resolved_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `IsActive` bit(1) DEFAULT NULL,
  `Project` int(11) NOT NULL,
  `LabelStyle` varchar(50) DEFAULT NULL,
  `Label` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_issue_resolved_result`
-- ----------------------------
BEGIN;
INSERT INTO `project_issue_resolved_result` VALUES ('1', '1', null, '未修复', b'1', '0', 'issue-severity-fatal', 'fa-minus-square-o'), ('2', '2', null, '修复', b'1', '0', 'issue-status-check', 'fa-gavel'), ('3', '3', null, '延迟修复', b'1', '0', 'issue-severity-critical', 'fa-bomb'), ('4', '4', null, '不修复', b'1', '0', 'issue-severity-fatal', 'fa-bolt'), ('5', '5', null, '重复', b'1', '0', 'issue-status-reopen', 'fa-crosshairs'), ('6', '6', null, 'Not a Bug', b'1', '0', 'issue-severity-major', 'fa-tint'), ('7', '7', null, 'By Desgin', b'1', '0', 'issue-severity-minor', 'fa-ban'), ('8', '8', null, '无法复现', b'1', '0', 'issue-severity-minor', 'fa-ban');
COMMIT;

-- ----------------------------
--  Table structure for `project_issue_severity`
-- ----------------------------
DROP TABLE IF EXISTS `project_issue_severity`;
CREATE TABLE `project_issue_severity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `IsActive` bit(1) DEFAULT NULL,
  `Project` int(11) NOT NULL,
  `LabelStyle` varchar(50) DEFAULT NULL,
  `Label` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_issue_severity`
-- ----------------------------
BEGIN;
INSERT INTO `project_issue_severity` VALUES ('1', '1', null, 'Fatal', b'1', '0', 'issue-severity-fatal', 'fa-circle'), ('2', '2', null, 'Critical', b'1', '0', 'issue-severity-critical', 'fa-circle'), ('3', '3', null, 'Major', b'1', '0', 'issue-severity-major', 'fa-circle'), ('4', '4', null, 'Minor', b'1', '0', 'issue-severity-minor', 'fa-circle');
COMMIT;

-- ----------------------------
--  Table structure for `project_issue_status`
-- ----------------------------
DROP TABLE IF EXISTS `project_issue_status`;
CREATE TABLE `project_issue_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `IsActive` bit(1) DEFAULT NULL,
  `Project` int(11) NOT NULL,
  `LabelStyle` varchar(50) DEFAULT NULL,
  `Label` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_issue_status`
-- ----------------------------
BEGIN;
INSERT INTO `project_issue_status` VALUES ('1', '1', 'created', '待提交', b'1', '0', 'issue-status-fresh', 'fa-sun-o'), ('2', '2', 'opened', '新建', b'1', '0', 'issue-status-new', 'fa-file'), ('3', '3', 'closed', '已关闭', b'1', '0', 'issue-status-closed', 'fa-minus-square-o'), ('4', '4', 'fixed', '已解决', b'1', '0', 'issue-status-resolved', 'fa-check'), ('5', '5', 'reopened', '重新打开', b'1', '0', 'issue-status-reopen', 'fa-retweet');
COMMIT;

-- ----------------------------
--  Table structure for `project_member`
-- ----------------------------
DROP TABLE IF EXISTS `project_member`;
CREATE TABLE `project_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `PMProjectID` int(11) NOT NULL,
  `PMRoleID` int(11) NOT NULL,
  `PMRoleType` int(11) NOT NULL,
  `PMMember` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=774 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `project_module`
-- ----------------------------
DROP TABLE IF EXISTS `project_module`;
CREATE TABLE `project_module` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Description` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `CreationTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `IsActive` bit(1) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=175 DEFAULT CHARSET=utf8;



-- ----------------------------
--  Table structure for `project_os`
-- ----------------------------
DROP TABLE IF EXISTS `project_os`;
CREATE TABLE `project_os` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `IsActive` bit(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_os`
-- ----------------------------
BEGIN;
INSERT INTO `project_os` VALUES ('1', '1', null, '无', b'1'), ('2', '2', null, 'IOS', b'1'), ('5', '5', null, 'Windows', b'1'), ('6', '6', null, 'MacOS', b'1'), ('7', '7', null, 'Linux', b'1'), ('8', '8', null, 'Android', b'1');
COMMIT;

-- ----------------------------
--  Table structure for `project_os_version`
-- ----------------------------
DROP TABLE IF EXISTS `project_os_version`;
CREATE TABLE `project_os_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `IsActive` bit(1) NOT NULL,
  `OS` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_os_version`
-- ----------------------------
BEGIN;
INSERT INTO `project_os_version` VALUES ('1', '1', null, '4.4', b'1', '8'), ('2', '2', null, '5.0', b'1', '8'), ('3', '3', null, '6.0', b'1', '8'), ('4', '4', null, '7.0', b'1', '8'), ('5', '5', null, '8.0', b'1', '8'), ('6', '1', '', '8.0', b'1', '2'), ('7', '2', '', '9.0', b'1', '2'), ('8', '3', '', '10.0', b'1', '2'), ('9', '4', '', '11.0', b'1', '2'), ('10', '5', '', '11.0.3', b'1', '2'), ('11', '1', null, '无', b'1', '1');
COMMIT;

-- ----------------------------
--  Table structure for `project_phase`
-- ----------------------------
DROP TABLE IF EXISTS `project_phase`;
CREATE TABLE `project_phase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `IsActive` bit(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_phase`
-- ----------------------------
BEGIN;
INSERT INTO `project_phase` VALUES ('1', '1', null, '需求分析', b'1'), ('2', '2', null, '需求评审', b'1'), ('3', '3', null, '设计研发', b'1'), ('4', '4', null, '提测前验证', b'1'), ('5', '5', null, '测试阶段', b'1'), ('6', '6', null, '预上线', b'1'), ('7', '7', null, '线上阶段', b'1');
COMMIT;

-- ----------------------------
--  Table structure for `project_role`
-- ----------------------------
DROP TABLE IF EXISTS `project_role`;
CREATE TABLE `project_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `PRName` varchar(20) NOT NULL,
  `PRColor` varchar(50) DEFAULT NULL,
  `PRAuthGroup` int(11) NOT NULL,
  `PRRoleDesc` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_role`
-- ----------------------------
BEGIN;
INSERT INTO `project_role` VALUES ('1', '2015-11-18 15:57:52', '1', 'User', 'green', '0', null), ('2', '2015-11-18 15:58:34', '1', 'Tester', 'red', '0', null), ('3', '2015-12-03 15:58:51', '1', 'Dev', 'orange', '0', null), ('4', '2015-11-18 15:59:20', '1', 'Admin', '#426ab3', '0', null), ('5', '2015-11-18 16:00:09', '1', 'Owner', '#7fb80e', '0', null);
COMMIT;

-- ----------------------------
--  Table structure for `project_tag`
-- ----------------------------
DROP TABLE IF EXISTS `project_tag`;
CREATE TABLE `project_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `TagName` varchar(20) NOT NULL,
  `TagProjectID` int(11) NOT NULL,
  `TagColor` varchar(50) DEFAULT NULL,
  `TagAvatar` varchar(255) DEFAULT NULL,
  `TagVisableLevel` int(11) NOT NULL,
  `TagOwner` int(11) NOT NULL,
  `TagType` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_tag`
-- ----------------------------
BEGIN;
INSERT INTO `project_tag` VALUES ('1', '2015-11-13 16:51:49', '1', ' 安卓', '0', '#32be77', null, '1', '2', '1'), ('2', '2015-11-13 16:53:33', '1', 'IOS', '0', 'red', null, '1', '2', '1'), ('3', '2015-11-13 16:54:02', '1', '功能', '0', 'blue', null, '1', '2', '1'), ('4', '2015-11-13 16:54:38', '1', 'WP', '0', '#426ab3', null, '1', '2', '1'), ('5', '2015-11-13 17:02:10', '1', '接口', '0', '#426ab3', null, '1', '2', '1'), ('6', '2015-11-13 17:02:32', '1', '长期', '0', 'orange', null, '1', '2', '1'), ('7', '2015-11-13 17:03:08', '1', '开发', '0', '#7fb80e', null, '1', '2', '1'), ('8', '2016-07-25 17:13:01', '1', '构建', '0', '#32be77', null, '1', '2', '1'), ('9', '2016-07-25 17:14:33', '1', '部署', '0', '#6a6da9', null, '1', '2', '1'), ('10', '2016-07-25 17:15:24', '0', '测试', '0', '#00ae9d', null, '1', '2', '1'), ('11', '2016-07-27 10:23:43', '1', 'Android', '0', '#1d953f', null, '1', '2', '3'), ('12', '2016-07-27 10:24:42', '1', 'IOS', '0', '#fdb933', null, '1', '2', '3'), ('13', '2016-11-24 17:40:35', '1', 'Release', '0', '#f05b72', null, '1', '2', '2'), ('14', '2016-11-24 17:48:53', '1', 'Test Complete', '0', '#f391a9', null, '1', '2', '2'), ('15', '2016-11-24 17:50:28', '1', 'Mile Stone', '0', '#d93a49', null, '1', '2', '2'), ('16', '2016-12-07 11:17:33', '1', 'VED_Build', '0', '#007947', null, '1', '2', '3'), ('17', '2016-12-15 17:17:51', '1', 'Daily Build', '0', '#faa755', null, '1', '2', '1'), ('26', '2018-06-14 16:35:45', '1', 'ADCat', '0', '#faa755', null, '1', '2', '3'), ('27', '2018-07-18 10:12:29', '1', 'MockAgent', '0', '#458B74', null, '1', '2', '3');
COMMIT;

-- ----------------------------
--  Table structure for `project_task`
-- ----------------------------
DROP TABLE IF EXISTS `project_task`;
CREATE TABLE `project_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  `Title` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `DeadLine` date DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `FinishedDate` date DEFAULT NULL,
  `WorkHours` int(11) NOT NULL,
  `Owner` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Creator` int(11) NOT NULL,
  `Progress` int(11) NOT NULL,
  `Description` varchar(1000) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Tags` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Status` int(11) NOT NULL,
  `Parent` int(11) unsigned DEFAULT NULL,
  `Priority` int(11) NOT NULL DEFAULT '1',
  `Version` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=190 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `project_test_application`
-- ----------------------------
DROP TABLE IF EXISTS `project_test_application`;
CREATE TABLE `project_test_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  `VersionID` int(11) NOT NULL,
  `Commitor` int(11) NOT NULL,
  `TestingFeature` varchar(2000) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `TestingAdvice` varchar(2000) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `CommitTime` datetime(6) DEFAULT NULL,
  `Status` int(11) NOT NULL,
  `EmailNotificationStatus` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT '0,0,0,0,0' COMMENT '邮件发送状态',
  `ProjectModuleID` int(11) DEFAULT '0',
  `ProjectCode` int(11) DEFAULT '0',
  `Attachment` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Testers` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT '',
  `ExpectCommitDate` datetime(6) DEFAULT NULL,
  `TestingDeadLineDate` datetime(6) DEFAULT NULL,
  `TestingFinishedDate` datetime(6) DEFAULT NULL,
  `Creator` int(11) NOT NULL DEFAULT '0',
  `TestingStartDate` datetime(6) DEFAULT NULL,
  `Topic` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=415 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `project_version`
-- ----------------------------
DROP TABLE IF EXISTS `project_version`;
CREATE TABLE `project_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `VProjectID` int(11) NOT NULL,
  `VVersion` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `VStartDate` date DEFAULT NULL,
  `VReleaseDate` date DEFAULT NULL,
  `VDescription` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=307 DEFAULT CHARSET=latin1;


-- ----------------------------
--  Table structure for `project_webhook`
-- ----------------------------
DROP TABLE IF EXISTS `project_webhook`;
CREATE TABLE `project_webhook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `WHProjectID` int(11) NOT NULL,
  `WHURL` varchar(500) NOT NULL,
  `WHParameters` varchar(500) DEFAULT NULL,
  `WHLabel` varchar(50) DEFAULT NULL,
  `WHIsDefault` tinyint(1) NOT NULL,
  `WHCatagory` int(11) NOT NULL,
  `WHCreator` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `task_queue`
-- ----------------------------
DROP TABLE IF EXISTS `task_queue`;
CREATE TABLE `task_queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `TaskID` int(11) NOT NULL,
  `TaskType` int(1) DEFAULT NULL,
  `Status` int(11) NOT NULL,
  `CaseList` varchar(10000) DEFAULT NULL,
  `EnqueueTime` datetime(6) NOT NULL,
  `RerunReportID` int(11) DEFAULT NULL,
  `RuntimeEnv` int(11) DEFAULT NULL,
  `TaskUUID` varchar(128) NOT NULL,
  `AgentID` int(11) DEFAULT NULL,
  `StartTime` datetime(6) DEFAULT NULL,
  `TaskEndTime` datetime(6) DEFAULT NULL,
  `FromName` varchar(100) DEFAULT NULL,
  `FromIP` varchar(20) DEFAULT NULL,
  `HasChild` tinyint(1) DEFAULT NULL,
  `Command` int(11) NOT NULL,
  `MobileDeviceId` int(11) DEFAULT NULL,
  `IsLocked` tinyint(1) unsigned zerofill NOT NULL,
  `LockTime` datetime(6) DEFAULT NULL,
  `DistributeTimes` int(11) DEFAULT NULL,
  `ErrorMsg` varchar(500) DEFAULT NULL,
  `Priority` int(1) NOT NULL,
  `BuildParameterID` varchar(30) DEFAULT NULL,
  `ParentID` int(11) unsigned zerofill DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7345 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- ----------------------------
--  Table structure for `team`
-- ----------------------------
DROP TABLE IF EXISTS `team`;
CREATE TABLE `team` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `team`
-- ----------------------------
BEGIN;
INSERT INTO `team` VALUES ('1', '2018-05-16 17:15:25.000000', '1', 'Android', null), ('2', '2018-05-16 17:15:32.000000', '1', 'IOS', null), ('3', '2018-05-16 17:15:49.000000', '1', '前端', null), ('4', '2018-05-16 17:16:05.000000', '1', '服务端', null), ('5', '2018-05-16 17:16:18.000000', '1', 'PM', null);
COMMIT;

-- ----------------------------
--  Table structure for `unittest_case_result`
-- ----------------------------
DROP TABLE IF EXISTS `unittest_case_result`;
CREATE TABLE `unittest_case_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `TestCaseName` varchar(100) DEFAULT NULL,
  `TaskResultID` int(11) NOT NULL,
  `StartTime` datetime(6) DEFAULT NULL,
  `EndTime` datetime(6) DEFAULT NULL,
  `Result` int(11) NOT NULL,
  `Error` varchar(1000) DEFAULT NULL,
  `StackTrace` varchar(5000) DEFAULT NULL,
  `BugID` int(11) NOT NULL,
  `FailCategoryID` int(11) NOT NULL,
  `ReRunID` int(11) NOT NULL,
  `FailType` int(11) NOT NULL,
  `FailNote` varchar(255) DEFAULT NULL,
  `CaseVersion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `user_action_log`
-- ----------------------------
DROP TABLE IF EXISTS `user_action_log`;
CREATE TABLE `user_action_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ActionTime` datetime(6) NOT NULL,
  `User` int(11) NOT NULL,
  `ContentType` int(11) NOT NULL,
  `ObjectID` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `ObjectRepr` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `ActionFlag` smallint(5) unsigned NOT NULL,
  `ChangeMessage` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `ActionType` int(11) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12015 DEFAULT CHARSET=latin1;


SET FOREIGN_KEY_CHECKS = 1;
