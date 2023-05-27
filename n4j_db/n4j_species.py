from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JSpecies:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_person_species(self, person, species):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("p", "Person", "pname")
                .custom_line("MERGE (s :Template :Species {name: $sname})", ("s"))
                .relation_basic("p", "s", "TEMPLATE")
                .relation_basic("p", "s", "SPECIES")
                .return_line().text(),
            pname=person,
            sname=species
        )
        for record in response:
            p1 = record.data().get("p").get("name")
            s1 = record.data().get("s").get("name")
        print(p1, "is of species:", s1)

    def create_subspecies(self, species, subspecies):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("s1", "Species", "sname")
                .merge_line("s2", "Species", "sname2")
                .relation_basic("s2", "s1", "WITHIN")
                .return_line().text(),
            sname=species,
            sname2=subspecies
        )
        for record in response:
            s1 = record.data().get("s1").get("name")
            s2 = record.data().get("s2").get("name")
        print(s2, "is a subspecies of", s1)