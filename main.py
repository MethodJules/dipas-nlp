import requests
from folium import folium

from hate_speech import nlpProcess
import importJSON

import pandas as pd
import glob
import nltk
nltk.download('vader_lexicon')


nlpProc = nlpProcess()


input_data = importJSON.JSONReader("C:/Users/mhammed/Desktop/comments_export_all.json")


#
# # Compute sentiment scores
# for id, comment in input_data.items():
#     scores = nlpProc.analyzeSentiments(comment)
#     print(f"SentimentScores for comment {id}: {scores}")
#
#
# # Identify relations for each comment.
# for id, comment in input_data.items():
#     relations = nlpProc.extractRelations(comment)
#     print(f"Relations for comment {id}: {relations}")
#
# # Remove stopwords from each comment.
# filtered = nlpProc.removeStopwords(input_data)
# print(filtered)
#
#
# # Remove stopwords from each comment.
# filtered = nlpProc.removeStopwords(list(input_data.values()))
#
# # filtered = nlpProc.removeStopwords(input_data)
#
#
# # Find entities in each comment.
# entities = nlpProc.findEntities(input_data)
# print(entities)
# '''
# #Remove real names in comments.
#
# # Laden der Namen aus den TXT-Dateien in Sets
# vornamen = nlpProc.load_txt('vornamen_deutsch.txt')
# nachnamen = nlpProc.load_txt('nachnamen_deutsch.txt')
#
# <<<<<<< HEAD
# =======
# privacy = nlpProc.filterNames(input, vornamen, nachnamen)
# print(privacy)
#
# >>>>>>> Methode zur Erkennung von Klarnamen wurde überarbeitet.
# # print(locations)
#
# '''
# '''
# hier wurde die OpenStreetMap Nominatim API verwendet, um die Koordinaten von Straßen
# in Hamburg abzurufen und sie auf einer Karte mithilfe von Folium anzuzeigen.
# '''
# locations = nlpProc.filterLocations(input_data)
#
# bbox = "9.8,53.4,10.3,53.7"  # Bounding box von Hamburg
# Straßen_Kordinaten = {}
# for street_name in locations:
#     url = f"https://nominatim.openstreetmap.org/search?format=json&q={street_name}&city=hamburg&country=Germany&bounded=1&viewbox={bbox}"
#     response = requests.get(url)
#     response_data = response.json()
#     if response_data:
#         lat = response_data[0]["lat"]
#         lon = response_data[0]["lon"]
#         Straßen_Kordinaten[street_name] = {"latitude": lat, "longitude": lon}
#
# print(len(Straßen_Kordinaten))
# print(Straßen_Kordinaten)
# map_center = [53.5671 , 10.0271]
# map_osm = folium.Map(location=map_center, zoom_start=13)
#
# for street_name, coords in Straßen_Kordinaten.items():
#     lat = float(coords['latitude'])
#     lon = float(coords['longitude'])
#     marker = folium.Marker([lat, lon], popup=street_name)
#     marker.add_to(map_osm)
#
# # print(len(map_osm))
# map_osm.save("map_osm.html")
#
#
# # Topic Modeling
# topics = nlpProc.performTopicModeling(input_data)
# labeled_topics = nlpProc.labelTopics(topics)
#
# for label, words in labeled_topics.items():
#     print(f"{label}: {words}")
#
# nlpProc.visualizeTopics(labeled_topics)
#
#
# preprocess = {}
# for id, comment in input_data.items():
#         # Apply lowercase transformation and removing stopwords and punctuation.
#         lower = nlpProc.lowercase(comment['text'])
#         nochar = nlpProc.removeSpecialChar(lower)
#         preprocess[id]  = nlpProc.removeStopwords(nochar)
#
#
# similar_comments = nlpProc.calculate_similarities(preprocess, threshold=0.90)
# num_similar_comments = len(similar_comments)
#
# print("Similar Comments Pairs:")
# for comment_pair in similar_comments:
#     comment1_id = comment_pair[0]
#     comment2_id = comment_pair[1]
#     similarity_score = comment_pair[2]
#     comment1_text = input_data[comment1_id]['text']
#     comment2_text = input_data[comment2_id]['text']
#     print(f"Comment {comment1_id}: {comment1_text}")
#     print(f"Comment {comment2_id}: {comment2_text}")
#     print(f"Similarity Score: {similarity_score:.2f}")
#     print()
#
# print(f"Number of Similar Comments Found: {num_similar_comments}")
# # <<<<<<< HEAD
# '''
# =======
#
# >>>>>>> Methode zur Erkennung von Klarnamen wurde überarbeitet.
# matched_dict = {}
# for id, comment in preprocess.items():
#     matched_spans = nlpProc.recognizePatterns(comment)
#     matched_dict[id] = matched_spans, comment
#
# for id, (matched_spans, comment_text) in matched_dict.items():
#     if matched_spans:
#             for span, pattern in matched_spans:
#                 print("ID:", id)
#                 print("Span:", span)
#                 print("Pattern:", pattern)
#                 print("Comment:", comment_text)
#                 print("---")
#
#
#
#
# tagged = {}
# for id, comment in input.items():
#     tagged[id] = nlpProc.pos_tagging(comment['text'])
#
# print(tagged)
# '''
#





hate_speech_result = nlpProc.detectHateSpeech(input_data)

# Ausgabe der erkannten Hate Speech-Kommentare
for result in hate_speech_result:
    print('Text:', result['text'])
    print('Kommentar:', result['comment'])
    # print('Kommentar-ID:', result['comment_id'])
    print('---')
print(len(hate_speech_result))

# Hate Speech erkennen
hate_speech_results = nlpProc.detectHateSpeech2(input_data)

# Ergebnisse anzeigen
for result in hate_speech_results:
    # print("Hate Speech: ", result['Hate Speech'])
    print("Kommentar: ", result['Kommentar'])
    print("Kommentar-ID: ", result['Kommentar-ID'])
    print("\n")
print(len(hate_speech_results))



# Define the path to your CSV files
path = 'C:/Users/mhammed/Downloads/datar/*.csv'
# Get a list of all CSV file paths in the specified directory
csv_files = glob.glob(path)
# Initialize an empty list to store the dataframes
dataframes = []

# Loop through each CSV file
for file in csv_files:
    file = file.replace('\\', '/')
    print(file)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file, sep="\t", header=None, names=["label", "comment_text"])
    # Append the DataFrame to the list
    dataframes.append(df)
    print(f"appended file {file}")

# Concatenate all the DataFrames vertically
data = pd.concat(dataframes, ignore_index=True)


value_counts = data['label'].value_counts()

print(value_counts)


# NaN-Werte entfernen
data = data.dropna()

# Trainieren des Hate-Speech-Modells
model, vectorizer = nlpProc.trainHateSpeechModel(data)

# Ausgabe des trainierten Modells und des Vektorisierers
print("Das Modell wurde erfolgreich trainiert.")
print("Trainiertes Modell:", model)
print("Vektorisierer:", vectorizer)


# Methode detectHateSpeech aufrufen
hate_speech_results = nlpProc.detectHateSpeech1(input_data, model, vectorizer)

# Ergebnisse anzeigen
for result in hate_speech_results:
    print('Hate Speech:', result['text'])
    print('Kommentar:', result['comment'])
    print('Kommentar-ID:', result['comment_id'])
    print('---')

print(len(hate_speech_results))