import requests
#import folium
from pprint import pprint
#from geopy.geocoders import Nominatim
from nlpProcess import nlpProcess
from spacy.tokens import Span
import importJSON
#import gensim
#import pyLDAvis.gensim_models as gensimvis
#import pyLDAvis
from spacy.lang.de.stop_words import STOP_WORDS





nlpProc = nlpProcess()

input = importJSON.JSONReader("comments_export2.json") 

'''
# Compute sentiment scores
for id, comment in input.items():
    scores = nlpProc.analyzeSentiments(comment)
    print(f"SentimentScores for comment {id}: {scores}")


# Identify relations for each comment.
for id, comment in input.items():
    relations = nlpProc.extractRelations(comment)
    print(f"Relations for comment {id}: {relations}")

# Remove stopwords from each comment.
filtered = nlpProc.removeStopwords(input)
print(filtered)


# Remove stopwords from each comment.
filtered = nlpProc.removeStopwords(list(input.values()))

# filtered = nlpProc.removeStopwords(input)


# Find entities in each comment.
entities = nlpProc.findEntities(input)
print(entities)
'''
# Remove real names in comments.
#privacy = nlpProc.filterNames(input)
#print(privacy)

#locations = nlpProc.filterLocations(input)
# print(locations)

'''
hier wurde die OpenStreetMap Nominatim API verwendet, um die Koordinaten von Straßen 
in Hamburg abzurufen und sie auf einer Karte mithilfe von Folium anzuzeigen.

bbox = "9.8,53.4,10.3,53.7"  # Bounding box von Hamburg
Straßen_Kordinaten = {}
for street_name in locations:
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={street_name}&city=hamburg&country=Germany&bounded=1&viewbox={bbox}"
    response = requests.get(url)
    response_data = response.json()
    if response_data:
        lat = response_data[0]["lat"]
        lon = response_data[0]["lon"]
        Straßen_Kordinaten[street_name] = {"latitude": lat, "longitude": lon}

print(len(Straßen_Kordinaten))
print(Straßen_Kordinaten)
map_center = [53.5671 , 10.0271]
map_osm = folium.Map(location=map_center, zoom_start=13)

for street_name, coords in Straßen_Kordinaten.items():
    lat = float(coords['latitude'])
    lon = float(coords['longitude'])
    marker = folium.Marker([lat, lon], popup=street_name)
    marker.add_to(map_osm)

# print(len(map_osm))
map_osm.save("map_osm.html")


# Topic Modeling
topics = nlpProc.performTopicModeling(input)
labeled_topics = nlpProc.labelTopics(topics)

for label, words in labeled_topics.items():
    print(f"{label}: {words}")

nlpProc.visualizeTopics(labeled_topics)

'''
# Remove stopwords from each comment.

preprocess = {}
for id, comment in input.items():
        # Apply lowercase transformation and removing stopwords and punctuation.
        lower = nlpProc.lowercase(comment['text'])
        nochar = nlpProc.removeSpecialChar(lower)
        preprocess[id]  = nlpProc.removeStopwords(nochar)


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
'''
matched_dict = {}
for id, comment in preprocess.items():
    matched_spans = nlpProc.recognizePatterns(comment)
    matched_dict[id] = matched_spans, comment

for id, (matched_spans, comment_text) in matched_dict.items():
    if matched_spans:
            for span, pattern in matched_spans:
                print("ID:", id)
                print("Span:", span)
                print("Pattern:", pattern)
                print("Comment:", comment_text)
                print("---")


            

tagged = {}
for id, comment in input.items():
    tagged[id] = nlpProc.pos_tagging(comment['text'])

print(tagged)
'''