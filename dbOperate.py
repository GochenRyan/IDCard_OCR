#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import local_config as lc

def connect_idcard_db():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user=lc.user,
        password=lc.password
    )

def inset_cardinfo(info):
    db = connect_idcard_db()
    cursor = db.cursor()
    sql = "INSERT INTO idcard.cardinfo(idnumber,name,sex,ethnicity,year,month,day,address,face)"\
          "VALUES('%s','%s','%s','%s','%d','%d','%d','%s', '%s')" % \
          (info['id_number'], info['name'], info['sex'], info['ethnicity'], info['year'], info['month'], info['day'],
           info['address'], info['face'])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def update_cardinfo(info):
    db = connect_idcard_db()
    cursor = db.cursor()
    sql = "UPDATE idcard.cardinfo SET name='%s',sex='%s',ethnicity='%s',year='%d',month='%d',day='%d',address='%s' WHERE idnumber='%s'" % \
          (info['name'], info['sex'], info['ethnicity'], info['year'], info['month'], info['day'],
           info['address'],info['id_number'])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.commit()
    db.close()

def select_cardinfo(info):
    db = connect_idcard_db()
    cursor = db.cursor()
    sql = "SELECT * FROM idcard.cardinfo WHERE idnumber='%s'" % (info['id_number'])
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        m_info = {}
        for result in results:
            m_info['id_number'] = result[0]
            m_info['name'] = result[1]
            m_info['sex'] = result[2]
            m_info['ethnicity'] = result[3]
            m_info['year'] = result[4]
            m_info['month'] = result[5]
            m_info['day'] = result[6]
            m_info['address'] = result[7]
            m_info['face'] = result[8]
        db.close()
        return m_info
    except:
        db.close()
        return ''
