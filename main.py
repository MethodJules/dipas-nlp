from nlpProcess import nlpProcess

nlpProc = nlpProcess()

scores = nlpProc.analyzeSentiments('Die Dummheit der Unterwerfung blüht in hübschen Farben.')
entities = nlpProc.findEntities(
    {"1": "Die Westallee in Hamburg sollte umgebaut werden.",
    "2": "Die Lange Straße in Köln ist baufällig"})

print(scores)
print(entities)