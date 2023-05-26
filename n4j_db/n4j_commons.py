from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JCommons:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def within(self, atype, aname, btype, bname):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("a", atype, "aname")
                .merge_line("b", btype, "bname")
                .relation_basic("a", "b", "WITHIN")
                .return_line().text(),
                aname=aname,
                bname=bname
        )
        for record in response:
            a1 = record.data().get("a").get("name")
            b1 = record.data().get("b").get("name")
        print(a1, "is within", b1)
