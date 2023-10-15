import requests
#import folium
from pprint import pprint
#from geopy.geocoders import Nominatim
from nlpProcess import nlpProcess
from spacy.tokens import Span
import importJSON
#import gensim
import pyLDAvis.gensim_models as gensimvis
#import pyLDAvis
from spacy.lang.de.stop_words import STOP_WORDS

nlpProc = nlpProcess()

input = importJSON.JSONReader("comments_export2.json") 

# Remove real names in comments.

# Laden der Namen aus den TXT-Dateien in Sets
vornamen = nlpProc.load_txt('vornamen_deutsch.txt')
nachnamen = nlpProc.load_txt('nachnamen_deutsch.txt')

privacy = nlpProc.filterNames(input, vornamen, nachnamen)
print(privacy)


# locations = nlpProc.filterLocations(input)
# print(locations)
# Remove stopwords from each comment.
def calculate_similar_comments():
    preprocess = {}
    for id, comment in input.items():
        # Apply lowercase transformation and removing stopwords and punctuation.
        lower = nlpProc.lowercase(comment['text'])
        nochar = nlpProc.removeSpecialChar(lower)
        preprocess[id] = nlpProc.removeStopwords(nochar)

    similar_comments = nlpProc.calculate_similarities(preprocess, threshold=0.90)
    num_similar_comments = len(similar_comments)

    print("Similar Comments Pairs:")
    for comment_pair in similar_comments:
        comment1_id = comment_pair[0]
        comment2_id = comment_pair[1]
        similarity_score = comment_pair[2]
        comment1_text = input[comment1_id]['text']
        comment2_text = input[comment2_id]['text']
        print(f"Comment {comment1_id}: {comment1_text}")
        print(f"Comment {comment2_id}: {comment2_text}")
        print(f"Similarity Score: {similarity_score:.2f}")
        print()

    print(f"Number of Similar Comments Found: {num_similar_comments}")
