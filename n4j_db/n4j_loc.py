from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

class N4JLoc:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_city(self, city):
        response, summary, keys = self.driver.execute_query(
            "MERGE (c :City {name: $name})"
            "RETURN c",
            name = city
        )
        for record in response:
            print(record.data().get("c").get("name"),"was added to the database.")

    def create_city_loc(self, city, location):
        response, summary, keys = self.driver.execute_query(
            """MERGE (c :City {name: $cname})
            MERGE (l :Location {name: $lname})
            MERGE (l)-[:WITHIN]->(c)
            RETURN c, l;""",
            cname = city,
            lname = location
        )
        print(location, "is within", city)

    def create_city_region(self, city, region):
        response, summary, keys = self.driver.execute_query(
            """MERGE (c :City {name: $cname})
            MERGE (r :Location :Region {name: $rname})
            MERGE (r)-[:WITHIN]->(c)
            RETURN c, r;""",
            cname = city,
            rname = region
        )
        for record in response:
            c1 = record.data().get("c").get("name")
            r1 = record.data().get("r").get("name")
        print(r1, "is within", c1)

    def create_loc(self, location):
        response, summary, keys = self.driver.execute_query(
            "MERGE (l :Location {name: $name})"
            "RETURN l",
            name = location
        )
        for record in response:
            print(record.data().get("l").get("name"),"was added to the database as a location.")


if __name__ == "__main__":
    print("This is where standalone tests of n4j_loc would go.")