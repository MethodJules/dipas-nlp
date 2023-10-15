#!/usr/bin/python
# coding=latin-1
from flask import Flask
from flask import request
from sentimentAnalyzerClass import SentimentAnalyzer
from nlpProcess import nlpProcess
import json

app = Flask(__name__)
nlpProc = nlpProcess()
@app.route('/')
def hello_world():
    return 'Hallo'

@app.route('/sentiment', methods=['POST'])
def analyzeSentiment():
    request_data = request.get_json()

    comment_text = request_data['comment_text']
    comment_id = request_data['comment_id']
    sentimentAnalyzer = SentimentAnalyzer()
    sentiment_score = sentimentAnalyzer.analyzeSentiments(comment_text)
    return json.dumps({"comment_id": comment_id, "sentiment_score": sentiment_score}).encode('utf-8')

@app.route('/filter-names', methods=['POST'])
def filter_names():
    # Laden der Namen aus den TXT-Dateien in Sets
    vornamen = nlpProc.load_txt('vornamen_deutsch.txt')
    nachnamen = nlpProc.load_txt('nachnamen_deutsch.txt')
    request_data = request.get_json()

    comment_text = request_data['comment_text']
    comment_id = request_data['comment_id']
    input = {comment_id: {"text": comment_text}}
    privacy = nlpProc.filterNames(input, vornamen, nachnamen)

    return json.dumps(privacy)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
