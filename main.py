import flask
from flask import Flask
from flask import request
import requests
app = Flask(__name__)

@app.route('/nextTrain', methods=['POST'])
def next_train():
    departure = flask.request.args['departure']
    arrival = flask.request.args['arrival']
    return (str(departure) + ' ' + str(arrival)) # пока вывожу только станции отправления и прибытия


@app.route('/rasp', methods=['POST'])
def rasp():
    departure = flask.request.args['departure']
    arrival = flask.request.args['arrival']
    return (str(departure) + '  #  ' + str(arrival)) # пока вывожу только станции отправления и прибытия разделенные '#'


if __name__ == "__main__":
    PORT = '5000'
    app.run('::', PORT, debug=True, threaded=True)
