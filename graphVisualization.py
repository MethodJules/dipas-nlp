import pandas as pd
from neo4jHandler import neo4jConnector
from nlpProcess import nlpProcess
import time
import importJSON

neo4jCon = neo4jConnector()
nlpProc = nlpProcess()

print("Waiting....")
time.sleep(0.5)
print("Continuing...")

tries = 3
for i in range(tries):
    try:
        
        nlpProc.connect_db()
        
        df = pd.read_json("comments_export2.json", orient="index")

        #neo4jCon.deleteAllNodes()
        
        count = 0
        for index, row in df.iterrows():
            
            text = row["text"]
            commentId = index 
            related_node_id = row["related_node_id"]
            relations = nlpProc.extractRelations(text)
            scores = nlpProc.analyzeSentiments(text)
            sentiment_score = nlpProc.getOverallSentimentScore(scores)
            entities = nlpProc.findEntitiesForComment(text)
            locations = set(nlpProc.filterLocationsForComment(text))

            neo4jCon.createCommentNode(commentId, related_node_id, relations, entities, locations, sentiment_score)
            
            contributionNodeExists = neo4jCon.checkContributionNodeExists(related_node_id)
            
            if contributionNodeExists == False:
                neo4jCon.createContributionNode(related_node_id)

            neo4jCon.createRelationContributionComment(related_node_id, commentId)

            for location in locations:
                locationNodeExists = neo4jCon.checkLocationNodeExists(location)

                if locationNodeExists == False:
                    neo4jCon.createLocationNode(location)

                neo4jCon.createRelationLocationComment(location, commentId)
            
            count += 1
            if count == 100:
                break
        print("Graph created...")
        neo4jCon.close()
        
    except Exception as e:
        if (type(e).__name__=="ServiceUnavilable" and i < tries -1):
            print("Retry connecting...")
            continue
        else:
            raise
    break

