from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JUniverse:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_universe(self, universe):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("u", "Universe", "uname")
                .return_line().text(),
            uname=universe
        )
        for record in response:
            u1 = record.data().get("u").get("name")
        print(u1, "is a universe in the database")

    def create_universe_city(self, universe, city):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("u", "Universe", "uname")
                .merge_line("c", "City", "cname")
                .relation_basic("c", "u", "WITHIN")
                .return_line().text(),
            cname=city,
            uname=universe
        )
        for record in response:
            c1 = record.data().get("c").get("name")
            u1 = record.data().get("u").get("name")
        print(c1, "is city within", u1)

