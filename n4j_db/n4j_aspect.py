from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

class N4JAspect:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_person_aspect(self, person, aspect):
        response, summary, keys = self.driver.execute_query(
            """MERGE (p :Person {name: $pname})
            MERGE (a :Aspect {name: $aname})
            MERGE (p)-[:ASPECT]->(a)
            RETURN a, p;
            """,
            pname=person,
            aname=aspect
        )
        for record in response:
            a1 = record.data().get("a").get("name")
            p1 = record.data().get("p").get("name")
        print(p1, "has aspect:", a1)