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

    def create_series_x_nation(self, series, type, nation):
        self.common.within("Nation", nation, type, series)

    def create_series_b_nation(self, series, nation):
        self.create_series_x_nation(series, "Series_Book", nation)

    def create_series_c_nation(self, series, nation):
        self.create_series_x_nation(series, "Series_Comic", nation)

    def create_series_m_nation(self, series, nation):
        self.create_series_x_nation(series, "Series_Movie", nation)

    def create_series_t_nation(self, series, nation):
        self.create_series_x_nation(series, "Series_TV", nation)

if __name__ == "__main__":
    print("This is where unit testing would go.")