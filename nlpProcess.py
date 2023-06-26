import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
import os
from gensim import corpora, models
import gensim
import pyLDAvis.gensim as gensimvis
import pyLDAvis
import spacy
from spacy.lang.de.stop_words import STOP_WORDS
from gensim.parsing.preprocessing import STOPWORDS
from spacy.lang.de import German
import regex as re
from spacy_sentiws import spaCySentiWS
import synonymMethod

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

        self.matcher = Matcher(self.nlp.vocab)
        self.initializeMatcher()
    
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
            dictionary containing only comments containing names
            format: {comment_id {comment, name}}
        '''
        filtered_dict = {}
        for id, comment in comments_input.items():
            doc = self.nlp(comment['text'])
            filteredComment = comment['text']
            names = []
            for ent in doc.ents:
                if ent.label_ == 'PER':
                    names.append(ent.text)
                    filteredComment = filteredComment.replace(ent.text, "<Klarname entfernt>")
            if names:
                filtered_dict[id] = {
                    'comment': filteredComment,
                    'names': names
                }

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
        '''
        Die Funktion removeStopwords verwendet das spaCy-Sprachmodell, um Stoppwörter aus den Kommentaren zu entfernen. 
        Dabei werden sowohl Standard-Stoppwörter als auch benutzerdefinierte Stoppwörter berücksichtigt. 
        Die gefilterten Kommentare werden als Ergebnis zurückgegeben.
        '''
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
        '''
        Die gegebene Funktion performTopicModeling führt Topic Modeling auf Basis von 
        Kommentaren durch. Dabei werden die Kommentartexte tokenisiert, ein Wörterbuch erstellt, 
        ein Bag-of-Words-Modell erstellt und schließlich ein LDA-Modell trainiert, um Topics zu 
        generieren. Die generierten Topics werden sortiert und zurückgegeben.
        '''
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

    def initializeMatcher(self):
        synonyms_time = synonymMethod.get_synonyms("momentan")
        synonyms_time += synonymMethod.get_synonyms("ständig")
        synonyms_time += synonymMethod.get_synonyms("immer")
        lc_time = [synonym.lower() for synonym in synonyms_time]
        synonyms_absence = synonymMethod.get_synonyms("ausbleiben")
        lc_absence = [synonym.lower() for synonym in synonyms_absence]
        
        # Definition der zu identifizierenden Pattern
        pattern1 = [{'POS': "ADP"}, {'POS': "DET"}, {'POS': "NOUN", 'ENT_TYPE': "LOC"}]
        pattern2 = [{'POS': "ADP"}, {'POS': "DET"}, {'POS': "PROPN", 'ENT_TYPE': "LOC"}]
        pattern3 = [{'POS': "ADP"}, {'POS': "NOUN", 'ENT_TYPE': "LOC"}]
        pattern4 = [{'POS': "ADP"}, {'POS': "PROPN", 'ENT_TYPE': "LOC"}]
        pattern5 = [{'POS': "AUX", 'LEMMA': {"IN": ["können"]}}]
        pattern6 = [{'LOWER': {"IN": lc_time}}]
        pattern7 = [{'POS': "VERB", 'LEMMA': {"IN": lc_absence}}]
        pattern8 = [{'POS': "AUX", 'LEMMA': {"IN":["sein", "wird", "müssen", "dürfen"]}}]
        patternF = [{'TEXT': "?"}]

        # Hinzufügen der Patterns zum Matcher
        self.matcher.add("Einschätzung", [pattern1])
        self.matcher.add("Einschätzung", [pattern2])
        self.matcher.add("Einschätzung", [pattern3])
        self.matcher.add("Einschätzung", [pattern4])
        self.matcher.add("Einschätzung", [pattern5])
        self.matcher.add("Einschätzung", [pattern6])
        self.matcher.add("Einschätzung", [pattern7])
        self.matcher.add("Anforderung", [pattern8])
        self.matcher.add("Frage", [patternF])

    def recognizePatterns(self, input):
            '''
            Method to identify the patterns in a comment.

            Parameters
            -----------
            input : String
                text which is scanned for patterns 
            
            Returns
            -----------
            matched_spans : list
                list of matched spans which correspond to a pattern
            '''

            doc = self.nlp(input)

            # Find matches in the input document
            matches = self.matcher(doc)

            # Extract matched spans from the document
            matched_spans = [(doc[start:end], self.matcher.vocab.strings[match_id]) for match_id, start, end in matches]

            return matched_spans

    def labelTopics(self, topics):
        '''
        Die Funktion labelTopics weist den Topics anhand ihrer IDs Labels zu und gibt ein neues Dictionary zurück, 
        das die Labels und die zugehörigen Wörter enthält.    
        '''
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
            else:
                label = 'Unbekanntes Thema'

            labeled_topics[label] = topic_words

        return labeled_topics

    def visualizeTopics(self, topics):
        '''
        Die Funktion visualizeTopics erstellt eine Visualisierung der Topics mithilfe der 
        PyLDAvis-Bibliothek. Sie verwendet ein LDA-Modell, um die Topics zu analysieren, 
        und speichert die Visualisierung als HTML-Datei ab.
        '''
        dictionary = gensim.corpora.Dictionary(topics.values())
        corpus = [dictionary.doc2bow(words) for words in topics.values()]
        lda_model = gensim.models.LdaModel(corpus, num_topics=len(topics), id2word=dictionary)

        vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
        pyLDAvis.save_html(vis_data, 'lda_visualization.html')


    
    def removeStopwords(self, input):
        '''
        Removes the stopwords from a comment dictionary.

        Parameters
        -----------
        input : str
            comments where the stopwords shall be removed

        Returns
        ----------
        filtered_token : str 
           String that contains comment without the identified stopwords
        '''
        
        doc = self.nlp(input)
        filtered_tokens = [token.text for token in doc if not token.is_stop]
        filtered_comment = ' '.join(filtered_tokens)

        return filtered_comment

    def lowercase(self, input):
        '''
        Transforms the input in lowercase letters.

        Parameters
        -----------
        input : str
            text to transform in lowercase

        Returns
        -----------
        text : str
            transformed lowercase text
        '''
        text = input.lower()

        return text
    
    def removeSpecialChar(self, input):
        '''
        Removes special characters from the input.

        Parameters
        -----------
        input : str
            text to clean

        Returns
        -----------
        text : str
            cleaned text
        '''
        text = re.sub(r'[^a-zA-Z0-9äöüß\s]', '', input.replace('\n', ''))

        return text

    def recognizePatterns(self, input):
        doc = self.nlp(input)
        matcher = Matcher(self.nlp.vocab)
        # Define your pattern(s)
        pattern1 = [{'POS': "ADP"}, {'POS': "DET"}, {'POS': "NOUN", 'ENT_TYPE': "LOC"}]
        pattern2 = [{'POS': "ADP"}, {'POS': "DET"}, {'POS': "PROPN", 'ENT_TYPE': "LOC"}]

        # Add patterns to the matcher
        matcher.add("Einschätzung", [pattern1])
        matcher.add("Einschätzung", [pattern2])

        # Find matches in the document
        matches = matcher(doc)

        # Extract matched spans from the document
        matched_spans = [(doc[start:end], matcher.vocab.strings[match_id]) for match_id, start, end in matches]

        return matched_spans
    
    def pos_tagging(self, input):
        doc = self.nlp(input)

        tagged_tokens = [(token.text, token.pos_) for token in doc]
    
        return tagged_tokens