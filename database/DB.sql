DROP DATABASE IF EXISTS NLQ;
CREATE DATABASE NLQ;

use NLQ;

DROP TABLE IF EXISTS person;
CREATE TABLE person(    
        person_id VARCHAR(255) PRIMARY KEY COMMENT '人员ID',
        person_name VARCHAR(255) DEFAULT NULL COMMENT '人员姓名',
        edu VARCHAR(255) COMMENT '教育经历',
        age INT COMMENT '生日',
        gender INT COMMENT '性别{1:男, 0:女}',
        jobrank VARCHAR(255) COMMENT '职级'
        ) DEFAULT CHARSET=UTF8, COMMENT '人员基本信息表';

DROP TABLE IF EXISTS experience;
CREATE TABLE experience(
        exp_id VARCHAR(255) PRIMARY KEY COMMENT '经历ID',
        exp_text TEXT COMMENT '经历文本',
        time_start DATE COMMENT '经历开始日期',
        time_end DATE COMMENT '经历结束日期',
        person_id VARCHAR(255) COMMENT '经历所属人员ID',
        INDEX (person_id)
        ) DEFAULT CHARSET=UTF8, COMMENT '经历表';

DROP TABLE IF EXISTS label;
CREATE TABLE label(
        label_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '标签ID',
        label_text VARCHAR(255) COMMENT '标签文本',
        person_id VARCHAR(255) COMMENT '标签所属人员ID',
        exp_id VARCHAR(255) DEFAULT NULL COMMENT '标签所属经历ID',
        time_start DATE DEFAULT NULL COMMENT '标签开始日期',
        time_end DATE DEFAULT NULL COMMENT '标签结束日期',
        INDEX (person_id),
        INDEX (exp_id)
        ) DEFAULT CHARSET=UTF8, COMMENT '标签表';