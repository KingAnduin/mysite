# -*- coding:utf-8 -*-
# 迁移数据库，将pymysql伪装成mysqlclient
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
