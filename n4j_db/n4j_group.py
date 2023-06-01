from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ
from n4j_db.n4j_cypher_builder import CypherBuilder

class N4JGroup:
    def __init__(self):
        load_dotenv()

        URI = environ.get("URI")
        AUTH = (environ.get("N4USER"), environ.get("N4PASS"))

        self.driver = GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def create_group(self, group):
        response, summary, keys = self.driver.execute_query(
            """MERGE (g :Group {name: $gname})
            RETURN g;
            """,
            gname=group
        )
        for record in response:
            g1 = record.data().get("g").get("name")
        print(g1, "is a group added to the database.")

    def create_gov(self, group):
        self.create_group(group)
        response, summary, keys = self.driver.execute_query("""
            MATCH (g :Group {name: $gname})
            SET g :Government
            RETURN g;""",
            gname=group
        )
        for record in response:
            g1 = record.data().get("g").get("name")
        print(g1, "is now a government group.")

    def create_group_mask(self, group, mask, role):
        response, summary, keys = self.driver.execute_query("""
            MERGE (g :Group {name: $gname})
            MERGE (m :Mask {name: $mname})
            MERGE (m)-[:MEMBER {role: $rname}]->(g)
            RETURN g, m;""",
            gname=group,
            mname=mask,
            rname=role
        )
        for record in response:
            g1 = record.data().get("g").get("name")
            m1 = record.data().get("m").get("name")

        print(m1, "has role", role, "for", g1)

    def create_group_member(self, group, person, role):
        response, summary, keys = self.driver.execute_query("""
            MERGE (g :Group {name: $gname})
            MERGE (p :Person {name: $pname})
            MERGE (p)-[:MEMBER {role: $rname}]->(g)
            RETURN g, p;""",
            gname=group,
            pname=person,
            rname=role
        )
        for record in response:
            g1 = record.data().get("g").get("name")
            p1 = record.data().get("p").get("name")

        print(p1, "has role", role, "for", g1)

    def create_group_position(self, group, position):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("g", "Group", "gname")
                .merge_line("p", "Position", "pname")
                .relation_basic("p", "g", "POSITION_WITHIN")
                .return_line().text(),
            gname=group,
            pname=position
            )
        for record in response:
            g1 = record.data().get("g").get("name")
            p1 = record.data().get("p").get("name")

        print(p1, "is position within", g1)

    def create_position_person(self, position, person, begin="", end=""):
        response, summary, keys = self.driver.execute_query(
            CypherBuilder().merge_line("p2", "Position", "pname2")
                .merge_line("p1", "Person", "pname")
                .custom_line("MERGE (p1)-[:POSITION {begins: $bname, ends: $ename}]->(p2)", "")
                .return_line().text(),
            bname=begin,
            ename=end,
            pname=person,
            pname2=position
            )
        for record in response:
            p2 = record.data().get("p2").get("name")
            p1 = record.data().get("p1").get("name")

        print("From", begin, "until", end, ", ", p1, "held the position of", p2)