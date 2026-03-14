from neo4j import GraphDatabase
from app.core.config import settings

class Neo4jService:
    def __init__(self):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI, 
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, cypher_query, parameters=None):
        if not self.driver:
            return None
        with self.driver.session() as session:
            result = session.run(cypher_query, parameters)
            return [record.data() for record in result]

neo4j_service = Neo4jService()
