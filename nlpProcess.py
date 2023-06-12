import spacy
import os
from gensim import corpora, models
import gensim
import pyLDAvis.gensim as gensimvis
import pyLDAvis
import spacy
from spacy.lang.de.stop_words import STOP_WORDS

from gensim.parsing.preprocessing import STOPWORDS
from spacy.lang.de import German
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
        self.comments = []  # Initialisierung des comments-Attributs
        self.dictionary = None
        self.corpus = None
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
    
    # def removeStopwords(self, comments_input):
    #     '''
    #     Removes the stopwords from a comment dictionary.
    #
    #     Parameters
    #     -----------
    #     comments_input : dict
    #         dictionary of comments where for each the stopwords shall be removed
    #
    #     Returns
    #     ----------
    #     filtered_dict : dict
    #         dictionary that contains all comments without the identified stopwords
    #     '''
    #     filtered_dict = {}
    #     for id, comment in comments_input.items():
    #         doc = self.nlp(comment)
    #         filtered_tokens = [token.text for token in doc if not token.is_stop]
    #         filtered_dict[id] = filtered_tokens
    #
    #     return filtered_dict


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


    def removeStopwords(self, comments_input):
        # Laden des deutschen Sprachmodells von spaCy
        nlp = spacy.load('de_core_news_sm')

        # Benutzerdefinierte Liste von Stoppwörtern
        custom_stopwords = ['zudem', 'somit', 'mal', 'bitte']

        filtered_list = []
        for comment in comments_input:
            doc = nlp(comment['text'])
            filtered_tokens = [token.text for token in doc if
                               not token.is_stop and token.text.lower() not in STOP_WORDS and token.text.lower() not in custom_stopwords]
            filtered_text = ' '.join(filtered_tokens)  # Tokens zu einem Satz verbinden
            filtered_list.append(filtered_text)

        return filtered_list



    def performTopicModeling(self, comments_input):
        comment_texts = [comment['text'] for comment in comments_input.values()]
        tokenized_texts = []


        nlp = spacy.load('de_core_news_sm')
        STOP_WORDS.update(['m', 'bitte', 'mal', 'zudem', 'unbedingt', 'somit', 'super', 'toll', 'zusätzlich', 'wichtig'])
        for text in comment_texts:
            doc = nlp(text)
            tokens = [token.lemma_ for token in doc if
                      not token.is_stop and token.is_alpha and token.text.lower() not in STOP_WORDS]
            tokenized_texts.append(tokens)

        self.dictionary = corpora.Dictionary(tokenized_texts)
        self.corpus = [self.dictionary.doc2bow(tokens) for tokens in tokenized_texts]

        num_topics = 5
        lda_model = models.LdaModel(self.corpus, num_topics=num_topics, id2word=self.dictionary, random_state=42)

        topics = {}
        for topic_id, topic_words in lda_model.show_topics(formatted=False):
            topics[f"Topic {topic_id + 1}"] = [word for word, _ in topic_words]

        # Sortieren
        sorted_topics = {key: topics[key] for key in sorted(topics.keys(), key=lambda x: int(x.split()[1]))}

        return sorted_topics




    def labelTopics(self, topics):
        labeled_topics = {}
        for topic_id, topic_words in topics.items():
            if topic_id == 'Topic 1':
                label = 'Engagement'
            elif topic_id == 'Topic 2':
                label = 'Nachhaltigkeit'
            elif topic_id == 'Topic 3':
                label = 'Freizeitgestaltung'
            elif topic_id == 'Topic 4':
                label = 'Öffentliche Spielplätze'
            elif topic_id == 'Topic 5':
                label = 'Spielplatz'
            # elif topic_id == 'Topic 6':
            #     label = 'Pflege'
            # elif topic_id == 'Topic 7':
            #     label = 'Verbindung'
            # elif topic_id == 'Topic 8':
            #     label = 'Spielplatz'
            # elif topic_id == 'Topic 9':
            #     label = 'Fußgänger'
            # elif topic_id == 'Topic 10':
            #     label = 'Entscheidung'
            else:
                label = 'Unbekanntes Thema'

            labeled_topics[label] = topic_words

        return labeled_topics

    def visualizeTopics(self, topics):
        dictionary = gensim.corpora.Dictionary(topics.values())
        corpus = [dictionary.doc2bow(words) for words in topics.values()]
        lda_model = gensim.models.LdaModel(corpus, num_topics=len(topics), id2word=dictionary)

        vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
        pyLDAvis.save_html(vis_data, 'lda_visualization.html')

