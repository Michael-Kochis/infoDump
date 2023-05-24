from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JVehicle:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_vehicle(self, vehicle, type):
        response, summary, keys = self.driver.execute_query(
            """MERGE (v :Vehicle {name: $vname, type: $vtype})
            RETURN v;
            """,
            vname=vehicle,
            vtype=type
        )
        for record in response:
            v1 = record.data().get("v").get("name")
        print(v1, "is a", type, "added to the database.")
