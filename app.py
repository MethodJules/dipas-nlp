#!/usr/bin/python
# coding=latin-1
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hallo'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
