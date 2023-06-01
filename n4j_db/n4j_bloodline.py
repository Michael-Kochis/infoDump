from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JBloodline:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_person_bloodline(self, person, bloodline):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("p", "Person", "pname")
                .custom_line("MERGE (b :Template :Bloodline {name: $bname})", ("b"))
                .relation_basic("p", "b", "TEMPLATE")
                .relation_basic("p", "b", "BLOODLINE")
                .return_line().text(),
            pname=person,
            bname=bloodline
        )
        for record in response:
            p1 = record.data().get("p").get("name")
            b1 = record.data().get("b").get("name")
        print(p1, "is of the bloodline:", b1)

    def create_branch(self, blood, branch):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("b1", "Bloodline", "bname")
                .merge_line("b2", "Bloodline", "bname2")
                .relation_basic("b2", "b1", "DERIVE_FROM")
                .return_line().text(),
            bname=blood,
            bname2=branch
        )
        for record in response:
            b1 = record.data().get("b1").get("name")
            b2 = record.data().get("b2").get("name")
        print(b2, "descends from", b1)