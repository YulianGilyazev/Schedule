#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sys
import psycopg2
import os
from args import params


path = os.getcwd() + '/esr.csv'
with psycopg2.connect(**params) as conn:
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS data')
    cur.execute('DROP TABLE IF EXISTS codes')
    cur.execute('DROP TABLE IF EXISTS schedule')
    cur.execute('''
       CREATE TABLE data
            (unusingcolumn1 varchar(50),
            code varchar(50),
            unusingcolumn2 varchar(50),
            unusingcolumn3 varchar(50),
            unusingcolumn4 varchar(50),
            unusingcolumn5 varchar(50),
            unusingcolumn6 varchar(50),
            unusingcolumn7 varchar(50),
            unusingcolumn8 varchar(50),
            unusingcolumn9 varchar(50),
            name varchar(50)
        )
    ''')
    path = os.getcwd() + '/esr.csv'
    cur.execute("COPY data FROM %s DELIMITER %s CSV", (path, ';'))
    cur.execute('''
        CREATE TABLE codes
            (code VARCHAR(50),
            name VARCHAR(50)
        )
        ''')
    cur.execute('''
        INSERT INTO codes (code, name)
            SELECT code, name FROM data WHERE code != 'esr';
    ''')
    cur.execute('''
        Create TABLE schedule(
            suburban varchar(50),
            arrival_station varchar(50),
            departure_station varchar(50),
            departure_time varchar(50)
        )     
    ''')

