from neo4j import GraphDatabase
import json
import os

class neo4jConnector(object):
    '''
    classdocs
    '''

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

    def createRootNode(self, contributionId):
        with self._driver.session() as session:
            query = "CREATE (rn:RootNode {contributionId:'" + str(contributionId) + "'})"
            session.run(query)

    def close(self):
        self._driver.close()