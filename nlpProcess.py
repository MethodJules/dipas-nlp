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
        self.nlp = spacy.load('de_core_news_lg') # load the german corpora
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
        '''
        Analyzes for a dictionary of comments which entities are contained in each of the comments.

        Parameters
        -----------
        comments_input : dict
            dictionary of comments to analyze in terms of contained entities

        Returns
        ----------
        entity_dict : dict
            dictionary that lists entities for each comment
        '''
        entity_dict = {}
        for id, comment in comments_input.items():
            doc = self.nlp(comment)
            entity_list = []
            for ent in doc.ents:
                entity_list.append({'Entität: ': ent.text,'Typ: ': ent.label_})
            entity_dict[id] = entity_list
        return entity_dict
    
    def extractRelations(self, comment):
        '''
        Analyzes for comments which relations are contained.

        Parameters
        -----------
        comment : str
            comment to analyze in terms of contained relations

        Returns
        ----------
        relations : list 
            list that contains all relations in a comment
        '''
        doc = self.nlp(comment)
        relations = []
        for sent in doc.sents:
            for tok in sent:
                if tok.dep_ in ["sb", "sbp"] and tok.head.pos_ == "VERB":
                    subj = tok
                    verb = tok.head
                    obj = ""
                    for child in verb.children:
                        if child.dep_ == "da":
                            obj = child
                    
                    relations.append((subj, verb, obj))

        return relations
    
    def removeStopwords(self, comments_input):
        '''
        Removes the stopwords from a comment dictionary.

        Parameters
        -----------
        comments_input : dict
            dictionary of comments where for each the stopwords shall be removed

        Returns
        ----------
        filtered_dict : dict 
            dictionary that contains all comments without the identified stopwords
        '''
        filtered_dict = {}
        for id, comment in comments_input.items():
            doc = self.nlp(comment)
            filtered_tokens = [token.text for token in doc if not token.is_stop]
            filtered_dict[id] = filtered_tokens

        return filtered_dict
    
    def filterNames(self, comments_input):
        '''
        Removes real names from comments due to privacy requirements.

        Parameters
        -----------
        comments_input : dict
            dictionary of comments which shall be filtered 
        
        Returns
        -----------
        filtered_dict : dict
            dictionary containing original comments without real names
        '''
        filtered_dict = {}
        for id, comment in comments_input.items():
            doc = self.nlp(comment)
            filteredComment = comment
            for ent in doc.ents:
                if ent.label_ == 'PER':
                    filteredComment = filteredComment.replace(ent.text, "<Klarname entfernt>")
            filtered_dict[id] = filteredComment

        return filtered_dict
    
    def filterLocations(self, comments_input):
        '''
        Removes real names from comments due to privacy requirements.

        Parameters
        -----------
        comments_input : dict
            dictionary of comments which shall be filtered 
        
        Returns
        -----------
        location_dict : list
            list containing locations
        '''
        locations = []
        for id, text in comments_input.items():
            comment = text['text']
            doc = self.nlp(comment)
            for ent in doc.ents:
                if ent.label_ == 'LOC':
                    locations.append(ent.text)

        return locations
