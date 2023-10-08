import spacy
import os
from gensim import corpora, models
import gensim
import pyLDAvis.gensim as gensimvis
import pyLDAvis
import spacy
from spacy.lang.de.stop_words import STOP_WORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from imblearn.over_sampling import RandomOverSampler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.pipeline import Pipeline
import requests
import csv
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from spacy.lang.de.stop_words import STOP_WORDS
from nltk.stem import SnowballStemmer
from sklearn.metrics import accuracy_score
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
        self.model = None
        # modify the spacy pipeline
        self.nlp.add_pipe('sentiws', config={'sentiws_path': 'data/sentiws'})

    #     self.matcher = Matcher(self.nlp.vocab)
    #     self.initializeMatcher()
    #
    # def connect_db(self):
    #     self.driver = neo4jConnector()

    def analyzeSentiments(self, text):
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
    
    def findEntitiesForComment(self, comment):

        doc = self.nlp(comment)
        entity_list = []
        for ent in doc.ents:
            entity_list.append({'Entität': ent.text,'Typ': ent.label_})

        return entity_list

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
		
    def detectHateSpeech(self, comments_input):
        '''
        Erkennt Hate Speech in den Kommentaren.

        Parameters
        -----------
        comments_input : dict
            Dictionary von Kommentaren, die auf Hate Speech überprüft werden sollen.

        Returns
        ----------
        hate_speech_list : list
            Liste der erkannten Hate Speech-Kommentare mit Text, vollständigem Kommentar und Kommentar-ID.
        '''
        analyzer = SentimentIntensityAnalyzer()
        hate_speech_list = []
        threshold = -0.92  # Benutzerdefinierter Schwellenwert

        for id, comment in comments_input.items():
            sentiment_scores = analyzer.polarity_scores(comment['text'])
            compound_score = sentiment_scores['compound']
            negative_score = sentiment_scores['neg']
            positive_score = sentiment_scores['pos']

            if compound_score < threshold and negative_score > positive_score:
                hate_speech_list.append({
                    'text': comment['text'],
                    'comment': comment,
                    'comment_id': id
                })

        return hate_speech_list

#####
    def detectHateSpeech2(self, comments_input):
        '''
        Erkennt Hate Speech in den Kommentaren und gibt die entsprechenden Ergebnisse zurück.

        Parameters:
        -----------
        comments_input : dict
            Ein Wörterbuch mit Kommentaren, die analysiert werden sollen.

        Returns:
        ----------
        hate_speech_results : list
            Eine Liste von Wörterbüchern, die den Text, den gesamten Kommentar und die Kommentar-ID enthalten, für die Hate Speech erkannt wurde.
        '''
        hate_speech_results = []
        for id, comment_data in comments_input.items():
            if 'text' in comment_data:  # Überprüfen, ob der Schlüssel 'text' im Wörterbuch vorhanden ist
                comment_text = comment_data['text']
                sentiment_scores = self.analyzeSentiments(comment_text)
                for score in sentiment_scores:
                    if score['sentiment_score'] is not None and score['sentiment_score'] < -0.6:
                        hate_speech_results.append({
                            'Hate Speech': score['text'],
                            'Kommentar': comment_text,
                            'Kommentar-ID': id
                        })
        return hate_speech_results

####

    def trainHateSpeechModel(self, labeled_data):
        '''
        Trainiert (mit NBais) ein Modell zur Hate-Speech-Erkennung auf Grundlage von annotierten Daten.

        Parameters
        -----------
        labeled_data : DataFrame
            Dataframe mit annotierten Daten, die positive (Hate Speech), negative (kein Hate Speech) oder neutrale Kommentare enthalten.

        Returns
        ----------
        model : MultinomialNB
            Das trainierte Modell zur Hate-Speech-Erkennung.
        vectorizer : TfidfVectorizer
            Der TfidfVectorizer zur Transformation der Kommentare in Vektoren.
        '''
        # Textvektorisierung
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(labeled_data['comment_text'])
        y = labeled_data['label']

        # Oversampling für die "hs"-Klasse durchführen
        oversampler = RandomOverSampler(sampling_strategy='auto')
        X_resampled, y_resampled = oversampler.fit_resample(X, y)
        print(X_resampled.shape, y_resampled.shape)
        # Naive Bayes-Modelltraining mit den resamplen Daten durchführen
        model = MultinomialNB()
        model.fit(X_resampled, y_resampled)
        self.model = model  # Speichern des Modells im Attribut der Klasse

        # Berechnung der Genauigkeit auf den Trainingsdaten
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        print("Accuracy on training data:", accuracy)

        return model, vectorizer

    # def trainHateSpeechModel(self, labeled_data):
    #     '''
    #     Trainiert (mit SVM) ein Modell zur Hate-Speech-Erkennung auf Grundlage von annotierten Daten.
    #
    #     Parameters
    #     -----------
    #     labeled_data : DataFrame
    #         Dataframe mit annotierten Daten, die positive (Hate Speech), negative (kein Hate Speech) oder neutrale Kommentare enthalten.
    #
    #     Returns
    #     ----------
    #     model : SVC
    #         Das trainierte Modell zur Hate-Speech-Erkennung.
    #     vectorizer : TfidfVectorizer
    #         Der TfidfVectorizer zur Transformation der Kommentare in Vektoren.
    #     '''
    #     # Textvektorisierung
    #     vectorizer = TfidfVectorizer()
    #     X = vectorizer.fit_transform(labeled_data['comment_text'])
    #     y = labeled_data['label']
    #
    #     # Oversampling für die "hs"-Klasse durchführen
    #     oversampler = RandomOverSampler(sampling_strategy='auto')
    #     X_resampled, y_resampled = oversampler.fit_resample(X, y)
    #     # SVM-Modelltraining mit den resamplen Daten durchführen
    #     model = SVC()
    #     model.fit(X_resampled, y_resampled)
    #     self.model = model  # Speichern des Modells im Attribut der Klasse
    #
    #     # Berechnung der Genauigkeit auf den Trainingsdaten
    #     y_pred = model.predict(X)
    #     accuracy = accuracy_score(y, y_pred)
    #     print("Accuracy on training data:", accuracy)
    #
    #     return model, vectorizer

    def detectHateSpeech1(self, comments_input, model, vectorizer):
        '''
        Erkennt Hate Speech in den Kommentaren und gibt die entsprechenden Ergebnisse zurück.

        Parameters:
        -----------
        comments_input : dict
            Ein Wörterbuch mit Kommentaren, die analysiert werden sollen.
        model : sklearn.svm.SVC
            Das trainierte Modell für die Hate Speech-Erkennung.
        vectorizer : sklearn.feature_extraction.text.TfidfVectorizer
            Der verwendete Vektorisierer.

        Returns:
        ----------
        hate_speech_results : list
            Eine Liste von Wörterbüchern, die den Text, den gesamten Kommentar und die Kommentar-ID enthalten, für die Hate Speech erkannt wurde.
        '''
        hate_speech_results = []
        for id, comment_data in comments_input.items():
            text = comment_data['text']
            processed_text = self.preprocessText(text)
            vectorized_text = vectorizer.transform([processed_text])
            prediction = model.predict(vectorized_text)[0]
            if prediction == 'hs':
                hate_speech_results.append({
                    'text': text,
                    'comment': comment_data,
                    'comment_id': id
                })

        return hate_speech_results


    def preprocessText(self, text):
        # Umwandeln in Kleinbuchstaben
        processed_text = text.lower()

        # Entfernen von Sonderzeichen und Satzzeichen
        processed_text = re.sub(r"[^a-zA-Z0-9ÄÖÜäöüß]", " ", processed_text)

        # Tokenisierung (optional)
        # tokenized_text = processed_text.split()

        # Entfernen von Stoppwörtern
        stop_words = set(stopwords.words("german"))
        processed_text = " ".join(word for word in processed_text.split() if word not in stop_words)

        # Stemming (z. B. Wortstammreduktion)
        stemmer = SnowballStemmer("german")
        processed_text = " ".join(stemmer.stem(word) for word in processed_text.split())

        return processed_text
