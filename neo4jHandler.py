from neo4j import GraphDatabase
import json
import os

class neo4jConnector(object):
    '''
    classdocs
    '''
    #bolt://localhost:7687
    # Initialize the connection to neo4j
    def __init__(self):
        try:
            uri = "bolt://graphdatabase:7687" # we need to call the docker service
            userName = "neo4j"
            password = "test"
            self._driver = GraphDatabase.driver(uri, auth=(userName, password), encrypted=False)
            print("Connected...")
        except:
            raise

    def createContributionNode(self, related_node_id):
        with self._driver.session() as session:
            query = "CREATE (con:contributionNode {related_node_id:'" + str(related_node_id) + "'})"
            session.run(query)

    def createCommentNode(self, commentId, related_node_id, relations, entities, locations, sentiment_score):
        special_characters = "/\"'"
        for char in special_characters:
            entities = str(entities).replace(char, "")
            relations = str(relations).replace(char, "")
            locations = str(locations).replace(char, "")

        with self._driver.session() as session:
            query = "CREATE (com:commentNode {commentId:'" + str(commentId) + "', related_node_id:'" + str(related_node_id) + "', entities:'" + str(entities) + "', relations:'" + str(relations) + "', locations:'" + str(locations) + "', sentiment_score:'" + str(sentiment_score) + "'})"
            session.run(query)

    def createLocationNode(self, location):
        with self._driver.session() as session:
            query = "CREATE (loc:locationNode {location:'" + str(location) + "'})"
            session.run(query)          

    def createRelationContributionComment(self, related_node_id, commentId):
        with self._driver.session() as session:
            query = "MATCH (con:contributionNode {related_node_id: '" + str(related_node_id) + "'}) MATCH (com:commentNode {commentId: '" + str(commentId) + "'}) CREATE (con)-[rel:contains]->(com)"
            session.run(query)

    def createRelationLocationComment(self, location, commentId):
        with self._driver.session() as session:
            query = "MATCH (loc:locationNode {location: '" + str(location) + "'}) MATCH (com:commentNode {commentId: '" + str(commentId) + "'}) CREATE (loc)-[rel:appears_in]->(com)"
            session.run(query)

    def checkContributionNodeExists(self, related_node_id):
        with self._driver.session() as session:
            query = "OPTIONAL MATCH (con:contributionNode {related_node_id:'" + str(related_node_id) + "'}) RETURN con IS NOT NULL AS Predicate"
            result = session.run(query)
            record = result.single()
            if record is not None:
                return record[0]
            else:
                return False
            
    def checkLocationNodeExists(self, location):
        with self._driver.session() as session:
            query = "OPTIONAL MATCH (loc:locationNode {location:'" + str(location) + "'}) RETURN loc IS NOT NULL AS Predicate"
            result = session.run(query)
            record = result.single()
            if record is not None:
                return record[0]
            else:
                return False
    
    def deleteAllNodes(self):
        with self._driver.session() as session:
            query = "MATCH (n) DETACH DELETE (n)"
            session.run(query)

    def close(self):
        self._driver.close()