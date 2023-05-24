from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import environ

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