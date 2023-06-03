from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder
from n4j_db.n4j_commons import N4JCommons

class N4JBusiness:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)
        self.__submodules__()

    def __init__(self, driver):
        self.driver = driver
        self.__submodules__()

    def __submodules__(self):
        self.commons = N4JCommons(self.driver)

    def close(self):
        self.driver.close()

    def create_city_bank(self, city, business):
        self.create_city_corp_type(city, business, "Bank")

    def create_city_business(self, city, business):
        self.commons.within("Business", business, "City", city)

    def create_city_corp(self, city, business):
        self.create_city_business(city, business)
        self.commons.node_add_label("Business", business, "Corporation")

    def create_city_corp_type(self, city, corp, type):
        self.create_city_corp(city, corp)
        self.commons.node_add_label("Corporation", corp, type)

    def create_corp_owns_business(self, corp, business):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("b", "Business", "bname")
                .merge_line("c", "Corporation", "cname")
                .relation_basic("c", "b", "OWNS")
                .return_line().text(),
            bname=business,
            cname=corp
        )
        for record in response:
            b1 = record.data().get("b").get("name")
            c1 = record.data().get("c").get("name")
        print(c1, "owns", b1)

    def create_universe_corp(self, universe, corp):
        self.commons.within("Corporation", corp, "Universe", universe)
        self.commons.node_add_label("Corporation", corp, "Business")
