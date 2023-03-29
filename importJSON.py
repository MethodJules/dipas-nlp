import json

#Angabe des Dateipfad als String
def JSONReader(file_path):

    with open(file_path, "r") as jsonFile:
        jsonData = json.load(jsonFile)

    jsonDict = {}

    for commentID in jsonData:

        related_node_id = jsonData[commentID]["related_node_id"]
        text = jsonData[commentID]["text"]
        jsonDict[commentID] = {"related_node_id": related_node_id, "text": text}

    return jsonDict
