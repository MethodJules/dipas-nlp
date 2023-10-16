import spacy
import os
from spacy_sentiws import spaCySentiWS
class SentimentAnalyzer(object):
    nlp = None
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Initiate class and load spacy
    def __init__(self):
        '''
        Contstructor
        '''
        self.nlp = spacy.load('de_core_news_sm') # load the german corpora
        # modify the spacy pipeline
        self.nlp.add_pipe('sentiws', config={'sentiws_path': 'data/sentiws'})


    def analyzeSentiments(self, text):
        sentiment_scores = []
        # create the space document object
        doc = self.nlp(text)
        for token in doc:
            # print('{},{},{}'.format(token.text, token._.sentiws, token.pos_))
            if token._.sentiws:
                print(token._.sentiws)
                sentiment_scores.append(token._.sentiws)
        return sum(sentiment_scores)