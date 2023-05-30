from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_commons import N4JCommons
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JNation:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver
        self.common = N4JCommons(self.driver)
        self.cypher = CypherBuilder()

    def close(self):
        self.driver.close()

    def create_continent_nation(self, continent, nation):
        results, summary, keys = self.driver.execute_query(
            self.cypher.clear()
                .custom_line("MERGE (n :Region :Nation {name: $nname})", "n")
                .custom_line("MERGE (c :Region :Continent {name: $cname})", "c")
                .relation_basic("c", "p", "WITHIN")
                .return_line().text(),
            cname=continent,
            nname=nation
        )
        for record in results:
            c1 = record.data().get("c").get("name")
            n1 = record.data().get("n").get("name")
        print(n1, "is a nation within", c1)

    def create_star_planet(self, star, planet):
        self.common.within("Star", star, "Planet", planet)

if __name__ == "__main__":
    print("This is where unit testing would go.")