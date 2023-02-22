from nlpProcess import nlpProcess
from neo4jHandler import neo4jConnector
import time

nlpProc = nlpProcess()
neo4jCon = neo4jConnector()
print("Waiting....")
time.sleep(0.5)
print("Continuing...")

comment = 'Die Einrichtung der "Ruhigen Gebiete" ist für uns Anwohner in Kirchwerder natürlich sehr zu begrüßen. Allerdings besteht nach wie vor das seit langem bekannte Problem des exzessiven und extrem lärmbelastenden Motorradverkehrs auf den Straßen am Deich (insbesondere auch in der Nähe der Kirchwerder Wiesen). Es wäre wirklich begrüßenswert und wichtig, dass die Stadt hier sehr viel häufiger Verkehrskontrollen vornimmt, damit die gewünschte Ruhe auch gewährleistet und geschützt werden kann.'
#scores = nlpProc.analyzeSentiments('Die Dummheit der Unterwerfung blüht in hübschen Farben.')
#print(scores)

#ners = nlpProc.nameEntityRecognition('Gerne mehr Strassenbäume im Nördlichen Teil der Lindenalle. Und besonders dort auch bitte kein Querparken mehr, von den schmalen Gehwegen bleibt ja durch den überstand der Autos fast gar nichts mehr übrig. Die gesamte Lindenalle sollte breitere Gehwege erhalten. Da muss man halt notfalls auch mal ein wenig Parkraum oder Strassenraum abzwacken. Irgendwo muss der Platz ja herkommen. Und der Platz am Wendehammer sollte umgestaltet werden, mit blumen und evtl. einem Brunnen.')
#print(ners)

## Connect to the graph database
tries = 3
for i in range(tries):
    try:
        # connect to the graph database
        nlpProc.connect_db()
        # calculate the the sentiment score of a comment [(-1)--(0)--(+1)]
        scores = nlpProc.analyzeSentiments(comment)
        sentiment_score = nlpProc.getOverallSentimentScore(scores)
        neo4jCon.createCommentNode(4, comment, sentiment_score)
    except Exception as e:
        if (type(e).__name__=="ServiceUnavilable" and i < tries -1):
            print("Retry connecting...")
            continue
        else:
            raise
    break
