
import json
import requests

def get_synonyms(word):
        API_URL = "https://www.openthesaurus.de/synonyme/search?q={}&format=application/json"
        response = requests.get(API_URL.format(word))

        if response.status_code == 200:
            # Konvertierung zu JSON-Datei
            data = json.loads(response.text)
            
            print("Statuscode: 200")
            
            # Synonyme für das Wort werden extrahiert
            synonyms = [term['term'] for term in data['synsets'][0]['terms']]
            return synonyms

        else:
            return "Fehler: Die Anfrage war nicht erfolgreich. Statuscode: " + str(response.status_code)
