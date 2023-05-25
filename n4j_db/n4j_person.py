from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

class N4JPerson:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_mask(self, mask, person):
        N4JPerson.create_person(self,person)
        response, summary, keys = self.driver.execute_query(
            """MERGE (m :Mask {name: $name})
            MERGE (p :Person {name: $person})
            MERGE (m)-[:CIVILIAN_ID]->(p)
            RETURN m
            """,
            name = mask,
            person = person
        )
        print(mask, "is worn by", person)

    def create_person(self, person):
        response, summary, keys = self.driver.execute_query("MERGE (p :Person {name: $name }) RETURN p",
                name = person)
        for record in response:
            print(record.data().get("p").get("name"),"was added to the database.")

    @staticmethod
    def _find_person(self, person):
        response, summary, keys = self.driver.execute_query("MATCH (p :Person {name: $name }) RETURN p",
                name = person)
        for record in response:
            print(record.data().get("p").get("name"),"was found in the database.")

    def find_mike(self):
        N4JPerson._find_person(self, "Michael Kochis")

if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        find_mike()
        create_mask("Superman", "Clark Kent")
        driver.close()