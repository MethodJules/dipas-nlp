#!/usr/bin/python
# coding=latin-1
from flask import Flask
from flask import request
from sentimentAnalyzerClass import SentimentAnalyzer
import json

app = Flask(__name__)

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

# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
