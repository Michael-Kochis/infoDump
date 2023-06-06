from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder
from n4j_db.n4j_commons import N4JCommons

class N4JSeriesTV:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)
        self.__submodule__()

    def __init__(self, driver):
        self.driver = driver
        self.__submodule__()

    def __submodule__(self):
        self.common = N4JCommons(self.driver)

    def close(self):
        self.driver.close()

    def create_mask_series(self, series, mask, person):
        self.common.within("Mask", mask, "Series_TV", series)

        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("m", "Mask", "mname")
                .merge_line("p", "Person", "pname")
                .relation_basic("m", "p", "CIVILIAN_ID")
                .return_line().text(),
            mname=mask,
            pname=person
        )
        for record in response:
            m1 = record.data().get("m").get("name")
            p1 = record.data().get("p").get("name")
        print(p1, "wears the mask of", m1)

    def create_loc_series(self, series, location):
        self.common.within("Location", location, "Series_TV", series)

    def create_series_business(self, series, business):
        self.common.within("Business", business, "Series_TV", series)

    def create_series_city(self, series, city):
        self.common.within("City", city, "Series_TV", series)

    def create_series_group(self, series, group):
        self.common.within("Group", group, "Series_TV", series)

    def create_series_person(self, series, person):
        self.common.within("Person", person, "Series_TV", series)

    def create_universe_series(self, universe, series):
        self.common.within("Series_TV", series, "Universe", universe)
