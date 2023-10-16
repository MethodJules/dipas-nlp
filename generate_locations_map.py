from nlpProcess import nlpProcess
import importJSON
import folium
import requests
import tqdm

nlpProc = nlpProcess()
input_data = importJSON.JSONReader("comments_export2.json")

locations = nlpProc.filterLocations(input_data)
# print(locations)
bbox = "9.8,53.4,10.3,53.7"  # Bounding box von Hamburg
Straßen_Kordinaten = {}
for street_name in locations:
    url = f"https://nominatim.openstreetmap.org/search?format=json&street={street_name}&city=hamburg&country=Germany&bounded=1&viewbox={bbox}"
    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
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