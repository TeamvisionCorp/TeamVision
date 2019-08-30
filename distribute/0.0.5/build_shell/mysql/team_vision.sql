/*
 Navicat MySQL Data Transfer

 Source Server         : 
 Source Server Type    : MySQL
 Source Server Version : 50619
 Source Host           : 
 Source Database       : team_vision

 Target Server Type    : MySQL
 Target Server Version : 50619
 File Encoding         : utf-8

 Date: 08/05/2019 17:05:51 PM
*/

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
  `AgentWorkSpace` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `AgentTags` varchar(255) NOT NULL,
  `AgentPort` int(11) NOT NULL,
  `Executors` int(11) NOT NULL,
  `RunningExecutors` int(11) NOT NULL,
  `BuildToolsDir` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;


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
  CONSTRAINT `auth_group_permission_group_id_33a12a5a8a5bcd3d_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group__permission_id_13acf6f62506d836_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=301 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_permission`
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry'), ('2', 'Can change log entry', '1', 'change_logentry'), ('3', 'Can delete log entry', '1', 'delete_logentry'), ('4', 'Can add permission', '2', 'add_permission'), ('5', 'Can change permission', '2', 'change_permission'), ('6', 'Can delete permission', '2', 'delete_permission'), ('7', 'Can add group', '3', 'add_group'), ('8', 'Can change group', '3', 'change_group'), ('9', 'Can delete group', '3', 'delete_group'), ('10', 'Can add user', '4', 'add_user'), ('11', 'Can change user', '4', 'change_user'), ('12', 'Can delete user', '4', 'delete_user'), ('13', 'Can add content type', '5', 'add_contenttype'), ('14', 'Can change content type', '5', 'change_contenttype'), ('15', 'Can delete content type', '5', 'delete_contenttype'), ('16', 'Can add session', '6', 'add_session'), ('17', 'Can change session', '6', 'change_session'), ('18', 'Can delete session', '6', 'delete_session'), ('19', 'Can add auto task', '7', 'add_autotask'), ('20', 'Can change auto task', '7', 'change_autotask'), ('21', 'Can delete auto task', '7', 'delete_autotask'), ('22', 'Can add auto test config', '8', 'add_autotestconfig'), ('23', 'Can change auto test config', '8', 'change_autotestconfig'), ('24', 'Can delete auto test config', '8', 'delete_autotestconfig'), ('25', 'Can add auto agent', '9', 'add_autoagent'), ('26', 'Can change auto agent', '9', 'change_autoagent'), ('27', 'Can delete auto agent', '9', 'delete_autoagent'), ('28', 'Can add auto mobile device', '10', 'add_automobiledevice'), ('29', 'Can change auto mobile device', '10', 'change_automobiledevice'), ('30', 'Can delete auto mobile device', '10', 'delete_automobiledevice'), ('31', 'Can add auto run result', '11', 'add_autorunresult'), ('32', 'Can change auto run result', '11', 'change_autorunresult'), ('33', 'Can delete auto run result', '11', 'delete_autorunresult'), ('34', 'Can add auto case result', '12', 'add_autocaseresult'), ('35', 'Can change auto case result', '12', 'change_autocaseresult'), ('36', 'Can delete auto case result', '12', 'delete_autocaseresult'), ('37', 'Can add auto service host', '13', 'add_autoservicehost'), ('38', 'Can change auto service host', '13', 'change_autoservicehost'), ('39', 'Can delete auto service host', '13', 'delete_autoservicehost'), ('40', 'Can add auto task queue', '14', 'add_autotaskqueue'), ('41', 'Can change auto task queue', '14', 'change_autotaskqueue'), ('42', 'Can delete auto task queue', '14', 'delete_autotaskqueue'), ('43', 'Can add dic type', '15', 'add_dictype'), ('44', 'Can change dic type', '15', 'change_dictype'), ('45', 'Can delete dic type', '15', 'delete_dictype'), ('46', 'Can add dic data', '16', 'add_dicdata'), ('47', 'Can change dic data', '16', 'change_dicdata'), ('48', 'Can delete dic data', '16', 'delete_dicdata'), ('49', 'Can add test job', '17', 'add_testjob'), ('50', 'Can change test job', '17', 'change_testjob'), ('51', 'Can delete test job', '17', 'delete_testjob'), ('52', 'Can add test project submition', '18', 'add_testprojectsubmition'), ('53', 'Can change test project submition', '18', 'change_testprojectsubmition'), ('54', 'Can delete test project submition', '18', 'delete_testprojectsubmition'), ('55', 'Can add test build history', '19', 'add_testbuildhistory'), ('56', 'Can change test build history', '19', 'change_testbuildhistory'), ('57', 'Can delete test build history', '19', 'delete_testbuildhistory'), ('58', 'Can add test job history', '20', 'add_testjobhistory'), ('59', 'Can change test job history', '20', 'change_testjobhistory'), ('60', 'Can delete test job history', '20', 'delete_testjobhistory'), ('61', 'Can add code commit log', '21', 'add_codecommitlog'), ('62', 'Can change code commit log', '21', 'change_codecommitlog'), ('63', 'Can delete code commit log', '21', 'delete_codecommitlog'), ('64', 'Can add test project', '22', 'add_testproject'), ('65', 'Can change test project', '22', 'change_testproject'), ('66', 'Can delete test project', '22', 'delete_testproject'), ('67', 'Can add project version', '23', 'add_projectversion'), ('68', 'Can change project version', '23', 'change_projectversion'), ('69', 'Can delete project version', '23', 'delete_projectversion'), ('70', 'Can add bug free mapping', '24', 'add_bugfreemapping'), ('71', 'Can change bug free mapping', '24', 'change_bugfreemapping'), ('72', 'Can delete bug free mapping', '24', 'delete_bugfreemapping'), ('73', 'Can add web apps', '25', 'add_webapps'), ('74', 'Can change web apps', '25', 'change_webapps'), ('75', 'Can delete web apps', '25', 'delete_webapps'), ('76', 'Can add dic type', '26', 'add_dictype'), ('77', 'Can change dic type', '26', 'change_dictype'), ('78', 'Can delete dic type', '26', 'delete_dictype'), ('79', 'Can add dic data', '27', 'add_dicdata'), ('80', 'Can change dic data', '27', 'change_dicdata'), ('81', 'Can delete dic data', '27', 'delete_dicdata'), ('82', 'Can add task', '28', 'add_task'), ('83', 'Can change task', '28', 'change_task'), ('84', 'Can delete task', '28', 'delete_task'), ('85', 'Can add version', '29', 'add_version'), ('86', 'Can change version', '29', 'change_version'), ('87', 'Can delete version', '29', 'delete_version'), ('97', 'Can add web hook', '33', 'add_webhook'), ('98', 'Can change web hook', '33', 'change_webhook'), ('99', 'Can delete web hook', '33', 'delete_webhook'), ('100', 'Can add project member', '34', 'add_projectmember'), ('101', 'Can change project member', '34', 'change_projectmember'), ('102', 'Can delete project member', '34', 'delete_projectmember'), ('103', 'Can add project', '35', 'add_project'), ('104', 'Can change project', '35', 'change_project'), ('105', 'Can delete project', '35', 'delete_project'), ('106', 'Can add tag', '36', 'add_tag'), ('107', 'Can change tag', '36', 'change_tag'), ('108', 'Can delete tag', '36', 'delete_tag'), ('109', 'Can add project role', '37', 'add_projectrole'), ('110', 'Can change project role', '37', 'change_projectrole'), ('111', 'Can delete project role', '37', 'delete_projectrole'), ('112', 'Can add user_ extend', '38', 'add_user_extend'), ('113', 'Can change user_ extend', '38', 'change_user_extend'), ('114', 'Can delete user_ extend', '38', 'delete_user_extend'), ('115', 'Can add action log', '39', 'add_actionlog'), ('116', 'Can change action log', '39', 'change_actionlog'), ('117', 'Can delete action log', '39', 'delete_actionlog'), ('118', 'Can add product', '40', 'add_product'), ('119', 'Can change product', '40', 'change_product'), ('120', 'Can delete product', '40', 'delete_product'), ('121', 'Can add file info', '41', 'add_fileinfo'), ('122', 'Can change file info', '41', 'change_fileinfo'), ('123', 'Can delete file info', '41', 'delete_fileinfo'), ('124', 'Can add user_ group_ extend', '42', 'add_user_group_extend'), ('125', 'Can change user_ group_ extend', '42', 'change_user_group_extend'), ('126', 'Can delete user_ group_ extend', '42', 'delete_user_group_extend'), ('127', 'Can add user_ permission_ extend', '43', 'add_user_permission_extend'), ('128', 'Can change user_ permission_ extend', '43', 'change_user_permission_extend'), ('129', 'Can delete user_ permission_ extend', '43', 'delete_user_permission_extend'), ('130', 'Can add device', '44', 'add_device'), ('131', 'Can change device', '44', 'change_device'), ('132', 'Can delete device', '44', 'delete_device'), ('133', 'Can add device management history', '45', 'add_devicemanagementhistory'), ('134', 'Can change device management history', '45', 'change_devicemanagementhistory'), ('135', 'Can delete device management history', '45', 'delete_devicemanagementhistory'), ('142', 'Can add user groups', '51', 'add_usergroups'), ('143', 'Can change user groups', '51', 'change_usergroups'), ('144', 'Can delete user groups', '51', 'delete_usergroups'), ('145', 'Can add Token', '52', 'add_token'), ('146', 'Can change Token', '52', 'change_token'), ('147', 'Can delete Token', '52', 'delete_token'), ('148', 'Can add cors model', '53', 'add_corsmodel'), ('149', 'Can change cors model', '53', 'change_corsmodel'), ('150', 'Can delete cors model', '53', 'delete_corsmodel'), ('151', 'Can add agent', '54', 'add_agent'), ('152', 'Can change agent', '54', 'change_agent'), ('153', 'Can delete agent', '54', 'delete_agent'), ('154', 'Can add error message', '55', 'add_errormessage'), ('155', 'Can change error message', '55', 'change_errormessage'), ('156', 'Can delete error message', '55', 'delete_errormessage'), ('157', 'Can add project module', '56', 'add_projectmodule'), ('158', 'Can change project module', '56', 'change_projectmodule'), ('159', 'Can delete project module', '56', 'delete_projectmodule'), ('163', 'Can add case tag', '58', 'add_casetag'), ('164', 'Can change case tag', '58', 'change_casetag'), ('165', 'Can delete case tag', '58', 'delete_casetag'), ('166', 'Can add task queue', '59', 'add_taskqueue'), ('167', 'Can change task queue', '59', 'change_taskqueue'), ('168', 'Can delete task queue', '59', 'delete_taskqueue'), ('172', 'Can add test application', '61', 'add_testapplication'), ('173', 'Can change test application', '61', 'change_testapplication'), ('174', 'Can delete test application', '61', 'delete_testapplication'), ('175', 'Can add project issue', '62', 'add_projectissue'), ('176', 'Can change project issue', '62', 'change_projectissue'), ('177', 'Can delete project issue', '62', 'delete_projectissue'), ('178', 'Can add mock api', '69', 'add_mockapi'), ('179', 'Can change mock api', '69', 'change_mockapi'), ('180', 'Can delete mock api', '69', 'delete_mockapi'), ('181', 'Can add mock handler', '70', 'add_mockhandler'), ('182', 'Can change mock handler', '70', 'change_mockhandler'), ('183', 'Can delete mock handler', '70', 'delete_mockhandler'), ('184', 'Can add mock response', '71', 'add_mockresponse'), ('185', 'Can change mock response', '71', 'change_mockresponse'), ('186', 'Can delete mock response', '71', 'delete_mockresponse'), ('187', 'Can add ci task flow section', '72', 'add_citaskflowsection'), ('188', 'Can change ci task flow section', '72', 'change_citaskflowsection'), ('189', 'Can delete ci task flow section', '72', 'delete_citaskflowsection'), ('190', 'Can add ci server', '67', 'add_ciserver'), ('191', 'Can change ci server', '67', 'change_ciserver'), ('192', 'Can delete ci server', '67', 'delete_ciserver'), ('193', 'Can add auto case result', '73', 'add_autocaseresult'), ('194', 'Can change auto case result', '73', 'change_autocaseresult'), ('195', 'Can delete auto case result', '73', 'delete_autocaseresult'), ('196', 'Can add ci task flow', '68', 'add_citaskflow'), ('197', 'Can change ci task flow', '68', 'change_citaskflow'), ('198', 'Can delete ci task flow', '68', 'delete_citaskflow'), ('199', 'Can add ci credentials', '65', 'add_cicredentials'), ('200', 'Can change ci credentials', '65', 'change_cicredentials'), ('201', 'Can delete ci credentials', '65', 'delete_cicredentials'), ('202', 'Can add ci task', '63', 'add_citask'), ('203', 'Can change ci task', '63', 'change_citask'), ('204', 'Can delete ci task', '63', 'delete_citask'), ('205', 'Can add ci task flow history', '74', 'add_citaskflowhistory'), ('206', 'Can change ci task flow history', '74', 'change_citaskflowhistory'), ('207', 'Can delete ci task flow history', '74', 'delete_citaskflowhistory'), ('208', 'Can add auto case', '75', 'add_autocase'), ('209', 'Can change auto case', '75', 'change_autocase'), ('210', 'Can delete auto case', '75', 'delete_autocase'), ('211', 'Can add service host', '76', 'add_servicehost'), ('212', 'Can change service host', '76', 'change_servicehost'), ('213', 'Can delete service host', '76', 'delete_servicehost'), ('214', 'Can add ci task plugin', '77', 'add_citaskplugin'), ('215', 'Can change ci task plugin', '77', 'change_citaskplugin'), ('216', 'Can delete ci task plugin', '77', 'delete_citaskplugin'), ('217', 'Can add unit test case result', '78', 'add_unittestcaseresult'), ('218', 'Can change unit test case result', '78', 'change_unittestcaseresult'), ('219', 'Can delete unit test case result', '78', 'delete_unittestcaseresult'), ('220', 'Can add ci deploy service', '66', 'add_cideployservice'), ('221', 'Can change ci deploy service', '66', 'change_cideployservice'), ('222', 'Can delete ci deploy service', '66', 'delete_cideployservice'), ('223', 'Can add auto testing task result', '79', 'add_autotestingtaskresult'), ('224', 'Can change auto testing task result', '79', 'change_autotestingtaskresult'), ('225', 'Can delete auto testing task result', '79', 'delete_autotestingtaskresult'), ('226', 'Can add ci task history', '80', 'add_citaskhistory'), ('227', 'Can change ci task history', '80', 'change_citaskhistory'), ('228', 'Can delete ci task history', '80', 'delete_citaskhistory'), ('229', 'Can add issue filter', '81', 'add_issuefilter'), ('230', 'Can change issue filter', '81', 'change_issuefilter'), ('231', 'Can delete issue filter', '81', 'delete_issuefilter'), ('232', 'Can add project issue resolved result', '82', 'add_projectissueresolvedresult'), ('233', 'Can change project issue resolved result', '82', 'change_projectissueresolvedresult'), ('234', 'Can delete project issue resolved result', '82', 'delete_projectissueresolvedresult'), ('235', 'Can add project issue status', '83', 'add_projectissuestatus'), ('236', 'Can change project issue status', '83', 'change_projectissuestatus'), ('237', 'Can delete project issue status', '83', 'delete_projectissuestatus'), ('238', 'Can add project issue daily statistics', '84', 'add_projectissuedailystatistics'), ('239', 'Can change project issue daily statistics', '84', 'change_projectissuedailystatistics'), ('240', 'Can delete project issue daily statistics', '84', 'delete_projectissuedailystatistics'), ('241', 'Can add project archive', '85', 'add_projectarchive'), ('242', 'Can change project archive', '85', 'change_projectarchive'), ('243', 'Can delete project archive', '85', 'delete_projectarchive'), ('244', 'Can add project issue category', '86', 'add_projectissuecategory'), ('245', 'Can change project issue category', '86', 'change_projectissuecategory'), ('246', 'Can delete project issue category', '86', 'delete_projectissuecategory'), ('247', 'Can add project os version', '87', 'add_projectosversion'), ('248', 'Can change project os version', '87', 'change_projectosversion'), ('249', 'Can delete project os version', '87', 'delete_projectosversion'), ('250', 'Can add project os', '88', 'add_projectos'), ('251', 'Can change project os', '88', 'change_projectos'), ('252', 'Can delete project os', '88', 'delete_projectos'), ('253', 'Can add project code url', '89', 'add_projectcodeurl'), ('254', 'Can change project code url', '89', 'change_projectcodeurl'), ('255', 'Can delete project code url', '89', 'delete_projectcodeurl'), ('256', 'Can add project issue version statistics', '90', 'add_projectissueversionstatistics'), ('257', 'Can change project issue version statistics', '90', 'change_projectissueversionstatistics'), ('258', 'Can delete project issue version statistics', '90', 'delete_projectissueversionstatistics'), ('259', 'Can add issue activity', '64', 'add_issueactivity'), ('260', 'Can change issue activity', '64', 'change_issueactivity'), ('261', 'Can delete issue activity', '64', 'delete_issueactivity'), ('262', 'Can add project phase', '91', 'add_projectphase'), ('263', 'Can change project phase', '91', 'change_projectphase'), ('264', 'Can delete project phase', '91', 'delete_projectphase'), ('265', 'Can add project issue severity', '92', 'add_projectissueseverity'), ('266', 'Can change project issue severity', '92', 'change_projectissueseverity'), ('267', 'Can delete project issue severity', '92', 'delete_projectissueseverity'), ('268', 'Can add mock api', '93', 'add_mockapi'), ('269', 'Can change mock api', '93', 'change_mockapi'), ('270', 'Can delete mock api', '93', 'delete_mockapi'), ('271', 'Can add mock handler', '94', 'add_mockhandler'), ('272', 'Can change mock handler', '94', 'change_mockhandler'), ('273', 'Can delete mock handler', '94', 'delete_mockhandler'), ('274', 'Can add mock response', '95', 'add_mockresponse'), ('275', 'Can change mock response', '95', 'change_mockresponse'), ('276', 'Can delete mock response', '95', 'delete_mockresponse'), ('277', 'Can add ci flow section history', '96', 'add_ciflowsectionhistory'), ('278', 'Can change ci flow section history', '96', 'change_ciflowsectionhistory'), ('279', 'Can delete ci flow section history', '96', 'delete_ciflowsectionhistory'), ('280', 'Can add project task dependency', '97', 'add_projecttaskdependency'), ('281', 'Can change project task dependency', '97', 'change_projecttaskdependency'), ('282', 'Can delete project task dependency', '97', 'delete_projecttaskdependency'), ('283', 'Can add project task owner', '98', 'add_projecttaskowner'), ('284', 'Can change project task owner', '98', 'change_projecttaskowner'), ('285', 'Can delete project task owner', '98', 'delete_projecttaskowner'), ('286', 'Can add project issue priority', '99', 'add_projectissuepriority'), ('287', 'Can change project issue priority', '99', 'change_projectissuepriority'), ('288', 'Can delete project issue priority', '99', 'delete_projectissuepriority'), ('289', 'Can add project document', '100', 'add_projectdocument'), ('290', 'Can change project document', '100', 'change_projectdocument'), ('291', 'Can delete project document', '100', 'delete_projectdocument'), ('292', 'Can add ci task api trigger', '101', 'add_citaskapitrigger'), ('293', 'Can change ci task api trigger', '101', 'change_citaskapitrigger'), ('294', 'Can delete ci task api trigger', '101', 'delete_citaskapitrigger'), ('295', 'Can add ci task stage history', '102', 'add_citaskstagehistory'), ('296', 'Can change ci task stage history', '102', 'change_citaskstagehistory'), ('297', 'Can delete ci task stage history', '102', 'delete_citaskstagehistory'), ('298', 'Can add ci task step output', '103', 'add_citaskstepoutput'), ('299', 'Can change ci task step output', '103', 'change_citaskstepoutput'), ('300', 'Can delete ci task step output', '103', 'delete_citaskstepoutput');
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
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_user`
-- ----------------------------
BEGIN;
INSERT INTO `auth_user` VALUES ('1', 'pbkdf2_sha256$100000$r5or5rIt7Whg$c+6efLZNgOZ4802kSnMgBSJSyOWmjlWjwnjf3A0K4WU=', '2019-07-29 05:36:08', '1', 'admin', '理员', '管', 'teamvision@teamvision.cn', '1', '1', '2014-10-16 09:42:16');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `auth_user_extend`
-- ----------------------------


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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `auth_user_groups`
-- ----------------------------
BEGIN;
INSERT INTO `auth_user_groups` VALUES ('1', '1', '27'), ('3', '2', '27'), ('4', '3', '29'), ('5', '4', '29'), ('6', '6', '29');
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
  CONSTRAINT `auth_user_user_permissi_user_id_46d89bc6ea1b4ae5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_u_permission_id_7543a650240f224d_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=2715 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `autotesting_case_result`
-- ----------------------------

-- ----------------------------
--  Table structure for `autotesting_task_result`
-- ----------------------------
DROP TABLE IF EXISTS `autotesting_task_result`;
CREATE TABLE `autotesting_task_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `StageHistoryID` int(11) DEFAULT NULL,
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
  `StepID` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;



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
) ENGINE=InnoDB AUTO_INCREMENT=311 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


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
INSERT INTO `case_tag` VALUES ('1', '2017-07-19 15:11:19', b'1', 'ALL', '全部'), ('2', '2017-07-19 14:48:44', b'1', 'P1', '环境检测'), ('3', '2017-07-19 14:49:08', b'1', 'P2', '业务主流程'), ('4', '2017-07-19 14:47:59', b'1', 'P3', 'BVT 测试');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  `LastRunTime` datetime(6) DEFAULT NULL,
  `Creator` int(11) NOT NULL,
  `Description` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `BuildVersion` int(11) NOT NULL,
  `HistoryCleanStrategy` int(11) NOT NULL,
  `LastHistory` int(11) DEFAULT '0',
  `Schedule` varchar(30) DEFAULT NULL,
  `ExecuteStrategy` int(11) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;



-- ----------------------------
--  Table structure for `ci_task_apitrigger`
-- ----------------------------
DROP TABLE IF EXISTS `ci_task_apitrigger`;
CREATE TABLE `ci_task_apitrigger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `TriggerName` varchar(100) DEFAULT NULL,
  `TriggerUUID` varchar(500) DEFAULT NULL,
  `TaskQueueUUID` varchar(100) NOT NULL,
  `TaskID` int(11) NOT NULL,
  `Branch` varchar(1000) DEFAULT NULL,
  `CodeAddress` varchar(1000) DEFAULT NULL,
  `CommitID` varchar(500) DEFAULT NULL,
  `BuildParameter` varchar(100) DEFAULT NULL,
  `ActionType` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;



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
  `Status` int(11) NOT NULL,
  `TaskUUID` varchar(255) DEFAULT NULL,
  `StartedBy` int(11) NOT NULL,
  `BuildVersion` int(11) NOT NULL,
  `ProjectVersion` int(11) NOT NULL,
  `BuildParameterID` varchar(30) DEFAULT NULL,
  `AgentID` int(11) DEFAULT NULL,
  `FlowSectionHistory` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;




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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `ci_task_plugin`
-- ----------------------------
BEGIN;
INSERT INTO `ci_task_plugin` VALUES ('1', '2016-07-01 11:48:14', '1', '    SVN', '2,', 'green', 'SVN插件', '1,4,5'), ('2', '2016-07-01 11:48:48', '1', '    GIT', '2,', 'red', 'GIT插件', '1,4,5'), ('3', '2016-07-01 11:49:10', '1', '    Shell 命令行', '1,2,3,4', 'orange', 'Shell命令行', '1,4,5'), ('4', '2016-10-31 14:50:00', '1', '    IOS构建', '3,', '#f26522', 'IOS构建', '1,4,5'), ('5', '2016-10-31 15:25:53', '1', '    Android构建', '3,', '#102b6a', 'Ant构建', '1,4,5'), ('6', '2017-02-08 11:47:33', '1', 'GAT API测试', '3,4', '#f15b6c', '接口测试', '1,4,5'), ('7', '2018-03-02 14:32:04', '1', 'GAT UI 测试', '2,3,4', '#b7ba6b', 'WebUI测试', '1,4,5'), ('8', '2016-11-03 13:40:41', '1', '    SSH部署', '3,', '#8f4b2e', '服务部署', '1,4,5,');
COMMIT;

-- ----------------------------
--  Table structure for `ci_task_stage_history`
-- ----------------------------
DROP TABLE IF EXISTS `ci_task_stage_history`;
CREATE TABLE `ci_task_stage_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `TaskID` int(11) NOT NULL,
  `Status` int(11) NOT NULL,
  `StartTime` datetime(6) DEFAULT NULL,
  `EndTime` datetime(6) DEFAULT NULL,
  `BuildResult` int(11) DEFAULT NULL,
  `BuildMessage` varchar(500) DEFAULT NULL,
  `TaskHistoryID` int(11) NOT NULL,
  `TQUUID` varchar(100) DEFAULT NULL,
  `StageID` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8;



-- ----------------------------
--  Table structure for `ci_task_step_output`
-- ----------------------------
DROP TABLE IF EXISTS `ci_task_step_output`;
CREATE TABLE `ci_task_step_output` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `StageID` varchar(100) DEFAULT NULL,
  `TaskID` int(11) NOT NULL,
  `StageHistoryID` int(11) NOT NULL,
  `ProductID` varchar(100) DEFAULT NULL,
  `ProductType` int(11) NOT NULL,
  `StepID` varchar(100) DEFAULT NULL,
  `CodeVersion` varchar(1000) DEFAULT NULL,
  `PackageInfo` varchar(500) DEFAULT NULL,
  `TaskHistoryID` int(11) DEFAULT NULL,
  `ChangeLog` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=760 DEFAULT CHARSET=utf8;



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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;



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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;



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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `dicdata`
-- ----------------------------
DROP TABLE IF EXISTS `dicdata`;
CREATE TABLE `dicdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DicType_id` int(11) NOT NULL,
  `DicDataName` varchar(500) NOT NULL,
  `DicDataValue` varchar(100) DEFAULT NULL,
  `DicDataDesc` varchar(500) DEFAULT NULL,
  `DicDataIsActive` tinyint(1) NOT NULL,
  `DicDataLabel` varchar(50) DEFAULT NULL COMMENT '页面显示标签',
  `Scope` varchar(10) DEFAULT NULL COMMENT '配置作用域 可选值  Global/CI/Project',
  PRIMARY KEY (`id`),
  KEY `dicdata_DicType_id_74ecac2420247de7_fk_dictype_id` (`DicType_id`),
  CONSTRAINT `dicdata_DicType_id_74ecac2420247de7_fk_dictype_id` FOREIGN KEY (`DicType_id`) REFERENCES `dictype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=315 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `dicdata`
-- ----------------------------
BEGIN;
INSERT INTO `dicdata` VALUES ('17', '7', 'Server', 'smtp.teamcat.com', '邮箱服务器', '1', '邮箱服务器', 'Global'), ('18', '7', 'User', 'teamcat', '发件人', '1', '发件人', 'Global'), ('19', '7', 'Password', '123456', '密码，留空表示不需要密码可发送', '1', '密码', 'Global'), ('20', '7', 'Postfix', '@teamvision.com', '邮箱后缀', '1', '邮箱后缀', 'Global'), ('26', '7', 'defautrecivers', 'zhangtiande@teamcat.com,lusiyuan@teamcat.com,yuanqingrong@teamcat.com', '默认收件人邮箱，多个邮箱用逗号分隔', '1', '默认收件人', 'Global'), ('111', '16', 'TaskWaitTimeout', '7200000', '', '1', null, 'CI'), ('112', '16', 'TaskRunTimeout', '7200000', '', '1', null, 'CI'), ('141', '16', 'TimerInterval', '5000', '', '1', null, 'CI'), ('142', '16', 'ControllerInterval', '10000', '', '1', null, 'CI'), ('143', '16', 'AgentDetcterInterval', '60000', '', '1', null, 'CI'), ('148', '26', 'DevScanInterval', '30000', '', '1', null, 'CI'), ('149', '26', 'TaskScanInterval', '5000', '', '1', null, 'CI'), ('150', '26', 'AgentDefaultPort', '8099', '', '1', null, 'CI'), ('151', '26', 'AgentDefaultSpace', '0', './workspace', '1', null, 'CI'), ('158', '26', 'WifiConnectTimeout', '180000', '', '1', null, 'CI'), ('159', '26', 'rerunTimeDefualt', '1', '', '1', null, 'CI'), ('160', '26', 'rerunIsUpdateResult', '1', '', '1', null, 'CI'), ('162', '16', 'LockTimeout', '180000', '', '1', null, 'CI'), ('246', '41', 'white_list', '\'zip\',\'apk\',\'ipa\',\'py\',\'sh\',\'war\',\'jsp\',\'txt\',\'html\',\'xml\'', '多个后缀名以逗号分隔', '1', '文件类型', 'Global'), ('247', '41', 'max_size', '600*1024*1024', '最小单位KB', '1', '文件大小', 'Global'), ('249', '39', 'Always check out a fresh copy', '1', null, '1', null, null), ('250', '39', 'Use svn update as much as possible', '2', null, '1', null, null), ('251', '38', 'Wipe out & shallow clone (无变更日志,耗时短)', '1', null, '1', null, null), ('252', '38', 'Wipe out & full clone (有变更日志,耗时长)', '2', null, '1', null, null), ('269', '16', 'DisasterInterval', '3600000', null, '1', null, 'CI'), ('275', '38', 'revert & update(有变更日志)', '3', null, '1', null, null), ('279', '16', 'TaskLimit', '4', null, '1', null, 'CI'), ('280', '16', 'SocketTimeout', '180000', null, '1', null, 'CI'), ('308', '16', 'IssueInterval', '3600000', '', '1', null, 'CI'), ('309', '40', 'RedisAddress', '140.143.236.132', 'Redis 实例所在IP或者域名', '1', '消息服务器', 'Global'), ('310', '40', 'RedisPort', '8803', 'Redis 实例端口', '1', '端口', 'Global'), ('311', '16', 'IssueVersionlimited', '5', '问题统计版本限制', '1', null, 'CI'), ('312', '26', 'AgentTimeOutMileSec', '7200000', 'Agent超时时间单位毫秒', '1', null, 'CI'), ('313', '16', 'SplitCount', '3', null, '1', null, 'CI'), ('314', '7', 'Port', '25', '邮箱服务端口', '1', '邮箱服务端口', 'Global');
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
  `DicTypeLabel` varchar(50) DEFAULT NULL COMMENT '页面显示标签',
  `Scope` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `dictype`
-- ----------------------------
BEGIN;
INSERT INTO `dictype` VALUES ('7', 'EmailConfig', '1', '7', '邮件设置', 'Global'), ('16', 'ControllerGlobalConfig', '1', '16', 'Controller运行参数', 'CI'), ('26', 'AgentGlobalConfig', '1', '26', 'Agent运行参数', 'CI'), ('38', 'GitCheckOutStrategy', '1', '38', null, 'CI'), ('39', 'SvnCheckOutStrategy', '1', '39', null, 'CI'), ('40', 'MessageQueue', '1', '40', '消息队列', 'Global'), ('41', 'UploadFileLimit', '1', '41', '上传文件限制', 'Global');
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
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `django_content_type`
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry'), ('44', 'administrate', 'device'), ('45', 'administrate', 'devicemanagementhistory'), ('3', 'auth', 'group'), ('2', 'auth', 'permission'), ('4', 'auth', 'user'), ('52', 'authtoken', 'token'), ('9', 'automationtesting', 'autoagent'), ('12', 'automationtesting', 'autocaseresult'), ('10', 'automationtesting', 'automobiledevice'), ('11', 'automationtesting', 'autorunresult'), ('13', 'automationtesting', 'autoservicehost'), ('7', 'automationtesting', 'autotask'), ('14', 'automationtesting', 'autotaskqueue'), ('8', 'automationtesting', 'autotestconfig'), ('16', 'automationtesting', 'dicdata'), ('15', 'automationtesting', 'dictype'), ('75', 'ci', 'autocase'), ('73', 'ci', 'autocaseresult'), ('79', 'ci', 'autotestingtaskresult'), ('58', 'ci', 'casetag'), ('65', 'ci', 'cicredentials'), ('66', 'ci', 'cideployservice'), ('96', 'ci', 'ciflowsectionhistory'), ('67', 'ci', 'ciserver'), ('63', 'ci', 'citask'), ('101', 'ci', 'citaskapitrigger'), ('68', 'ci', 'citaskflow'), ('74', 'ci', 'citaskflowhistory'), ('72', 'ci', 'citaskflowsection'), ('80', 'ci', 'citaskhistory'), ('77', 'ci', 'citaskplugin'), ('102', 'ci', 'citaskstagehistory'), ('103', 'ci', 'citaskstepoutput'), ('76', 'ci', 'servicehost'), ('78', 'ci', 'unittestcaseresult'), ('5', 'contenttypes', 'contenttype'), ('53', 'corsheaders', 'corsmodel'), ('69', 'env', 'mockapi'), ('70', 'env', 'mockhandler'), ('71', 'env', 'mockresponse'), ('54', 'home', 'agent'), ('27', 'home', 'dicdata'), ('26', 'home', 'dictype'), ('55', 'home', 'errormessage'), ('41', 'home', 'fileinfo'), ('59', 'home', 'taskqueue'), ('25', 'home', 'webapps'), ('93', 'interface', 'mockapi'), ('94', 'interface', 'mockhandler'), ('95', 'interface', 'mockresponse'), ('24', 'productquality', 'bugfreemapping'), ('64', 'project', 'issueactivity'), ('81', 'project', 'issuefilter'), ('40', 'project', 'product'), ('35', 'project', 'project'), ('85', 'project', 'projectarchive'), ('89', 'project', 'projectcodeurl'), ('100', 'project', 'projectdocument'), ('62', 'project', 'projectissue'), ('86', 'project', 'projectissuecategory'), ('84', 'project', 'projectissuedailystatistics'), ('99', 'project', 'projectissuepriority'), ('82', 'project', 'projectissueresolvedresult'), ('92', 'project', 'projectissueseverity'), ('83', 'project', 'projectissuestatus'), ('90', 'project', 'projectissueversionstatistics'), ('34', 'project', 'projectmember'), ('56', 'project', 'projectmodule'), ('88', 'project', 'projectos'), ('87', 'project', 'projectosversion'), ('91', 'project', 'projectphase'), ('37', 'project', 'projectrole'), ('97', 'project', 'projecttaskdependency'), ('98', 'project', 'projecttaskowner'), ('36', 'project', 'tag'), ('28', 'project', 'task'), ('61', 'project', 'testapplication'), ('29', 'project', 'version'), ('33', 'project', 'webhook'), ('6', 'sessions', 'session'), ('21', 'testjob', 'codecommitlog'), ('23', 'testjob', 'projectversion'), ('19', 'testjob', 'testbuildhistory'), ('17', 'testjob', 'testjob'), ('20', 'testjob', 'testjobhistory'), ('22', 'testjob', 'testproject'), ('18', 'testjob', 'testprojectsubmition'), ('39', 'user', 'actionlog'), ('51', 'user', 'usergroups'), ('38', 'user', 'user_extend'), ('42', 'user', 'user_group_extend'), ('43', 'user', 'user_permission_extend');
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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `django_migrations`
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2015-12-03 07:57:34'), ('2', 'auth', '0001_initial', '2015-12-03 07:57:39'), ('3', 'admin', '0001_initial', '2015-12-03 07:57:40'), ('4', 'contenttypes', '0002_remove_content_type_name', '2015-12-03 07:57:41'), ('5', 'auth', '0002_alter_permission_name_max_length', '2015-12-03 07:57:41'), ('6', 'auth', '0003_alter_user_email_max_length', '2015-12-03 07:57:42'), ('7', 'auth', '0004_alter_user_username_opts', '2015-12-03 07:57:42'), ('8', 'auth', '0005_alter_user_last_login_null', '2015-12-03 07:57:42'), ('9', 'auth', '0006_require_contenttypes_0002', '2015-12-03 07:57:42'), ('10', 'auth', '0007_user_profiles', '2015-12-03 07:57:43'), ('11', 'auth', '0008_delete_user_profiles', '2015-12-03 07:57:43'), ('12', 'sessions', '0001_initial', '2015-12-03 07:57:43'), ('13', 'admin', '0002_logentry_remove_auto_add', '2016-03-28 06:32:59'), ('14', 'administrate', '0001_initial', '2016-03-28 06:33:00'), ('15', 'auth', '0007_alter_validators_add_error_messages', '2016-03-28 06:33:00'), ('16', 'administrate', '0002_auto_20160328_1434', '2016-03-28 06:35:08'), ('17', 'administrate', '0002_auto_20160330_1107', '2016-05-31 08:56:29'), ('18', 'administrate', '0003_merge', '2016-05-31 08:56:29'), ('19', 'auth', '0008_alter_user_username_max_length', '2017-06-09 08:05:08'), ('20', 'authtoken', '0001_initial', '2017-06-09 08:05:08'), ('21', 'authtoken', '0002_auto_20160226_1747', '2017-06-09 08:05:08'), ('23', 'user', '0001_initial', '2017-06-09 08:28:24'), ('24', 'home', '0001_initial', '2017-06-09 08:35:51'), ('25', 'ci', '0001_initial', '2017-07-12 05:39:49'), ('28', 'env', '0001_initial', '2018-08-06 01:56:06'), ('29', 'auth', '0009_alter_user_last_name_max_length', '2019-02-01 07:16:49'), ('30', 'project', '0001_initial', '2019-02-01 07:21:41'), ('31', 'project', '0002_auto_20190221_1608', '2019-02-21 08:11:04'), ('32', 'ci', '0002_citaskapitrigger', '2019-04-22 06:39:35'), ('35', 'ci', '0003_autocase_autocaseresult_autotestingtaskresult_casetag_cicredentials_cideployservice_ciflowsectionhis', '2019-06-17 11:23:12');
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
--  Records of `django_session`
-- ----------------------------
BEGIN;
INSERT INTO `django_session` VALUES ('1rfi3fbue3m4w23g8iypkewmqbw5io13', 'ZDgzNTI4N2ViM2Q0NjUzMDhmZjdjMGM5YjNhNzI4Y2E5Njg3ZDk5MTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk0MDQ5YzA5MWQ5ZDU1MjNlNWQwOTQ0ZjI2Zjk2MzRlMzcwYTgxYTMiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2018-12-25 07:36:02'), ('1shcujl24g3mdbimfi51ucbtsitfbr45', 'MWI4MzljODRhMjdiOWZlZjJkYzdlMTIzYzM5ZDAzODJiMmM4OTY5NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-07-03 06:04:41'), ('22kf1rr3tnexvdwx3zbbaepu6p1rnnyv', 'ODM2OWI5ZDIxNDA5NTM1OWUwODJiNjc0ZGU3YjZmNGUwY2I2NzZkMzp7Il9hdXRoX3VzZXJfaWQiOiI2Iiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiVXNlciJdLCJfYXV0aF91c2VyX2hhc2giOiIxYmJjMzc3YmVmNWRlYWQ0NThlOTZmNGZmMzlmMDIzZGMwMTM4MTRmIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==', '2019-05-02 03:15:34'), ('2topem90uh4kfuud3bwo9tbn2gfw8849', 'NWJmYzQ4NWJkZTIwYzhlZjZiMDI3OTU4ZjgxNTE1NWEzM2E4ZTY0Mzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIl9hdXRoX3VzZXJfaWQiOiIyIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-01-25 06:02:43'), ('2xyuksy674d2nb23khmm2qardghhn5p2', 'ZGQ0NTU4NzFkNmZmMGUwMDQ0OWZiNDEzODYwYTRjNTI1ODBjMmZjZDp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5NDA0OWMwOTFkOWQ1NTIzZTVkMDk0NGYyNmY5NjM0ZTM3MGE4MWEzIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-02-21 09:58:02'), ('2yhkboxb6a8aj1y980586inixjsow5v0', 'Y2ZmMzBkZTgyYjJmNjk4MGExYWNiZDc0M2FmM2EwNTc5NmU4MTkwMzp7Il9hdXRoX3VzZXJfaWQiOiIyIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-07 05:55:03'), ('3c2yxy1w6gphl9rfteqxcz1gxe6v22za', 'YWIxZDhlNzViZjM1MThmNmNjNGU4NDg0YzVkMGEzZDI5NGYzNzk1ODp7IndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-05-06 06:42:17'), ('3f94yqds3j3cbfxh2ac37m3i2yxl5o1m', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-04-25 11:28:50'), ('3shzvi671dcpy2he3nix7r0wotym4xue', 'ZGQ0NTU4NzFkNmZmMGUwMDQ0OWZiNDEzODYwYTRjNTI1ODBjMmZjZDp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5NDA0OWMwOTFkOWQ1NTIzZTVkMDk0NGYyNmY5NjM0ZTM3MGE4MWEzIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-02-25 01:56:37'), ('453v98xjao7ht47235ptssvdbzqgimb8', 'ZGQ0NTU4NzFkNmZmMGUwMDQ0OWZiNDEzODYwYTRjNTI1ODBjMmZjZDp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5NDA0OWMwOTFkOWQ1NTIzZTVkMDk0NGYyNmY5NjM0ZTM3MGE4MWEzIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-04-03 23:12:44'), ('49im9chc6j32kwnjrkgkarzpkps32b8i', 'YjUwNTkxNDI4YjRjY2IzNWZhZGRmOTE0YzMxYjU2NTQ2ZWI0ZmQzNTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-06-03 12:51:51'), ('4exthk0mekt7c71ytdr2ct103a8b4p7h', 'MTM2YzhmYjk4Y2ZkOTZhMzRmZWUwYjUxMTBjYjVlOGMyM2RhZDFmMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-05-06 07:10:56'), ('4g8k7pcobayqnjgwu0t7ui83rxmjhy4q', 'Yjc4ZTRlODI0NmYwY2VhNzlhNDc5MWMxNmQ1ZGFhZDBiYjZlZDUwNjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5Iiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-05-07 13:41:22'), ('4jsf35cm6bjgu15wlhm4tte53ujtmw5y', 'ZDhiNzg4OGVlNGVlNTNhMGYwZWVmYmZhN2U2MDQ5ZmJmMmRlMWYwZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2019-05-08 12:08:08'), ('6igy8khhqr3bre9m4kqugnyt8hi5j6to', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-04-25 09:57:48'), ('6o4f2elng93mzedcsggxmdna538lak05', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-04-25 07:45:03'), ('774sfs83x34h7fwhfs866d3sl6om0pig', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-03-22 06:31:17'), ('7gzb95duxraahgke56h3qpdypljx4d3d', 'NzFmYzE5ODJhZDUxOGY3ZWJhNzFjYTU4YzNiMTgwMGM4NjJjMzk2ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5Iiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-07-29 12:23:48'), ('8ikjtpwhq996qjwvwubz3smtciumvzfv', 'ZGY2MDc1MGEyMzIwMGM5MWU3ODQ4OWYzY2Y5ZGY2MmY0Y2Q2MmIxNTp7Il9hdXRoX3VzZXJfaGFzaCI6IjljZDQ1OTFkYzBmNWYwYzQxNTliNTNhY2Y3NTZmOWVlMjExODZmNjkiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2019-06-11 02:37:53'), ('8z03a7sbd9muq8cof266efcmxxdoykhv', 'N2U4MTQ0MmEyMjk4YTlhOTNkODA0ZmU3ZWNlZmNkZTA5NzJiMmI3ZTp7IndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-08-09 08:00:38'), ('9e7qz3dam6a6hjpso6y1wxd9q2ped9gz', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-04-25 08:05:21'), ('asz6b2ojmxr7dwmxgwcoy9bzt0h3f028', 'MTM2YzhmYjk4Y2ZkOTZhMzRmZWUwYjUxMTBjYjVlOGMyM2RhZDFmMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-05-06 07:12:33'), ('awtmmg0r8858x8mzk0j39bj8j8pezaaa', 'ZWZmNGE3ZGQzNDYzNjRlNDM2ZDBiOTAwMDMxOTA1ZmVhY2FiMTNiYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2019-05-01 13:00:44'), ('cb10qg8y2xhlezq61eslry6253i1biiz', 'ZDEzNmY4NGYzNzQwNTEwM2Q4OGU2NTgxNTBjMDY1ZGFhM2MyOGE3NDp7IndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5NDA0OWMwOTFkOWQ1NTIzZTVkMDk0NGYyNmY5NjM0ZTM3MGE4MWEzIn0=', '2018-12-23 12:58:19'), ('df77e0crn5attqzgdiaiijpjxh9zllj0', 'NmIzOGQ0YmE2NTMyNTZjOWQ1ZDQ4MDZkMTUxYmRkOGZlNWExYjBjNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjZhNzY2YzYzOTg0OTBhODZkMzlkMjI4OTU3MmYwNjg5NDkyMDY5ZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-08-12 05:36:08'), ('ejrz3jax7mkf0zniinb08etwrthxdqm0', 'MWI4MzljODRhMjdiOWZlZjJkYzdlMTIzYzM5ZDAzODJiMmM4OTY5NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-07-03 05:59:26'), ('f9mf3ur72j0w791v61646nho0fvq3amp', 'ZTUzYjAxODBiMTU0OWRlYzA3NGIwYmQ5MzVmMjBiODEzYmNmM2UwYjp7Il9hdXRoX3VzZXJfaGFzaCI6IjljZDQ1OTFkYzBmNWYwYzQxNTliNTNhY2Y3NTZmOWVlMjExODZmNjkiLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-06-06 02:08:39'), ('fh0xbhxi1fpr6v70zyiwfpqj6fq87wla', 'YmEzOTE0NzU2M2UzMjA1NWRiODNjMDc0ZDYwZWM5ODQxN2MyMWRkZTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk0MDQ5YzA5MWQ5ZDU1MjNlNWQwOTQ0ZjI2Zjk2MzRlMzcwYTgxYTMiLCJfYXV0aF91c2VyX2lkIjoiMiIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-01-29 08:19:19'), ('fqb0ykv4fgingaehj7tstn7mm4z1fi53', 'OGJmNmE1MGFmOWIxZWVkYTFiZDM4M2UwZjc0ZTJiZjk2OGIyNTUxYjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5NDA0OWMwOTFkOWQ1NTIzZTVkMDk0NGYyNmY5NjM0ZTM3MGE4MWEzIn0=', '2019-04-24 03:37:48'), ('g2vtix4fx6dv3e75qb06plqi96x5cpzc', 'MmI0MDgzNWIwYzdhYWFkNmMzNzU0NjZjY2Q2M2FkNmI1NTMwYTRhNDp7Il9hdXRoX3VzZXJfaGFzaCI6IjljZDQ1OTFkYzBmNWYwYzQxNTliNTNhY2Y3NTZmOWVlMjExODZmNjkiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-08-16 05:48:08'), ('gqtczir72acvfhnpetq688wbyjfeoplu', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-03-14 10:51:08'), ('lxjirreo73fvaj84rqhmvogh4knpjyxs', 'MGFlZGVhNjc3NmY3MzRiMGQ2NTZjMzgyMjkyYmViZDc1NGEyN2E4Yjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk0MDQ5YzA5MWQ5ZDU1MjNlNWQwOTQ0ZjI2Zjk2MzRlMzcwYTgxYTMiLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-04-29 02:49:57'), ('o1t1avmpa3h8qh7jf164btlnvejzab43', 'MGFlZGVhNjc3NmY3MzRiMGQ2NTZjMzgyMjkyYmViZDc1NGEyN2E4Yjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk0MDQ5YzA5MWQ5ZDU1MjNlNWQwOTQ0ZjI2Zjk2MzRlMzcwYTgxYTMiLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-04-10 09:41:02'), ('odg2pij6nwot6aml1a74io5c1cnksoil', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-04-24 09:29:39'), ('oj7g14tq577yyp5roq15am2le8rs5s33', 'N2FkYTE1MGMzOWRlNjFiNmY5ZWNjYzNiOTk5YmMzZjYzYzkxYzE3NTp7Il9hdXRoX3VzZXJfaGFzaCI6IjljZDQ1OTFkYzBmNWYwYzQxNTliNTNhY2Y3NTZmOWVlMjExODZmNjkiLCJfYXV0aF91c2VyX2lkIjoiMiIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-21 07:36:31'), ('pkzimixya8svs4hb127ahew5z3fb55z3', 'MTM2YzhmYjk4Y2ZkOTZhMzRmZWUwYjUxMTBjYjVlOGMyM2RhZDFmMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-08-05 05:30:52'), ('q02zta3qi3fxhlu3f0u3c2rtsmgh6mbz', 'NmIzOGQ0YmE2NTMyNTZjOWQ1ZDQ4MDZkMTUxYmRkOGZlNWExYjBjNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjZhNzY2YzYzOTg0OTBhODZkMzlkMjI4OTU3MmYwNjg5NDkyMDY5ZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-01-25 09:57:33'), ('qypqjhb85q3bk9rdmfvow02521n5q11g', 'MTQ2OWI2ZDBmNjM0NzM0MWM0YmU5NzVkNTBhMGMzY2YxNmNiMDFkNDp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-08-07 06:00:33'), ('r9ftrqy3280cmjuns0sh7k38i1vmp1ll', 'ZWJiNTA1YTE1MTY4ZGM4NDg5Y2M4MGU2YzQ1M2IwNDA2MmMwNDM4Yjp7IndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfaGFzaCI6IjljZDQ1OTFkYzBmNWYwYzQxNTliNTNhY2Y3NTZmOWVlMjExODZmNjkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2019-07-29 08:35:08'), ('rdcnsog4ld81imlprmi211uslnneof8p', 'MjY3MWQyMzE4NTc4OGJmNTIyN2VkMWJhYzU0NzMwNTkyOWM1Njc5Yzp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2hhc2giOiI5NDA0OWMwOTFkOWQ1NTIzZTVkMDk0NGYyNmY5NjM0ZTM3MGE4MWEzIn0=', '2019-04-09 06:29:31'), ('rhr3vd0av7wblnozkoqeif342posp6ao', 'MTQ2OWI2ZDBmNjM0NzM0MWM0YmU5NzVkNTBhMGMzY2YxNmNiMDFkNDp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-08-07 06:00:33'), ('rlibyyky2eam5g17yg4ruibetlom68z8', 'ZWZmNGE3ZGQzNDYzNjRlNDM2ZDBiOTAwMDMxOTA1ZmVhY2FiMTNiYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2019-05-01 13:02:42'), ('rort43ge8inb3mdtd2qzhouhurhv7mgx', 'MTQ2OWI2ZDBmNjM0NzM0MWM0YmU5NzVkNTBhMGMzY2YxNmNiMDFkNDp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-08-07 06:00:31'), ('rxhmg63tdrh6tby8hrttl5yzpboltwui', 'YWMzNzRmYzg5Y2U5ZjExYzA1OWRmN2EzYjlmZmYwYTc0OTlkMTlhYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-04-25 07:48:12'), ('t55xl0pwg6bs6z5ohsidrjfcrkyvov5h', 'MGFlZGVhNjc3NmY3MzRiMGQ2NTZjMzgyMjkyYmViZDc1NGEyN2E4Yjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk0MDQ5YzA5MWQ5ZDU1MjNlNWQwOTQ0ZjI2Zjk2MzRlMzcwYTgxYTMiLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-04-09 08:02:01'), ('tff4wg5scy276n65h0ge9q9o948lg2zf', 'MmIwM2NlNGFkMmJmYTFhZDc1N2U1MzU1MDZiM2M2OWRkY2VlZTM2ODp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk0MDQ5YzA5MWQ5ZDU1MjNlNWQwOTQ0ZjI2Zjk2MzRlMzcwYTgxYTMiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-01-10 01:51:12'), ('tfmqdbf4ar5z45khoqbo10lzcrikngu1', 'OTVkNTA5MmVmNjIzZGY0ZDY2YjNmZWQ3NTc2NmI0ODcwNGQ5ZGEzZTp7IndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-05-08 03:14:05'), ('tzmgfnxze067drxrqk8mm1sc7wqqwb48', 'ZTQzNmVhMzgzN2M1ZDVjYjVkYzc0ZmM5MTM3YzMyMTFkMzVmNWI5Mzp7Il9hdXRoX3VzZXJfaGFzaCI6IjljZDQ1OTFkYzBmNWYwYzQxNTliNTNhY2Y3NTZmOWVlMjExODZmNjkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-08-09 09:14:15'), ('u0gm8q0yh9t71fyu6hypstee3lm4d1tc', 'YjUwNTkxNDI4YjRjY2IzNWZhZGRmOTE0YzMxYjU2NTQ2ZWI0ZmQzNTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-05-29 06:58:52'), ('uw33dawljrxjh2xfsch78uq0ftmp4plu', 'ZTE0YzNkOGU1YjRhN2E5MmMyN2ViZDUxYmY1Nzg2YjgxOTYwNWQ1YTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2hhc2giOiI5Y2Q0NTkxZGMwZjVmMGM0MTU5YjUzYWNmNzU2ZjllZTIxMTg2ZjY5In0=', '2019-08-07 11:09:33'), ('wiytoyi89fzjbs7r5rkk0fnq9ay05ikn', 'ZWZmNGE3ZGQzNDYzNjRlNDM2ZDBiOTAwMDMxOTA1ZmVhY2FiMTNiYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXSwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2019-05-02 09:39:01'), ('xi9ex159w5ci5hu5li13uhs6kc7oh7ju', 'YmEzOTE0NzU2M2UzMjA1NWRiODNjMDc0ZDYwZWM5ODQxN2MyMWRkZTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk0MDQ5YzA5MWQ5ZDU1MjNlNWQwOTQ0ZjI2Zjk2MzRlMzcwYTgxYTMiLCJfYXV0aF91c2VyX2lkIjoiMiIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-01-29 08:15:01'), ('xw0couuuv9iqdu9be7d4q1ejxlewsvsp', 'NWJmYzQ4NWJkZTIwYzhlZjZiMDI3OTU4ZjgxNTE1NWEzM2E4ZTY0Mzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTQwNDljMDkxZDlkNTUyM2U1ZDA5NDRmMjZmOTYzNGUzNzBhODFhMyIsIl9hdXRoX3VzZXJfaWQiOiIyIiwid3M0cmVkaXM6bWVtYmVyb2YiOlsiQWRtaW4iXX0=', '2019-01-09 06:17:19'), ('xzw1en0w330eh3h6470thmpmvnlzsgco', 'OGY5Zjk5NDIyODM5YzQ4MDljYmU5MGJiNmMxZDZjMWNmN2RkN2I5Yjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJ3czRyZWRpczptZW1iZXJvZiI6WyJBZG1pbiJdLCJfYXV0aF91c2VyX2hhc2giOiI5NDA0OWMwOTFkOWQ1NTIzZTVkMDk0NGYyNmY5NjM0ZTM3MGE4MWEzIn0=', '2019-03-25 02:49:22'), ('yyvq0k5conrqo2pcb8261vy414qr5j6e', 'ZDhiNzg4OGVlNGVlNTNhMGYwZWVmYmZhN2U2MDQ5ZmJmMmRlMWYwZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWNkNDU5MWRjMGY1ZjBjNDE1OWI1M2FjZjc1NmY5ZWUyMTE4NmY2OSIsIndzNHJlZGlzOm1lbWJlcm9mIjpbIkFkbWluIl0sIl9hdXRoX3VzZXJfaWQiOiIyIn0=', '2019-06-03 05:43:33');
COMMIT;

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
  `FileFolder` int(11) DEFAULT NULL,
  `FileSuffixes` varchar(10) DEFAULT NULL,
  `FileCreator` int(11) NOT NULL,
  `FileSize` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=696 DEFAULT CHARSET=latin1;



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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `interface_mock_api`
-- ----------------------------
BEGIN;
INSERT INTO `interface_mock_api` VALUES ('1', '2018-12-29 02:41:40.179928', '1', 'TEST', '1', '/API/API', '1', null, null, '1', null, null, '', '1', '0', '');
COMMIT;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;



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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

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
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;



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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;



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
  `Archive` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `project_document`
-- ----------------------------
DROP TABLE IF EXISTS `project_document`;
CREATE TABLE `project_document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `ProjectID` int(11) NOT NULL,
  `Type` int(11) NOT NULL,
  `FileID` int(11) NOT NULL,
  `Owner` int(11) NOT NULL,
  `LockBy` int(11) DEFAULT NULL,
  `ReadOnly` tinyint(1) NOT NULL DEFAULT '0',
  `Parent` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;



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
  `Desc` varchar(10000) COLLATE utf8_bin DEFAULT NULL,
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
  `Priority` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;



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
--  Table structure for `project_issue_priority`
-- ----------------------------
DROP TABLE IF EXISTS `project_issue_priority`;
CREATE TABLE `project_issue_priority` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` int(11) NOT NULL,
  `Desc` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `IsActive` bit(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_issue_priority`
-- ----------------------------
BEGIN;
INSERT INTO `project_issue_priority` VALUES ('1', '1', null, 'P0', b'1'), ('2', '2', null, 'P1', b'1'), ('3', '3', null, 'P2', b'1'), ('4', '4', null, 'P3', b'1'), ('5', '5', null, 'P4', b'1');
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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;



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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;



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
INSERT INTO `project_role` VALUES ('1', '2015-11-18 15:57:52', '1', 'User', '#45b97c', '0', null), ('2', '2015-11-18 15:58:34', '1', 'Tester', '#ed1941', '0', null), ('3', '2015-12-03 15:58:51', '1', 'Dev', '#d1923f', '0', null), ('4', '2015-11-18 15:59:20', '1', 'Admin', '#426ab3', '0', null), ('5', '2015-11-18 16:00:09', '1', 'Owner', '#7fb80e', '0', null);
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `project_tag`
-- ----------------------------
BEGIN;
INSERT INTO `project_tag` VALUES ('1', '2015-11-13 16:51:49', '1', ' 安卓', '0', '#32be77', null, '1', '2', '1'), ('2', '2015-11-13 16:53:33', '1', 'IOS', '0', 'red', null, '1', '2', '1'), ('3', '2015-11-13 16:54:02', '1', '功能', '0', 'blue', null, '1', '2', '1'), ('4', '2015-11-13 16:54:38', '1', 'Windows', '0', '#426ab3', null, '1', '2', '1'), ('5', '2015-11-13 17:02:10', '1', '接口', '0', '#426ab3', null, '1', '2', '1'), ('6', '2015-11-13 17:02:32', '1', '长期', '0', 'orange', null, '1', '2', '1'), ('7', '2015-11-13 17:03:08', '1', '开发', '0', '#7fb80e', null, '1', '2', '1'), ('8', '2016-07-25 17:13:01', '1', '构建', '0', '#32be77', null, '1', '2', '1'), ('9', '2016-07-25 17:14:33', '1', '部署', '0', '#6a6da9', null, '1', '2', '1'), ('10', '2016-07-25 17:15:24', '0', '测试', '0', '#00ae9d', null, '1', '2', '1'), ('11', '2016-07-27 10:23:43', '1', 'Android', '0', '#1d953f', null, '1', '2', '3'), ('12', '2016-07-27 10:24:42', '1', 'IOS', '0', '#fdb933', null, '1', '2', '3'), ('13', '2016-11-24 17:40:35', '1', 'Release', '0', '#f05b72', null, '1', '2', '2'), ('14', '2016-11-24 17:48:53', '1', 'Test Complete', '0', '#f391a9', null, '1', '2', '2'), ('15', '2016-11-24 17:50:28', '1', 'Mile Stone', '0', '#d93a49', null, '1', '2', '2'), ('17', '2016-12-15 17:17:51', '1', 'Daily Build', '0', '#faa755', null, '1', '2', '1'), ('29', '2019-05-09 06:40:41', '1', 'Linux', '0', '#8e3459', null, '1', '2', '1'), ('30', '2019-05-09 06:40:48', '1', 'Mac', '0', '#2d4031', null, '1', '2', '1');
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
  `DeadLine` datetime DEFAULT NULL,
  `StartDate` datetime DEFAULT NULL,
  `FinishedDate` datetime DEFAULT NULL,
  `WorkHours` int(11) NOT NULL,
  `Owner` int(11) NOT NULL,
  `Creator` int(11) NOT NULL,
  `Progress` float(11,2) NOT NULL DEFAULT '0.00',
  `Description` varchar(1000) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Tags` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Status` int(11) NOT NULL,
  `Parent` int(11) unsigned DEFAULT NULL,
  `Priority` int(11) NOT NULL DEFAULT '1',
  `Version` int(11) NOT NULL DEFAULT '0',
  `OrderID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=328 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `project_task`
-- ----------------------------
BEGIN;
INSERT INTO `project_task` VALUES ('1', '2018-12-13 01:49:54.727872', '1', '1', 'TestDemo', '2018-12-21 06:32:47', '2018-12-16 23:20:47', null, '8', '2', '0', '0.00', '', null, '0', null, '2', '1', null), ('2', '2018-12-13 01:51:23.766309', '1', '1', 'TestDemo2', '2018-12-24 00:03:59', '2018-12-18 06:47:11', null, '8', '2', '0', '0.00', '', null, '0', null, '3', '1', null), ('3', '2018-12-13 01:51:50.226663', '1', '1', '和规范化个发挂号费和方法和规范化脚后跟积分回房间', '2018-12-22 13:30:23', '2018-12-18 23:35:11', null, '8', '2', '2', '0.00', '', null, '2', null, '3', '1', null), ('4', '2018-12-13 01:53:58.788187', '1', '1', '12', '2018-12-11 00:00:00', null, null, '12', '1', '2', '0.00', '', null, '0', null, '3', '1', null), ('5', '2018-12-13 01:55:16.367450', '1', '1', 'TestDemo12法师打发士大夫撒旦范德萨发生的发生大富士达佛挡杀佛是打发大师傅撒发顺丰', '2019-01-15 17:35:11', '2019-01-08 22:08:47', '2019-02-11 16:00:00', '8', '2', '2', '0.00', '', null, '2', null, '1', '1', null), ('6', '2018-12-13 01:56:53.548121', '0', '1', 'TEST34', '2018-12-14 00:00:00', null, null, '12', '2', '2', '0.00', '', null, '1', null, '3', '1', null), ('7', '2018-12-13 02:09:36.355210', '1', '1', 'test322323飞洒的发的所发生的发送梵蒂冈施工方的', '2019-01-17 00:00:00', '2018-12-20 09:54:23', '2019-02-11 16:00:00', '8', '2', '2', '0.00', '', null, '2', null, '1', '1', null), ('8', '2018-12-13 02:24:24.930940', '1', '1', '233飞洒的范德萨发送的范德萨范德萨', '2019-01-14 00:00:00', '2018-12-20 21:11:11', '2019-02-11 16:00:00', '8', '2', '0', '0.00', '', null, '2', null, '1', '1', null), ('9', '2018-12-13 02:28:44.989132', '1', '1', '发挂号费和规范化风很反感和复活节', '2018-12-13 00:00:00', null, '2018-12-14 00:00:00', '14', '2', '2', '0.00', '', null, '2', null, '1', '1', null), ('10', '2019-01-14 05:45:41.550144', '1', '1', '和尽快缓解看和叫尽快缓解狂欢节狂欢节课', '2019-02-08 00:00:00', null, null, '8', '1', '1', '0.00', '', null, '0', null, '3', '1', null), ('150', '2019-01-31 13:06:37.016804', '1', '1', '需求分析2', '2019-02-27 16:00:00', '2019-02-12 00:03:59', null, '8', '0', '0', '1.00', '', null, '0', null, '3', '4', '0'), ('151', '2019-01-31 13:16:26.245014', '1', '1', '开发', '2019-02-17 17:49:35', '2019-02-11 13:44:47', null, '8', '0', '2', '1.00', '', null, '0', null, '3', '4', '1'), ('253', '2019-02-11 01:57:41.311040', '1', '1', '发布', '2019-02-17 17:49:35', '2019-02-14 13:44:47', null, '8', '0', '0', '1.00', null, null, '0', null, '3', '4', '3'), ('254', '2019-02-11 01:58:39.747998', '1', '1', '测试', '2019-02-23 14:49:35', '2019-02-13 19:09:10', '2019-05-31 08:20:51', '8', '0', '0', '1.00', null, null, '2', null, '3', '4', '2'), ('272', '2019-02-12 05:43:04.456683', '0', '1', 'New task1', '2019-02-22 01:51:59', null, null, '8', '0', '2', '0.00', null, null, '0', '273', '1', '4', '0'), ('273', '2019-02-12 05:50:03.554385', '1', '1', 'New task', '2019-02-23 14:49:35', '2019-02-14 05:49:35', null, '8', '0', '2', '0.00', null, null, '0', '254', '1', '4', '0'), ('274', '2019-02-12 05:51:00.438427', '1', '1', 'New task', '2019-02-17 17:49:35', '2019-02-12 05:51:00', null, '8', '0', '2', '1.00', null, null, '0', '151', '1', '4', '0'), ('275', '2019-02-12 06:04:23.199493', '1', '1', 'New task1', '2019-02-17 17:49:35', null, null, '8', '0', '2', '0.00', null, null, '0', '253', '1', '4', '0'), ('276', '2019-02-12 06:06:58.645090', '1', '1', 'New task2', '2019-02-17 17:49:35', null, null, '8', '0', '2', '0.00', null, null, '0', '253', '1', '4', '1'), ('277', '2019-02-12 06:08:23.970603', '1', '1', 'New task', '2019-02-17 17:49:35', null, null, '8', '0', '2', '0.00', null, null, '0', '253', '1', '4', '2'), ('278', '2019-02-12 06:11:34.045634', '1', '1', 'New task', '2019-02-23 14:49:35', '2019-02-13 19:09:10', null, '8', '0', '2', '0.35', null, null, '0', '254', '1', '4', '1'), ('279', '2019-02-12 06:14:43.709150', '1', '1', 'New task', '2019-02-28 02:27:59', '2019-02-21 04:19:32', null, '8', '0', '2', '1.00', null, null, '0', '150', '1', '4', '0'), ('280', '2019-02-12 09:51:52.712618', '1', '1', 'TEST4', '2019-02-20 18:45:36', '2019-02-13 12:59:05', '2019-05-31 08:20:49', '8', '0', '2', '1.00', '', null, '2', null, '3', '4', null), ('281', '2019-02-12 12:05:55.019065', '1', '1', 'New task', '2019-02-21 10:37:35', '2019-02-12 13:07:12', '2019-05-31 08:20:50', '8', '0', '2', '1.00', null, null, '2', null, '1', '4', '5'), ('282', '2019-02-12 13:33:33.088430', '1', '1', 'New task', '2019-02-10 16:00:00', '2019-02-09 16:00:00', null, '8', '0', '2', '1.00', null, null, '2', null, '1', '4', '6'), ('283', '2019-02-12 13:33:38.770224', '1', '1', 'New task', '2019-02-10 16:00:00', '2019-02-09 16:00:00', null, '8', '0', '2', '1.00', null, null, '0', '282', '1', '4', '0'), ('284', '2019-02-18 13:04:46.755063', '1', '1', 'New task', '2019-02-20 18:45:36', '2019-02-13 12:59:05', null, '8', '0', '2', '1.00', null, null, '0', '280', '1', '4', '0'), ('285', '2019-02-21 08:37:04.192822', '1', '1', 'siyuan', '2019-02-25 16:00:00', '2019-02-09 16:00:00', '2019-05-31 08:20:51', '8', '0', '2', '1.00', null, null, '2', null, '1', '4', '7'), ('286', '2019-02-21 08:37:38.970126', '1', '1', 'New task', '2019-02-25 16:00:00', '2019-02-09 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', '285', '1', '4', '0'), ('287', '2019-02-21 08:38:41.144263', '1', '1', 'New task', '2019-02-25 16:00:00', '2019-02-09 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', '286', '1', '4', '0'), ('288', '2019-02-21 08:38:44.623614', '1', '1', 'New task', '2019-02-25 16:00:00', '2019-02-09 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', '287', '1', '4', '0'), ('289', '2019-02-21 08:38:49.318004', '1', '1', 'New task', '2019-02-25 16:00:00', '2019-02-09 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', '288', '1', '4', '0'), ('290', '2019-02-21 08:38:52.132660', '1', '1', 'New task', '2019-02-25 16:00:00', '2019-02-09 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', '289', '1', '4', '0'), ('291', '2019-03-01 10:56:56.456375', '1', '1', 'New task', '2019-02-10 16:00:00', '2019-02-09 16:00:00', '2019-05-31 08:06:29', '8', '0', '2', '1.00', null, null, '2', null, '1', '4', '8'), ('292', '2019-03-01 11:00:30.941663', '1', '1', 'New task1234', '2019-02-10 16:00:00', '2019-02-09 16:00:00', '2019-05-31 08:06:30', '8', '0', '2', '1.00', null, null, '2', null, '1', '4', '9'), ('293', '2019-04-04 10:17:22.438599', '1', '1', '测试进度更新状态', '2019-04-05 18:44:15', '2019-04-04 10:17:22', '2019-05-31 08:05:21', '8', '0', '2', '1.00', '', null, '2', null, '1', '4', null), ('294', '2019-04-04 14:46:20.903564', '1', '5', 'test', '2019-04-04 16:00:00', null, '2019-04-04 15:02:18', '8', '0', '2', '1.00', '', null, '2', null, '1', '6', null), ('295', '2019-04-04 14:49:10.496720', '1', '5', 'test2', '2019-04-04 16:00:00', null, '2019-04-04 15:02:20', '8', '0', '2', '1.00', '', null, '2', null, '1', '6', null), ('296', '2019-04-04 14:49:56.945513', '1', '5', 'test3', '2019-04-10 16:00:00', null, null, '8', '0', '2', '0.00', '', null, '0', null, '1', '6', null), ('297', '2019-04-04 14:53:09.217554', '1', '5', 'test4', '2019-04-04 16:00:00', null, null, '8', '0', '2', '0.00', '', null, '0', null, '1', '6', null), ('298', '2019-04-04 15:00:20.150570', '1', '5', '测试', '2019-04-10 16:00:00', '2019-04-04 19:54:54', null, '8', '0', '2', '1.00', '', null, '2', null, '1', '6', null), ('299', '2019-04-04 15:34:04.931791', '1', '5', '测试进度同步状态', '2019-04-05 15:34:05', '2019-04-04 15:34:05', null, '8', '0', '2', '1.00', '', null, '2', null, '1', '6', null), ('300', '2019-04-04 15:36:07.531702', '1', '5', '测试创建', '2019-04-05 15:36:08', null, null, '8', '0', '2', '0.00', '', null, '0', null, '1', '6', null), ('301', '2019-04-04 15:36:39.391208', '1', '5', '测试创建2', '2019-04-05 15:36:39', null, null, '8', '0', '2', '0.00', '', null, '0', null, '1', '6', null), ('302', '2019-04-18 03:16:40.686279', '1', '8', 'ceshi', '2019-04-18 16:00:00', null, null, '8', '0', '6', '1.00', '', null, '2', null, '1', '18', null), ('303', '2019-04-18 03:16:40.945389', '1', '8', 'ceseh', '2019-04-18 16:00:00', null, null, '0', '0', '6', '0.00', '', null, '1', '302', '1', '0', null), ('304', '2019-05-22 11:22:21.582691', '1', '1', '222', '2019-02-23 14:49:35', null, null, '0', '0', '0', '0.00', '', null, '0', '254', '1', '0', null), ('305', '2019-05-22 11:33:20.022034', '1', '1', '111', '2019-02-21 10:37:35', null, null, '0', '0', '2', '0.00', '', null, '0', '281', '1', '0', null), ('306', '2019-05-22 11:33:26.977349', '1', '1', '1', '2019-02-10 16:00:00', null, null, '0', '0', '2', '0.00', '', null, '0', '291', '1', '0', null), ('307', '2019-05-22 11:33:35.251780', '1', '1', '1', '2019-02-10 16:00:00', null, null, '0', '0', '2', '0.00', '', null, '0', '292', '1', '0', null), ('308', '2019-05-22 11:33:42.797448', '1', '1', '1', '2019-04-05 18:44:15', null, null, '0', '0', '2', '0.00', '', null, '0', '293', '1', '0', null), ('309', '2019-05-22 11:50:16.914535', '0', '2', 'New task', '2019-05-19 16:00:00', '2019-05-18 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', null, '1', '2', '0'), ('310', '2019-05-22 11:50:24.223226', '0', '2', 'New task', '2019-05-19 16:00:00', '2019-05-18 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', '309', '1', '2', '0'), ('311', '2019-05-22 11:53:15.517851', '0', '2', 'test1', '2019-05-22 16:00:00', null, null, '8', '0', '2', '0.00', '', null, '0', null, '1', '2', null), ('313', '2019-05-22 12:05:31.855438', '0', '2', ' test', '2019-05-22 16:00:00', '2019-05-22 12:05:32', null, '8', '0', '2', '0.00', '', null, '0', null, '1', '2', null), ('314', '2019-05-22 12:05:32.185957', '0', '2', 'test', '2019-05-22 16:00:00', null, null, '0', '0', '2', '0.00', '', null, '0', '313', '1', '2', null), ('315', '2019-05-23 02:17:32.975315', '0', '2', 'TEST', '2019-05-25 22:41:00', '2019-05-23 22:41:33', null, '8', '0', '2', '0.00', '', null, '0', null, '1', '2', null), ('316', '2019-05-23 02:17:33.166700', '0', '2', 'TEST', '2019-05-25 22:41:00', '2019-05-23 22:41:33', null, '8', '0', '2', '0.00', '', null, '0', '315', '1', '2', null), ('317', '2019-05-23 02:27:41.302544', '0', '2', 'New task', '2019-05-19 16:00:00', '2019-05-18 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', null, '1', '2', '0'), ('318', '2019-05-23 02:27:45.159964', '0', '2', 'New task', '2019-05-19 16:00:00', '2019-05-18 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', '317', '1', '2', '0'), ('319', '2019-05-23 02:28:45.757724', '0', '2', 'TEST1', '2019-05-23 16:00:00', '2019-05-23 02:28:46', null, '8', '0', '2', '0.00', '', null, '0', null, '1', '2', null), ('320', '2019-05-23 02:28:45.963823', '0', '2', 'TEST222', '2019-05-23 16:00:00', null, null, '0', '0', '2', '0.00', '', null, '0', '319', '1', '2', null), ('321', '2019-05-23 02:29:34.943667', '0', '2', 'TEST', '2019-05-23 16:00:00', '2019-05-23 02:29:35', null, '8', '0', '2', '0.00', '', null, '0', null, '1', '2', null), ('322', '2019-05-23 02:29:45.055773', '0', '2', 'TEST1', '2019-05-23 16:00:00', null, null, '0', '0', '2', '0.00', '', null, '0', '321', '1', '2', null), ('323', '2019-05-23 02:29:51.206846', '0', '2', 'New task', '2019-05-19 16:00:00', '2019-05-18 16:00:00', null, '8', '0', '2', '0.00', null, null, '0', null, '1', '2', '1'), ('324', '2019-05-23 03:29:27.879656', '1', '2', 'TEST1', '2019-05-24 16:00:00', '2019-05-23 03:29:28', null, '8', '0', '2', '1.00', '', null, '2', null, '1', '2', null), ('325', '2019-05-23 03:43:09.855869', '0', '2', 'test', '2019-05-24 16:00:00', null, null, '0', '0', '2', '0.00', '', null, '0', '324', '1', '0', null), ('326', '2019-05-23 03:45:10.511817', '0', '2', '1', '2019-05-24 16:00:00', null, null, '0', '0', '2', '0.00', '', null, '0', '324', '1', '2', null), ('327', '2019-07-23 10:32:08.108777', '1', '1', '任务Owner增加任务类型字段', '2019-07-23 16:00:00', null, null, '8', '0', '2', '0.00', '', null, '0', null, '1', '4', null);
COMMIT;

-- ----------------------------
--  Table structure for `project_task_dependency`
-- ----------------------------
DROP TABLE IF EXISTS `project_task_dependency`;
CREATE TABLE `project_task_dependency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Predecessor` int(11) NOT NULL,
  `Successor` int(11) NOT NULL,
  `Type` int(11) NOT NULL,
  `Version` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



-- ----------------------------
--  Table structure for `project_task_owner`
-- ----------------------------
DROP TABLE IF EXISTS `project_task_owner`;
CREATE TABLE `project_task_owner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CreationTime` datetime(6) NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Owner` int(11) NOT NULL,
  `Unit` double NOT NULL,
  `Task` int(11) NOT NULL,
  `Version` int(11) NOT NULL,
  `TaskType` int(11) NOT NULL DEFAULT '1' COMMENT '1: 任务,2：提测',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=310 DEFAULT CHARSET=utf8;



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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;



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
  `VersionFiled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;



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
--  Table structure for `tag_owner`
-- ----------------------------
DROP TABLE IF EXISTS `tag_owner`;
CREATE TABLE `tag_owner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Owner` int(11) NOT NULL,
  `OwnerType` int(11) NOT NULL,
  `TagID` int(11) NOT NULL,
  `CreationTime` datetime DEFAULT NULL,
  `IsActive` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;



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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

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
  `Creator` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `team`
-- ----------------------------
BEGIN;
INSERT INTO `team` VALUES ('1', '2018-05-16 17:15:25.000000', '1', 'Android', null, null), ('2', '2018-05-16 17:15:32.000000', '1', 'IOS', null, null), ('3', '2018-05-16 17:15:49.000000', '1', '前端', null, null), ('4', '2018-05-16 17:16:05.000000', '1', '服务端', null, null), ('5', '2018-05-16 17:16:18.000000', '1', 'PM', null, null);
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
) ENGINE=InnoDB AUTO_INCREMENT=1447 DEFAULT CHARSET=latin1;



SET FOREIGN_KEY_CHECKS = 1;
