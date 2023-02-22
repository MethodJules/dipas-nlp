import spacy
import os
from spacy_sentiws import spaCySentiWS
from neo4jHandler import neo4jConnector

class nlpProcess(object):
    nlp = None
    driver = None
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Initiate class and load spacy
    def __init__(self):
        '''
        Contstructor
        '''
        self.nlp = spacy.load('de_core_news_sm') # load the german corpora
        
    
    def analyzeSentiments(self, text):
        # modify the spacy pipeline
        self.nlp.add_pipe('sentiws', config={'sentiws_path': 'data/sentiws'})
        sentiment_scores = []

        # create the space document object
        doc = self.nlp(text)
        for token in doc:
            # print('{},{},{}'.format(token.text, token._.sentiws, token.pos_))
            sentiment_scores.append({'text': token.text, 'sentiment_score': token._.sentiws, 'POS': token.pos_})
        return sentiment_scores

    def getOverallSentimentScore(self, sentiment_scores):
        res = [ sub['sentiment_score'] for sub in sentiment_scores]
        overallSentimentScore = sum(filter(None, res))
        return overallSentimentScore
                

    def nameEntityRecognition(self, text):
        nameEntityRecognitions = []
        doc = self.nlp(text)
        for ent in doc.ents:
            nameEntityRecognitions.append({'text': ent.text, 'NER': ent.label_})
        return nameEntityRecognitions

    def connect_db(self):
        self.driver = neo4jConnector()