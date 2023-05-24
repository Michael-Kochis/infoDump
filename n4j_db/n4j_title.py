from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JTitle:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_mask_title(self, mask, title):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("m", "Mask", "mname")
                .merge_line('t', 'Title', "tname")
                .relation_basic('m', 't', "TITLE")
                .return_line().text(),
            mname=mask,
            tname=title
        )
        for record in response:
            m1 = record.data().get("m").get("name")
            t1 = record.data().get("t").get("name")
        print(m1, "is titled", t1)


def create_person_title(self, person, title):
    response, summary, keys = self.driver.execute_query(
        CypherBuilder().merge_line("p", "Person", "pname")
                .merge_line('t', 'Title', "tname")
                .relation_basic('m', 't', "TITLE")
                .return_line().text(),
        pname=person,
        tname=title
    )
    for record in response:
        p1 = record.data().get("p").get("name")
        t1 = record.data().get("t").get("name")
    print(p1, "is titled", t1)


if __name__ == "__main__":
    print("This is where testing would go.")