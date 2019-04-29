#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sys
import psycopg2
import os
path = os.getcwd() + '/esr.csv'


params = dict(dbname="rasp", user="yulian", password="12369", host="localhost")
with psycopg2.connect(**params) as conn:
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS table1')
    cur.execute('DROP TABLE IF EXISTS codes')
    cur.execute('''
       CREATE TABLE table1
            (c1 varchar(50),
            c2 varchar(50),
            c3 varchar(50),
            c4 varchar(50),
            c5 varchar(50),
            c6 varchar(50),
            c7 varchar(50),
            c8 varchar(50),
            c9 varchar(50),
            c10 varchar(50),
            c11 varchar(50)
        )
    ''')
    path = os.getcwd() + '/esr.csv'
    cur.execute("COPY table1 FROM %s DELIMITER %s CSV", (path, ';'))
    cur.execute('''
        CREATE TABLE codes
            (code VARCHAR(50),
            name VARCHAR(50)
        )
        ''')
    cur.execute('''
        INSERT INTO codes (code, name)
            SELECT c2, c11 FROM table1 WHERE c2 != 'esr';
    ''')