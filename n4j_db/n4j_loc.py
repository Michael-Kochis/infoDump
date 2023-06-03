from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder
from n4j_db.n4j_commons import N4JCommons

class N4JLoc:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)
        self.__submethods__()

    def __init__(self, driver):
        self.driver = driver
        self.__submethods__()

    def __submethods__(self):
        self.commons = N4JCommons(self.driver)

    def close(self):
        self.driver.close()

    def create_city(self, city):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("c", "City", "cname")
                .return_line().text(),
            name = city
        )
        for record in response:
            c1 = record.data().get("c").get("name")
        print(c1,"was added to the database.")

    def create_city_loc(self, city, location):
        self.commons.within("Location", location, "City", city)

    def create_city_loc_type(self, city, location, type):
        self.commons.within("Location", location, "City", city)
        self.commons.node_add_label("Location", location, type)

    def create_city_region(self, city, region):
        self.commons.within("Region", region, "City", city)

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