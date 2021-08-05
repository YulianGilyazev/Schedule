#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import flask
from flask import Flask
from flask import request
import requests
from datetime import datetime
import psycopg2
import json
from args import params, PORT, HOST, lang, transport_types, system, address


app = Flask(__name__)


@app.route('/nextTrain', methods=['POST'])
def next_train():
    departure = flask.request.args['departure']
    arrival = flask.request.args['arrival']
    data = get_trains(departure, arrival)
    out = ''
    for train in data:
        if str(train[1]) >= str(datetime.now().strftime("%H:%M:%S")):
            out = ' '.join([str(train[0]), str(train[1])])
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
    for train in data:
        out = ' '.join([out, str(train[0]), str(train[1]), '\n'])
    if out == '':
        out = "Не найдено подходящих поездов"
    return out


def get_trains(departure, arrival):
    date = str(datetime.now().strftime("%Y-%m-%d"))
    arrival_code = get_code(arrival)
    departure_code = get_code(departure)
    try:
        response = requests.get(address + '&lang=' + lang + '&transport_types=' + transport_types + '&system=' + system + '&date=' + date + '&from=' + str(departure_code) + '&to=' + str(arrival_code))
        data = json.loads(response.text)
        name_and_time = []
        with psycopg2.connect(**params) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM schedule WHERE arrival_station = %s AND departure_station = %s",
                        (arrival, departure))
            for train in data["segments"]:
                time = str(train['arrival'])[11:19]    #time = datetime.strptime(str(train['arrival']), '%Y-%m-%dT%H:%M:%S%z') не работает(
                name_and_time.append([train['thread']['title'], time])
                cur = conn.cursor()
                cur.execute('''
                            INSERT INTO schedule(suburban, arrival_station, departure_station, departure_time)
                            VALUES(%s, %s, %s, %s);
                            ''', (train["thread"]["title"], arrival, departure, time)
                            )
        return name_and_time
    except BaseException:
        with psycopg2.connect(**params) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT suburban, departure_time
                FROM schedule
                WHERE departure_station = %s AND arrival_station = %s
                ORDER BY departure_time;
                ''', (departure, arrival)
                )
            name_and_time = []
            for row in cur.fetchall():
                name_and_time.append([str(row[0]).strip(), str(row[1]).strip()])
            return name_and_time


def get_code(station):
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('SELECT code FROM codes where name = %s LIMIT 1;', (station, ))
        for row in cur:
            return str(row[0])


if __name__ == "__main__":
    app.run('::', PORT, debug=True, threaded=True)
