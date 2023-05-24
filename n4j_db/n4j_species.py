from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

class N4JSpecies:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_person_species(self, person, species):
        response, summary, keys = self.driver.execute_query(
            """MERGE (p :Person {name: $pname})
            MERGE (s :Template :Species {name: $sname})
            MERGE (p)-[:TEMPLATE]->(s)
            MERGE (p)-[:SPECIES]->(s)
            RETURN p, s;
            """,
            pname=person,
            sname=species
        )
        for record in response:
            p1 = record.data().get("p").get("name")
            s1 = record.data().get("s").get("name")
        print(p1, "is of species:", s1)