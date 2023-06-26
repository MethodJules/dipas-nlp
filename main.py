from nlpProcess import nlpProcess
import importJSON
import requests
import folium
from pprint import pprint
from geopy.geocoders import Nominatim
import importJSON
from nlpProcess import nlpProcess
import gensim
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from spacy.lang.de.stop_words import STOP_WORDS

nlpProc = nlpProcess()

input_data = importJSON.JSONReader("C:/Users/mhammed/Desktop/comments_export2.json")


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

# Remove real names in comments.
privacy = nlpProc.filterNames(input)
print(privacy)


locations = nlpProc.filterLocations(input)
# print(locations)

'''
hier wurde die OpenStreetMap Nominatim API verwendet, um die Koordinaten von Straßen 
in Hamburg abzurufen und sie auf einer Karte mithilfe von Folium anzuzeigen.
'''
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
topics = nlpProc.performTopicModeling(input_data)
labeled_topics = nlpProc.labelTopics(topics)

for label, words in labeled_topics.items():
    print(f"{label}: {words}")

nlpProc.visualizeTopics(labeled_topics)

