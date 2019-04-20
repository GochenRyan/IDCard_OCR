#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import local_config as lc

def connect_idcard_db():
    return pymysql.connect(
        host='47.101.221.80',
        port=3306,
        user=lc.user,
        password=lc.password
    )

def inset_cardinfo(info):
    db = connect_idcard_db()
    cursor = db.cursor()
    sql = "INSERT INTO IDCardDB.cardinfo(idnumber,name,sex,ethnicity,year,month,day,address)"\
          "VALUES('%s','%s','%s','%s','%d','%d','%d','%s')" % \
          (info['id_number'], info['name'], info['sex'], info['ethnicity'], info['year'], info['month'], info['day'], info['address'])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
