from nlpProcess import nlpProcess

nlpProc = nlpProcess()

scores = nlpProc.analyzeSentiments('Die Dummheit der Unterwerfung blüht in hübschen Farben.')
print(scores)