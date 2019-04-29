#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import flask
from flask import Flask
from flask import request
import requests
import datetime
from peewee import *
import psycopg2
import json
import sys
from args import params

reload(sys)
sys.setdefaultencoding('utf8')

lang = 'ru_RU'
transport_types = 'suburban'
system = 'esr'
address = 'https://api.rasp.yandex.net/v3.0/search/?apikey=3a91f747-0a08-4fa3-ad32-c014a043b08c'
app = Flask(__name__)



@app.route('/nextTrain', methods=['POST'])
def next_train():
    departure = flask.request.args['departure']
    arrival = flask.request.args['arrival']
    data = get_trains(departure, arrival)
    out = ''
    for train in data["segments"]:
        if str(train["arrival"][11:19:1]) >= str(datetime.datetime.now().strftime("%H:%M:%S")):
            out += train["thread"]["title"]
            out += " " * (50 - len(train["thread"]["title"]))
            out += str(train["arrival"])[11:19:1]
            out += '\n'
            break
    if out == '':
        out = "Не найдено подходящих поездов"
    return out


@app.route('/rasp', methods=['POST'])
def rasp():
    departure = flask.request.args['departure']
    arrival = flask.request.args['arrival']
    data = get_trains(departure, arrival)
    out = ''
    for train in data["segments"]:
        out += train["thread"]["title"]
        out += " " * (50 - len(train["thread"]["title"]))
        out += str(train["arrival"])[11:19:1]
        out += '\n'
    if out == '':
        out = "Не найдено подходящих поездов"
    return out

def get_trains(departure, arrival):
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    arrival_code = get_code(arrival)
    departure_code = get_code(departure)
    response = requests.get(address + '&lang=' + lang + '&transport_types=' + transport_types + '&system=' + system + '&date=' + date + '&from=' + departure_code + '&to=' + arrival_code)
    return json.loads(response.text)

def get_code(station):
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('SELECT code FROM codes where name = %s LIMIT 1', (station, ))
        for row in cur:
            return str(row[0])


if __name__ == "__main__":
    PORT = '5000'
    app.run('::', PORT, debug=True, threaded=True)
