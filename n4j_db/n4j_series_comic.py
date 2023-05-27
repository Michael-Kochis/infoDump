from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JSeriesComic:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_series_mask_person(self, series, mask, person):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("m", "Mask", "mname")
                .merge_line("p", "Person", "pname")
                .merge_line("s", "Series_Comic", "sname")
                .relation_basic("m", "s", "WITHIN")
                .relation_basic("m", "p", "CIVILIAN_ID")
                .return_line().text(),
            mname=mask,
            pname=person,
            sname=series
        )
        for record in response:
            m1 = record.data().get("m").get("name")
            p1 = record.data().get("p").get("name")
            s1 = record.data().get("s").get("name")
        print(p1, "wears the mask of", m1, "in comic series", s1)

    def create_series_loc(self, series, location):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("s", "Series_Comic", "sname")
                .merge_line("l", "Location", "lname")
                .relation_basic("l", "s", "WITHIN")
                .return_line().text(),
            lname = location,
            sname = series
        )
        for record in response:
            s1 = record.data().get("s").get("name")
            l1 = record.data().get("l").get("name")
        print(l1, "is location within", s1)

    def create_series_comic(self, series, comic):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("s", "Series_Comic", "sname")
                .merge_line("c", "Comic", "cname")
                .relation_basic("c", "s", "WITHIN")
                .return_line().text(),
            sname=series,
            cname=comic
        )
        for record in response:
            c1 = record.data().get("c").get("name")
            s1 = record.data().get("s").get("name")
        print(c1, "is comic in series", s1)

    def create_series_person(self, series, person):

        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("s", "Series_Comic", "sname")
                .merge_line("p", "Person", "pname")
                .relation_basic("p", "s", "WITHIN")
                .return_line().text(),
            pname = person,
            sname = series
        )
        for record in response:
            s1 = record.data().get("s").get("name")
            p1 = record.data().get("p").get("name")
        print(p1, "is a person within", s1)

    def create_universe_series(self, universe, series):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("s", "Series_Comic", "sname")
                .merge_line("u", "Universe", "uname")
                .relation_basic("s", "u", "WITHIN")
                .return_line().text(),
            uname=universe,
            sname=series
        )
        for record in response:
            s1 = record.data().get("s").get("name")
            u1 = record.data().get("u").get("name")
        print(s1, "is a comic series within", u1)
