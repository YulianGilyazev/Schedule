#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import requests
import argparse
from args import HOST
from args import PORT
import sys


def get_args():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers (dest='action')
    nextTrain = subs.add_parser('nextTrain', help='Action next train')
    nextTrain.add_argument('--departure-station', dest='departure', help='Choose departure station')
    nextTrain.add_argument('--arrival-station', dest='arrival', help='Choose arrival station')
    rasp = subs.add_parser('rasp', help='Action all raspisanie')
    rasp.add_argument('--departure-station', dest='departure', help='Choose departure station')
    rasp.add_argument('--arrival-station', dest='arrival', help='Choose arrival station')
    args = parser.parse_args()
    return args.action, args.departure, args.arrival


def next_train(departure, arrival):
    response = requests.post('http://' + HOST + ':' + PORT + '/nextTrain', params={'departure': departure, 'arrival': arrival})
    return response.text


def rasp(departure, arrival):
    response = requests.post('http://' + HOST + ':' + PORT + '/rasp', params={'departure': departure, 'arrival': arrival})
    return response.text


if __name__ == '__main__':
    args = get_args()
    action = args[0]
    departure = args[1]
    arrival = args[2]
    if action == 'nextTrain':
        print(next_train(departure, arrival))
    if action == 'rasp':
        print(rasp(departure, arrival))

