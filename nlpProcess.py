import spacy
import os
from spacy_sentiws import spaCySentiWS

class nlpProcess(object):
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
            sentiment_scores.append({'text': token.text, 'sentiment_score': token._.sentiws, 'POS': token.pos_})
        return sentiment_scores
    
    def findEntities(self, comments_input):
        entity_dict = {}
        for id, comment in comments_input.items():
            doc = self.nlp(comment)
            entity_list = []
            for ent in doc.ents:
                entity_list.append({'Entität: ': ent.text,'Typ: ': ent.label_})
            entity_dict[id] = entity_list
        return entity_dict
    